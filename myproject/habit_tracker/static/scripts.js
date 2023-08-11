document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById('messageModal');
    var span = document.getElementsByClassName("close-button")[0];

    if (modal && span) {
        // Display the modal
        modal.style.display = "block";

        // Close the modal
        span.onclick = function() {
            modal.style.display = "none";
        }

        // Close the modal if clicked outside
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    }
});

