function openModal(imageUrl) {
    document.getElementById("modalImage").src = imageUrl;
    document.getElementById("imageModal").style.display = "block";
}
function closeModal() {
    document.getElementById("imageModal").style.display = "none";
}