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
        alert("Insert successful"); // Show a success message
        console.log(data); // Log server response for debugging
    })
    .catch(error => {
        console.error("There was an error with the submission:", error);
        alert("There was an error with the submission. Please try again.");
    });
});
