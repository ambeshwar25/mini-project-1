# AcademicHub — Simple Python Mini Project

A beginner-friendly Department Academic Notes & Resource Sharing Portal built with **Python + Flask + SQLite**, with HTML, CSS and a small amount of JavaScript for the interface.

## Features
- Search by title, subject, subject code, faculty, or description
- Filter by semester and resource type
- Add a resource with optional file upload or external URL
- Download uploaded documents
- SQLite database is created automatically on first run
- Three sample resources are inserted automatically
- Simple faculty-verification toggle for demonstration only

## Requirements
- Python 3.10 or newer recommended
- VS Code (optional but recommended)

## Run on Windows in VS Code
1. Extract the ZIP and open the `academichub-python` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```
4. Activate it in PowerShell:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt terminal and run:
   ```bat
   .venv\Scripts\activate.bat
   ```
5. Install Flask:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Start the app:
   ```powershell
   python app.py
   ```
7. Open `http://127.0.0.1:5000` in your browser.
8. Stop the server with `Ctrl+C` in the terminal.

## Notes
- No MySQL, Node.js, or separate database setup is required. SQLite file `academichub.db` is created automatically.
- Uploaded files are saved in the local `uploads/` directory.
- The verification toggle is for classroom demonstration only. There is no real login, access control, or production-grade security. Do not deploy this demo publicly as-is.
- Allowed uploads: PDF, DOC, DOCX, PPT, PPTX, TXT.
