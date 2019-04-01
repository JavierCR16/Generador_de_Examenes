function procesarAjaxSubtemas(tema,idObjHTML){
    $.ajax({

        url: "/filtrarSubtemas",
        type: 'post',
        data:JSON.stringify({informacion:tema}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            var select =  $("#"+idObjHTML);

            select.find('option').remove();
            select.append($('<option>',{text: "Escoger Subtema"}));
            for(i = 0; i< datos["subtemas"].length; i++){

                var subtema = datos["subtemas"][i]["id"]+"-"+datos["subtemas"][i]["subtema"];
                  select.append($('<option>',{text: subtema}));
            }
        }
    })
}

function procesarAjaxItems(subtema,tipoFiltrado,idObjSelect,idPopDescripcion){
    $.ajax({

        url: "/filtrarItems",
        type: 'post',
        data:JSON.stringify({informacionSubtema:subtema,tipo:tipoFiltrado}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {

            var select =  $("#"+idObjSelect);
            var ojo = $("#"+idPopDescripcion);

            ojo.attr("onclick","desplegarDescripcion(" +datos["descripcionItems"]+ ","+JSON.stringify(idObjSelect)+ ")");
            select.find('option').remove();
            select.append($('<option>',{text: "Escoger Item"}));
            for(i = 0; i< datos["items"].length; i++){
                var item = datos["items"][i]["idLargo"]+"/Item"+datos["items"][i]["id"];
                  select.append($('<option>',{text: item}));
            }
        }
    })
}

function procesarAjaxIndice(idItemSecreto,nuevoIndice, idSub,valorBoton,descripItems) {
    $.ajax({
        url: "/cambioIndiceDiscriminacion",
        type: 'post',
        data:JSON.stringify({idItem:idItemSecreto,newIndex:nuevoIndice, botonPresionadoIndice:valorBoton,idSubtema: idSub}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",
        success: function (datos) {

            var tabla =  $("#tablaDiscriminacion tbody");
            tabla.find('tr').remove();

            for(i= 0;i< datos["items"].length;i++){
                var identificador = datos["items"][i]["idLargo"]+"/Item"+datos["items"][i]["id"];
                var tipo = datos["items"][i]["tipo"];
                var puntaje = datos["items"][i]["puntaje"];
                var indice = datos["items"][i]["indiceDiscriminacion"];
                var idSubtema = datos["items"][i]["idSubtema"];
                var boton = $('<button class="consult-button" onclick="verificarIndiceDiscriminacion(this,\''+ descripItems + '\' )"><i class="material-icons" style="font-size: 20px;">info</i> </button>');


                tabla.append($('<tr>')
                        .append($('<td>').append(identificador))
                        .append($('<td>').append(tipo))
                        .append($('<td>').append(puntaje))
                        .append($('<td>').append(indice))
                        .append($('<td hidden>').append(idSubtema))
                        .append($('<td>').append(boton))
                );
            }
        }
    })
}

function procesarAjaxItemModificar(itemSeleccionado){
    var tiposSelected = $('[name = "tiposItemModificar"]');
    var descripcion = $("#descItemMod");
    var puntaje = $("#puntajeMod");

    $.ajax({

        url: "/extraerInformacionItem",
        type: 'post',
        data:JSON.stringify({item:itemSeleccionado}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            descripcion.val(datos["informacionItem"]["descripcion"]);
            puntaje.val(datos["informacionItem"]["puntaje"]);

            for(i =0; i<tiposSelected.length;i++){
                if(tiposSelected[i].value===datos["informacionItem"]["tipo"])
                    tiposSelected[i].checked = true
            }

        }
    })
}

function procesarAjaxRespuestasViejas(itemSeleccionado){
    var radioRespuestas = $('[name = "Mrespuesta"]');
    var listaRespuestas = [$('#Mrespuesta1'),$('#Mrespuesta2'),$('#Mrespuesta3'),$('#Mrespuesta4')];

    $.ajax({

        url: "/extraerRespuestasItem",
        type: 'post',
        data:JSON.stringify({item:itemSeleccionado}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            if(datos["informacionItem"]["respuestas"].length !==0) {

                for (i = 0; i < radioRespuestas.length; i++) {
                    if (radioRespuestas[i].value === datos["informacionItem"]["respCorrecta"]) {
                        radioRespuestas[i].checked = true;
                    }
                    listaRespuestas[i].val(datos["informacionItem"]["respuestas"][i]);
                }
                $("#respuestasModificar").removeAttr('hidden');
            }
        }
    })
}

function procesarAjaxEncabezado(curso,escuela,periodo,fecha,tiempo,tipo,instrucciones){
    $.ajax({

        url: "/previewEncabezado",
        type: 'post',
        data:JSON.stringify({curso:curso,escuela:escuela,periodo:periodo,fecha:fecha,tiempo:tiempo,tipo:tipo,
        instrucciones:instrucciones}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            var bodyModalPreview = $("#previewEncabezadoModal");
            bodyModalPreview.find('img').remove();

            //TODO Cambiar nombre de imagen de forma dinamica por si hay varios usuarios conectados haciendo previews.
            bodyModalPreview.append("<img class=\"img-responsive\" src=\"/static/preview.png\" alt=\"Previsualización\"  style=\"border-color: black;width: 100%\">");

            var modalPreview = $("#previsualizationModal");

            modalPreview.modal({
                show:true
            });
        }
    })
}

function obtenerSubtemas(selectEscogido, idObjHTML){

    var temaEscogido = selectEscogido.options[selectEscogido.selectedIndex].text;

    procesarAjaxSubtemas(temaEscogido, idObjHTML)
}

function obtenerItems(selectEscogido,tipoFiltrado ,idObjSelect,idPopDescripcion){

    var subtemaEscogido = selectEscogido.options[selectEscogido.selectedIndex].text;

    procesarAjaxItems(subtemaEscogido,tipoFiltrado,idObjSelect,idPopDescripcion)

}

function cargarDatosModificar(selectItem){

    var itemSeleccionado = selectItem.options[selectItem.selectedIndex].text;

    procesarAjaxItemModificar(itemSeleccionado)

}

function cargarRespuestasModificar(selectItem){
    var itemSeleccionado = selectItem.options[selectItem.selectedIndex].text;

    procesarAjaxRespuestasViejas(itemSeleccionado)
}

function agregarIndiceDiscriminacion(descripItems) {
    var idItemSecreto = $('#idItemSecretoAdd').val();

    var nuevoIndice = $('#addIndice').val();

    var valorBoton = $('#agregarIndiceBoton').val();

    var idSubtema = $('#idSubtemaSecretAdd').val();

    procesarAjaxIndice(idItemSecreto,nuevoIndice,idSubtema,valorBoton,descripItems);

    closeFormAdd()
}

function modificarEliminarIndiceDiscriminacion(valorBoton,descripItems) {

    var idItemSecreto = $('#idItemSecretoMod').val();

    var nuevoIndice = $('#modIndice').val();

    var idSubtema = $('#idSubtemaSecretMod').val();

    procesarAjaxIndice(idItemSecreto,nuevoIndice,idSubtema,valorBoton,descripItems);

    closeFormModDel()
}

function verificarIndiceDiscriminacion(botonClickeado,descripItems){
    descripItems = !(descripItems instanceof Array) ? descripItems.split(",") : descripItems;

    var indice = $(botonClickeado).closest('tr').index();
    var filaTablaDiscriminacion = $("#tablaDiscriminacion tr").eq(indice+1).find('td');
    var valorDiscriminacion = filaTablaDiscriminacion.eq(3).text();
    var descripcion = descripItems[indice];
    var identificador = filaTablaDiscriminacion.eq(0).text();
    var idSubtema = filaTablaDiscriminacion.eq(4).text();
    var idItem = identificador.split("/Item")[1] ;

    valorDiscriminacion === "None" || valorDiscriminacion === "" ? openFormAdd(descripcion,idItem,idSubtema)
        : openFormModDel(descripcion,valorDiscriminacion,idItem,idSubtema)

}

function openFormAdd(descripcion,idItem,idSubtema) {

    $("#infoItemAgregar").text(descripcion);
    $('#idItemSecretoAdd').val(idItem);
    $('#idSubtemaSecretAdd').val(idSubtema);

    document.getElementById("agregarIndice").style.display = "block";
}

function closeFormAdd() {document.getElementById("agregarIndice").style.display = "none";}

function openFormModDel(descripcion,indiceDisc,idItem,idSubtema) {

    $("#infoItemModificar").text(descripcion)
    $('#modIndice').val(indiceDisc);
    $('#idItemSecretoMod').val(idItem);
    $('#idSubtemaSecretMod').val(idSubtema);

    document.getElementById("modiEliIndice").style.display = "block";
}

function closeFormModDel() {document.getElementById("modiEliIndice").style.display = "none";}

function desplegarDescripcion(descripcionesItems,selectItem) {

            var select = document.getElementById(selectItem);

            if(select !== undefined && select.selectedIndex !== 0) {
                var indice = select.selectedIndex -1;
                var modalItem = $("#modalItem");

                modalItem.modal({
                    show: true
                });
                $("#descripcionModal").text(descripcionesItems[indice]);
            }
        }

function previewEncabezado() {

    var curso = "Probabilidades";  //LUEGO INCLUIR UN SELECT CON CURSOS
    var escuela = "Escuela de Matemáticas";  //LUEGO INCLUIR UN SELECT CON ESCUELAS

    var periodoDOM = document.getElementById("selectPeriodo")
    var periodo = periodoDOM.options[periodoDOM.selectedIndex].text;

    var fecha = $("#fechaEncabezado").val();
    var tiempo = $("#tiempoEncabezado").val();

    var tipoDOM = document.getElementById("selectTipo");
    var tipo = tipoDOM.options[tipoDOM.selectedIndex].text;

    var instrucciones = $("#instruccionesEncabezado").val();

    procesarAjaxEncabezado(curso, escuela, periodo, fecha, tiempo,tipo, instrucciones);

}
