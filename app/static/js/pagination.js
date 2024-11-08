document.addEventListener("DOMContentLoaded", function() {
    let currentPage = 1;
    let recordsPerPage = 10;

    function fetchRecords() {
        fetch(`/get_records?page=${currentPage}&per_page=${recordsPerPage}`)
            .then(response => response.json())
            .then(data => {
                const outputBox = document.getElementById("output-box");
                outputBox.innerHTML = ""; // Clear existing records
                data.forEach(record => {
                    const newElement = document.createElement("p");
                    newElement.textContent = record;
                    outputBox.appendChild(newElement);
                });
            });
    }

    document.getElementById("next-page").addEventListener("click", function() {
        currentPage++;
        fetchRecords();
    });

    document.getElementById("prev-page").addEventListener("click", function() {
        if (currentPage > 1) {
            currentPage--;
            fetchRecords();
        }
    });

    document.getElementById("records-per-page").addEventListener("change", function() {
        recordsPerPage = parseInt(this.value);
        currentPage = 1; // Reset to first page
        fetchRecords();
    });

    // Initial fetch
    fetchRecords();
});
