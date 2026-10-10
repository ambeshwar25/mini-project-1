document.addEventListener('DOMContentLoaded', () => {
  const searchInputs = document.querySelectorAll('input[type="search"]');
  searchInputs.forEach((input) => {
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') input.value = '';
    });
  });
  const fileInput = document.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.addEventListener('change', () => {
      const file = fileInput.files && fileInput.files[0];
      if (file && file.size > 15 * 1024 * 1024) {
        alert('Please choose a file smaller than 15 MB.');
        fileInput.value = '';
      }
    });
  }
});
