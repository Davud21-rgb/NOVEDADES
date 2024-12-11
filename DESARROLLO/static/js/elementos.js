function Ir(paso, idEQUIPAMIENTO) {
    let formulario = document.getElementById('mio_' + idEQUIPAMIENTO);
    let respuestaField = document.getElementById('respuesta_' + idEQUIPAMIENTO);
    
    if (paso === 1) {
        let respuesta = respuestaField.value;
        if (respuesta.length > 0) {
            respuestaField.value = respuesta;
            formulario.setAttribute('action', '/n/i');
            formulario.submit();
        } else {
            respuestaField.value = "ELEMENTO EDITADO CORRECTAMENTE [EDITADO]";
            formulario.setAttribute('action', '/n/i');
            formulario.submit();
        }
    } 
    
    if (paso === 2) {
        let respuesta = respuestaField.value;
        if (respuesta.length > 0) {
            respuestaField.value = respuesta;
            formulario.setAttribute('action', '/n/d');
            formulario.submit();
        } else {
            respuestaField.value = "NOVEDAD CERRADA POR EL CUENTADANTE [CERRADA]";
            formulario.setAttribute('action', '/n/d');
            formulario.submit();
        }
    }
}
