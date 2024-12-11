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
  