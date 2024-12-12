<<<<<<< HEAD
document.querySelectorAll('.delete-link').forEach(button => {
  button.addEventListener('click', function(e) {
    e.preventDefault()

    let nomEle = this.closest('tr').querySelector("td#nomEle").textContent;

    Swal.fire({
      title: `Está seguro de eliminar el elemento: ${nomEle}`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí, Eliminar!"
    }).then((result) => {
      if (result.isConfirmed) {
        const row = this.closest('tr'); // Find the closest row of the element
        const deleteUrl = this.getAttribute('href'); // Get the URL for deletion

        fetch(deleteUrl, { method: 'DELETE' }) 
          .then(response => {
            if (response.ok) {
              row.remove(); // Remove the row dynamically if successful
              Swal.fire({
                title: "Eliminado!",
                text: "El elemento ha sido eliminado.",
                icon: "success"
              });
            } else {
              Swal.fire({
                title: "Error!",
                text: "Hubo un error al eliminarlo.",
                icon: "error"
              });
            }
          })
          .catch(error => {
            console.error('Error:', error); // Log errors
            Swal.fire({
              title: "Error!",
              text: "Hubo un error al eliminar el elemento.",
              icon: "error"
            });
          });
      }
    });
  });
});
=======
document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const row = this.closest('tr');
      const deleteUrl = this.getAttribute('href');
  
      fetch(deleteUrl, { method: 'DELETE' })
        .then(response => {
          if (response.ok) {
            row.remove(); // Remove the row dynamically
          } else {
            alert('Failed to delete the element.');
          }
        })
        .catch(error => console.error('Error:', error));
    });
  });
  
>>>>>>> 9f1feabfb61519029df5a09752a7aab256ef7b25
