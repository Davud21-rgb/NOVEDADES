let newElement = document.querySelector("#newElement");
newElement.addEventListener("click", (event) => {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const form = newElement.closest('form');
    const formData = new FormData(form);

    // Send the form data using fetch
    fetch("http://localhost:8000/i/e", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
        if (data.status_code === 200) {
            // Redirect to alertas with the success message
            window.location.href = `/alertas?msgito=${encodeURIComponent(data.message)}&regreso=/ele`;
        } else {
            // Handle error: redirect to alertas with the error message
            window.location.href = `/alertas?msgito=${encodeURIComponent(data.message)}&regreso=/ele`;
        }
    })
    .catch(error => {
        console.error("There was an error with the submission:", error);
        alert("There was an error with the submission. Please try again.");
    });
});
