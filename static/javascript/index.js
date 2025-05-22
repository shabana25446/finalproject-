document.addEventListener("DOMContentLoaded", function () {
    const searchBar = document.getElementById("searchBar");
    const filterDropdown = document.getElementById("filterDropdown");
    const packageCards = document.querySelectorAll(".package-card");

    // Live Search by Destination
    searchBar.addEventListener("input", function () {
        const searchValue = searchBar.value.toLowerCase();

        packageCards.forEach(card => {
            const location = card.getAttribute("data-location").toLowerCase();
            card.style.display = location.includes(searchValue) ? "block" : "none";
        });
    });

    // Real-time Filtering
    filterDropdown.addEventListener("change", function () {
        const filterValue = filterDropdown.value;
        const sections = document.querySelectorAll(".package-section");

        sections.forEach(section => {
            if (filterValue === "all" || section.getAttribute("data-category") === filterValue) {
                section.style.display = "block";
            } else {
                section.style.display = "none";
            }
        });
    });
});
