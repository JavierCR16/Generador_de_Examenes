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
                var boton = $('<button class="consult-button" onclick="verificarIndiceDiscriminacion(this,\''+ descripItems + '\' )"><i class="material-icons" style="font-size:20px;">info</i></button>');


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
            console.log(datos);
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

                    if (radioRespuestas[i].value === datos["informacionItem"]["respCorrecta"].toString()) {
                        radioRespuestas[i].checked = true;
                    }
                    listaRespuestas[i].val(datos["informacionItem"]["respuestas"][i]);
                }
                $("#respuestasModificar").removeAttr('hidden');
            }
            else
                $("#respuestasModificar").attr("hidden",true);
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
            console.log(datos);
            var bodyModalPreview = $("#previewEncabezadoModal");
            bodyModalPreview.find('img').remove();

            bodyModalPreview.append("<img id=\"imagenPreview\" class=\"img-responsive\" alt=\"Previsualización\"  style=\"border-color: black;width: 100%\">");
            $("#imagenPreview").attr("src","/static/" +datos["imagen"]);

            var modalPreview = $("#previsualizationModal");

            modalPreview.modal({
                show:true
            });
        }
    })
}

function procesarAjaxSugerencias(nuevaEdicion,comentarios,idItem){

    $.ajax({

        url: "/enviarSugerencia",
        type: 'post',
        data:JSON.stringify({nuevaEdicion:nuevaEdicion,comentarios:comentarios,idItem:idItem}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            console.log(datos["status"]);
            $("#modalSugerencia").modal('hide');
        }
    })

}

function procesarAjaxVerificarEdiciones(accion,idSugerencia,sugerencia,idItem){
    $.ajax({

        url: "/aprobarRechazarSugerencia",
        type: 'post',
        data:JSON.stringify({accion:accion,idSugerencia:idSugerencia,sugerencia:sugerencia,idItem:idItem}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            console.log(datos["status"]);
            $("#modalVerificacion").modal('hide');
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
    console.log(descripItems);
    descripItems = !(descripItems instanceof Array) ? descripItems.split(",") : descripItems;
    console.log(descripItems);

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

    $("#modalAgregarIndice").modal({show : true});
}

function closeFormAdd() {$("#modalAgregarIndice").modal('hide');}

function openFormModDel(descripcion,indiceDisc,idItem,idSubtema) {

    $("#infoItemModificar").text(descripcion);
    $('#modIndice').val(indiceDisc);
    $('#idItemSecretoMod').val(idItem);
    $('#idSubtemaSecretMod').val(idSubtema);

    $("#modalModificarIndice").modal({show: true});
}

function closeFormModDel() {$("#modalModificarIndice").modal('hide');}

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

    var periodoDOM = document.getElementById("selectPeriodo");
    var periodo = periodoDOM.options[periodoDOM.selectedIndex].text;

    var fecha = $("#fechaEncabezado").val();
    var tiempo = $("#tiempoEncabezado").val();

    var tipoDOM = document.getElementById("selectTipo");
    var tipo = tipoDOM.options[tipoDOM.selectedIndex].text;

    var instrucciones = $("#instruccionesEncabezado").val();

    procesarAjaxEncabezado(curso, escuela, periodo, fecha, tiempo,tipo, instrucciones);

}

function desplegarModalSugerencia(botonClickeado, descripcionItems){
    var indice = $(botonClickeado).closest('tr').index();
    var filaTabla = $("#tablaSugerencia tr").eq(indice+1).find('td');
    var idItem = filaTabla.eq(0).text().split("/Item")[1];


    $("#descModalSugerencia").text("Descripción Actual: "+ descripcionItems[indice]);

    $("#botonModalSugerencia").attr("onclick","enviarSugerencia("+idItem+")");

    $("#modalSugerencia").modal({
       show:true
    });

}

function desplegarModalVerificar(botonClickeado,descripcionItem,sugerencia,comentarios){
    var indice = $(botonClickeado).closest('tr').index();
    var filaTabla = $("#tablaVerificaciones tr").eq(indice+1).find('td');
    var idSugerencia = filaTabla.eq(0).text();
    var idItem = filaTabla.eq(1).text().split("/Item")[1];

    $("#descModalVerificacion").text("DESCRIPCIÓN: "+descripcionItem[indice]);

    $("#sugerenciaEdicion").val(sugerencia[indice]);

    $("#comentarios").val(comentarios[indice]);

    $("#botonModalAprobar").attr("onclick","aprobacionSugerencia(1, "+idSugerencia+", "+JSON.stringify(sugerencia[indice])+", "+ idItem+")");
    $("#botonModalRechazar").attr("onclick","aprobacionSugerencia(2, "+idSugerencia+")");

    $("#modalVerificacion").modal({
       show:true
    });
}

function desplegarModalEncabezados(dict_encabezados){
    var indexEncabezado = $("#selectEncabezados").prop('selectedIndex');

    if(indexEncabezado !== 0){
       var curso = dict_encabezados[indexEncabezado -1]["curso"];
       var escuela = dict_encabezados[indexEncabezado -1]["escuela"];
       var periodo = dict_encabezados[indexEncabezado -1]["idPeriodo"];
       var fecha = dict_encabezados[indexEncabezado -1]["anno"];
       var tiempo = dict_encabezados[indexEncabezado -1]["tiempo"];
       var tipo = dict_encabezados[indexEncabezado -1]["idTipoExamen"];
       var instrucciones = dict_encabezados[indexEncabezado -1]["instrucciones"];

       procesarAjaxEncabezado(curso,escuela,periodo,fecha,tiempo,tipo,instrucciones);
    }


}

function enviarSugerencia(idItem){

    var nuevaEdicion = $("#sugerenciaEdicion").val();

    var comentarios = $("#comentarios").val();

    procesarAjaxSugerencias(nuevaEdicion,comentarios,idItem)
}

function aprobacionSugerencia(accion,idSugerencia,sugerencia = null,idItem = null){procesarAjaxVerificarEdiciones(accion,idSugerencia,sugerencia,idItem);}

function descripcionItemsExamen(descripciones,index){

    $("#descripcionModalExamen").text(descripciones[index]);

    $("#modalItemExamen").modal({
       show:true
    });

}

function OcultAcordion(id) {
        var x = document.getElementById(id);
        if (x.className.indexOf("w3-show") === -1) {
            x.className += " w3-show";
        } else {
            x.className = x.className.replace(" w3-show", "");
        }
}

function openNav() {
      document.getElementById("mySidenav").style.width = "100%";
}

function closeNav() {
      document.getElementById("mySidenav").style.width = "0";
}

function mostrarAddRespuestas(selectItems){

    var item = $(selectItems).children("option:selected").val();
    var tipo = item.split("/Item")[0];
    tipo = tipo.split("-")[2];

    if(tipo === "S" || tipo ==="PS") {
        $("#respAddSelect").removeAttr("hidden");
        $("#respAddDesarrollo").attr("hidden",true);
    }
    else {
        $("#respAddDesarrollo").removeAttr("hidden");
        $("#respAddSelect").attr("hidden",true);
    }

    $("#botonAddResp").removeAttr("hidden")

}


