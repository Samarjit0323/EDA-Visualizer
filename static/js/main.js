const modal = document.getElementById("uploadModal");
const openBtn = document.getElementById("openUploadModal");
const closeBtn = document.getElementById("closeModal");

// open modal
openBtn.addEventListener("click", (e) => {
    e.preventDefault();
    modal.style.display = "block";
});

// close modal
closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
});

// close when clicking outside
window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});

// File upload functionality
const fileInput = document.getElementById('formFileLg');
const fileName = document.getElementById('fileName');
const fileUploadLabel = document.querySelector('.file-upload-label');

fileInput.addEventListener('change', function() {
    if (this.files && this.files[0]) {
        fileName.textContent = this.files[0].name;
    } else {
        fileName.textContent = 'No file chosen';
    }
});

// Drag and drop
fileUploadLabel.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadLabel.style.borderColor = 'aqua';
    fileUploadLabel.style.background = 'rgba(0, 255, 255, 0.1)';
});

fileUploadLabel.addEventListener('dragleave', () => {
    fileUploadLabel.style.borderColor = 'rgba(255, 255, 255, 0.3)';
    fileUploadLabel.style.background = 'rgba(255, 255, 255, 0.05)';
});

fileUploadLabel.addEventListener('drop', (e) => {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
    fileInput.dispatchEvent(new Event('change'));
    fileUploadLabel.style.borderColor = 'rgba(255, 255, 255, 0.3)';
    fileUploadLabel.style.background = 'rgba(255, 255, 255, 0.05)';
});
