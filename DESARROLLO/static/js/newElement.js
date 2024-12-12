<<<<<<< HEAD
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
=======
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
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok " + response.statusText);
        }
        return response.text(); // Or `response.json()` if the server sends JSON
    })
    .then(data => {
        window.location.href = "/alertas"; // Redirect to the alertas page after insert
    })
    .catch(error => {
        console.error("There was an error with the submission:", error);
        alert("There was an error with the submission. Please try again.");
    });
});
>>>>>>> 9f1feabfb61519029df5a09752a7aab256ef7b25
