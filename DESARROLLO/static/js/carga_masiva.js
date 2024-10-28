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
})