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
})