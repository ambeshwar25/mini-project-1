from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import sqlite3
from pathlib import Path
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'academichub.db'
UPLOAD_DIR = BASE_DIR / 'uploads'
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt'}
app = Flask(__name__)
app.secret_key = 'change-this-demo-secret'


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            subject_code TEXT DEFAULT '',
            semester TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            faculty TEXT DEFAULT '',
            description TEXT DEFAULT '',
            filename TEXT DEFAULT '',
            link TEXT DEFAULT '',
            verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        count = conn.execute('SELECT COUNT(*) FROM resources').fetchone()[0]
        if count == 0:
            sample = [
                ('Data Structures Unit Notes', 'Data Structures', 'KCS301', '3', 'Lecture Notes', 'CSE Faculty', 'Sample notes entry. Replace this with your own file or link.', '', '', 1),
                ('Digital Logic Design PYQ', 'Digital Logic Design', 'KCS302', '3', 'Previous Year Paper', 'CSE Faculty', 'Sample previous-year paper entry.', '', '', 1),
                ('DBMS Lab Manual', 'Database Management Systems', 'KCS403', '4', 'Lab Manual', 'Computer Science Department', 'Sample lab manual entry.', '', '', 0),
            ]
            conn.executemany('''INSERT INTO resources
                (title, subject, subject_code, semester, resource_type, faculty, description, filename, link, verified)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', sample)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    q = request.args.get('q', '').strip()
    semester = request.args.get('semester', '').strip()
    resource_type = request.args.get('type', '').strip()
    sql = 'SELECT * FROM resources WHERE 1=1'
    params = []
    if q:
        pattern = f'%{q}%'
        sql += ''' AND (title LIKE ? OR subject LIKE ? OR subject_code LIKE ?
                  OR faculty LIKE ? OR description LIKE ?)'''
        params.extend([pattern] * 5)
    if semester:
        sql += ' AND semester = ?'
        params.append(semester)
    if resource_type:
        sql += ' AND resource_type = ?'
        params.append(resource_type)
    sql += ' ORDER BY created_at DESC, id DESC'
    with connect_db() as conn:
        resources = conn.execute(sql, params).fetchall()
        total = conn.execute('SELECT COUNT(*) FROM resources').fetchone()[0]
        verified_count = conn.execute('SELECT COUNT(*) FROM resources WHERE verified = 1').fetchone()[0]
    return render_template('index.html', resources=resources, q=q, semester=semester,
                           resource_type=resource_type, total=total, verified_count=verified_count)


@app.route('/add', methods=['POST'])
def add_resource():
    title = request.form.get('title', '').strip()
    subject = request.form.get('subject', '').strip()
    semester = request.form.get('semester', '').strip()
    resource_type = request.form.get('resource_type', '').strip()
    if not all([title, subject, semester, resource_type]):
        flash('Please fill all required fields.', 'error')
        return redirect(url_for('index'))

    uploaded_file = request.files.get('file')
    filename = ''
    if uploaded_file and uploaded_file.filename:
        if not allowed_file(uploaded_file.filename):
            flash('Allowed files: PDF, DOC, DOCX, PPT, PPTX, TXT.', 'error')
            return redirect(url_for('index'))
        filename = secure_filename(uploaded_file.filename)
        # Avoid overwriting an existing file with the same name.
        target = UPLOAD_DIR / filename
        if target.exists():
            target = UPLOAD_DIR / f'{Path(filename).stem}_{os_random_suffix()}{Path(filename).suffix}'
            filename = target.name
        uploaded_file.save(target)

    data = (title, subject, request.form.get('subject_code', '').strip(), semester,
            resource_type, request.form.get('faculty', '').strip(),
            request.form.get('description', '').strip(), filename,
            request.form.get('link', '').strip(), 0)
    with connect_db() as conn:
        conn.execute('''INSERT INTO resources
            (title, subject, subject_code, semester, resource_type, faculty, description, filename, link, verified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    flash('Resource added successfully. It is marked unverified until reviewed by faculty.', 'success')
    return redirect(url_for('index'))


def os_random_suffix():
    import secrets
    return secrets.token_hex(3)


@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)


@app.route('/verify/<int:resource_id>', methods=['POST'])
def verify_resource(resource_id):
    # Demo-only verification toggle; no authentication is implemented.
    with connect_db() as conn:
        row = conn.execute('SELECT verified FROM resources WHERE id = ?', (resource_id,)).fetchone()
        if row:
            conn.execute('UPDATE resources SET verified = ? WHERE id = ?', (0 if row['verified'] else 1, resource_id))
            flash('Verification status updated (demo mode).', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    print('AcademicHub is running at http://127.0.0.1:5000')
    app.run(debug=True)
