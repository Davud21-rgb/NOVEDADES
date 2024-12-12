let carga_masiva = document.querySelector("#carga_masiva");
carga_masiva.addEventListener("click", (event) => {
    event.preventDefault();

    const form = carga_masiva.closest('form');
    const formData = new FormData(form);

    // Send the form data using fetch
    fetch("http://localhost:8000/massive/load", {
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
})