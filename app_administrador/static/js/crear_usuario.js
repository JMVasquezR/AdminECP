$(document).ready(function () {
    let formulario = $('#form-crear-cliente')

    // Definimos la funcion que se encarga de seleccionar el genero que le corresponde a la nana
    function setGenero() {
        $("#genero option[value=" + formulario.data('genero') + "]").attr('selected', 'selected');
    }

    // Pintamos el select de tipo de documento
    $.ajax({
        url: formulario.data('url-tipo-documento'),
        type: "GET",
        success: function (data) {
            dibujarSelectConDataRest(data, 'id', 'nombre_corto', 'tipo_documento')
        },
        error: function (result) {
            console.log(result)
        }
    });

    // Pintamos el select de generos
    $.ajax({
        url: formulario.data('url-genero'),
        type: "GET",
        success: function (data) {
            dibujarSelectConDataRest(data, 'id', 'nombre', 'genero')
            setGenero()
        },
        error: function (result) {
            console.log(result)
        }
    });

    // Enviamos el formulario por Ajax
    formulario.on('submit', (function (e) {

            e.preventDefault() // No permite enviar el formulario

            formData = new FormData(this);

            $.ajax({
                type: "POST",
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                },
                url: formulario.data('url'),
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    console.log(data)
                },
                error: function (result) {
                    console.log(result)

                }

            });
        }
    ));
});