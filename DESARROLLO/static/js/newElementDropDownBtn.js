// Function to update 'nombre' dropdown based on selected 'idTIPOELEMENTO'
function updateNombreDropdown(selectedTipoElemento) {
    const nombreDropdown = document.getElementById('nombre');
    nombreDropdown.innerHTML = '';  // Clear current options

    // Get all the options in the 'idTIPOELEMENTO' dropdown
    const options = document.querySelectorAll('#idTIPOELEMENTO option');

    options.forEach(option => {
        if (option.value === selectedTipoElemento) {
            const nomTipo = option.getAttribute('data-nomtipo');  // Get the associated 'NOMTIPO'

            const newOption = document.createElement('option');
            newOption.value = nomTipo;
            newOption.textContent = nomTipo;

            nombreDropdown.appendChild(newOption);
        }
    });

    if (nombreDropdown.options.length === 0) {
        const defaultOption = document.createElement('option');
        defaultOption.textContent = 'No Hay Elementos Disponibles';
        nombreDropdown.appendChild(defaultOption);
    }
}

// Set up event listener for when the 'idTIPOELEMENTO' dropdown changes
document.getElementById('idTIPOELEMENTO').addEventListener('change', function() {
    const selectedValue = this.value;  // Get the selected value
    updateNombreDropdown(selectedValue);  // Update the 'nombre' dropdown based on the selected value
});

// Optionally, trigger the function to populate the 'nombre' dropdown on page load
document.addEventListener('DOMContentLoaded', function() {
    const initialTipoElemento = document.getElementById('idTIPOELEMENTO').value;
    if (initialTipoElemento) {
        updateNombreDropdown(initialTipoElemento);  // Populate 'nombre' dropdown based on the initial value
    }
});
