// jshint esversion: 11

document.addEventListener("DOMContentLoaded", () => {
    const dropArea = document.getElementById("drop-area");
    const fileInput = document.getElementById("id_image");
    const preview = document.getElementById("preview");

    // Handle file validation and preview
    const handleFile = (file) => {
        if (!file.type.startsWith("image/")) {
            alert("Only image files (PNG, JPG, GIF, WebP) are allowed.");
            return;
        }
        if (file.size > 10 * 1024 * 1024) {
            alert("File size exceeds 10MB limit.");
            return;
        }

        // Clear previous preview and display selected image
        preview.innerHTML = "";
        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.style.maxWidth = "200px";
        img.style.marginTop = "10px";
        preview.appendChild(img);
    };

    // Handle image selection from file input
    fileInput?.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Highlight drop area on dragover
    dropArea?.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropArea.style.borderColor = "blue";
    });

    // Reset drop area style when dragging leaves
    dropArea?.addEventListener("dragleave", () => {
        dropArea.style.borderColor = "#ccc";
    });

    dropArea?.addEventListener("drop", (e) => {
        e.preventDefault();
        dropArea.style.borderColor = "#ccc";
        if (e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            fileInput.files = e.dataTransfer.files; // Sync with file input
            handleFile(file);
        }
    });
});
