function Ir(paso, idNovedades) {
    let formulario = document.getElementById('mio_' + idNovedades);
    let respuestaField = document.getElementById('respuesta_' + idNovedades);
    
    if (paso === 1) {
        let respuesta = respuestaField.value;
        if (respuesta.length > 0) {
            respuestaField.value = respuesta;
            formulario.setAttribute('action', '/n/i');
            formulario.submit();
        } else {
            respuestaField.value = "NOVEDAD PROCESADA POR EL CUENTADANTE [PROCESO]";
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
