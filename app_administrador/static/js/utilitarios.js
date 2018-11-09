function dibujarSelectConDataRest(data, valor, nombre, select_id) {
    var html = $('#' + select_id).html()
    if (html == '') {
        var html = '<option value="" selected>Escoge una opcion</option>'
    }
    for (var i in data) {
        if ($(html).attr('value') != data[i][valor]) {
            html += '<option value=' + data[i][valor] + '>' + data[i][nombre] + '</option>'
        }

    }
    $('#' + select_id).html(html)
}

$(document).on("keypress", "form", function (event) { // Deshabilita el enter
    return event.keyCode != 13;
});