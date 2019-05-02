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

function procesarAjaxItems(subtema,tipoFiltrado,idObjSelect,idPopDescripcion,url){
    $.ajax({

        url: url,
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
                var boton = $('<button class="iconB"><i class="fas fa-info-circle"></i></button>').attr(
                    "onclick","verificarIndiceDiscriminacion(this," + JSON.stringify(descripItems) +")"
                );


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

            $("#divModificarItem").removeAttr('hidden');

        }
    })
}

function procesarAjaxRespuestasViejas(itemSeleccionado,tipoItem){
    var radioRespuestas = $('[name = "Mrespuesta"]');
    var listaRespuestas = [$('#Mrespuesta1'),$('#Mrespuesta2'),$('#Mrespuesta3'),$('#Mrespuesta4')];
    var respuestaDesarrollo = $("#respModDesarrollo");
    var divModificarSel = $("#divrespModSelect");
    var divModificarDes = $("#divrespModDesarrollo");
    var botonModResp = $("#botonModResp");

    $.ajax({

        url: "/extraerRespuestasItem",
        type: 'post',
        data:JSON.stringify({item:itemSeleccionado}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            if(tipoItem === "S" || tipoItem === "PS") {
                for (i = 0; i < datos["informacionItem"]["respuestas"].length; i++) {

                    if (radioRespuestas[i].value === datos["informacionItem"]["respCorrecta"].toString()) {
                        radioRespuestas[i].checked = true;
                    }
                    listaRespuestas[i].val(datos["informacionItem"]["respuestas"][i]);
                }
                divModificarSel.removeAttr('hidden');
                divModificarDes.attr('hidden', true);
            }
            else {
                respuestaDesarrollo.val(datos["informacionItem"]["respuestas"][0]);
                divModificarDes.removeAttr('hidden');
                divModificarSel.attr('hidden', true);
            }
                botonModResp.removeAttr('hidden');
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

            bodyModalPreview.append("<img id=\"imagenPreview\" class=\"img-responsive\" alt=\"Previsualización\"  style=\"border-color: black;width: 100%\">");
            $("#imagenPreview").attr("src","/static/" +datos["imagen"]);

            var modalPreview = $("#previsualizationModal");

            modalPreview.modal({
                show:true
            });
        }
    })
}

function procesarAjaxJuego(codigo){

     $.ajax({

        url: "/guardarJuego",
        type: 'post',
        data:JSON.stringify({codigo:codigo}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {

            $("#modalSesionJuego").modal({
                show: true
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
            $("#modalVerificacion").modal('hide');
            window.location.href = "/VerificacionEdicion"
        }
    })
}

function procesarAjaxInformacionExamen(tipoExamen, funcion = null){
    $.ajax({

        url: "/loadInformacionExamen",
        type: 'post',
        data:JSON.stringify({tipoExamen:tipoExamen}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            var indexItem = 0;
            var cantItems = 0;
            var tagPadre = $("#allfather");

            tagPadre.empty();
            for(var i =0; i< datos["temas"].length;i++){

                var l1Tema = "<li></li>";
                var inputTemas = $("<input type=\"checkbox\" >").attr("onclick","OcultAcordion(" +JSON.stringify("subtemas"+i) +")");
                var labelTemas = "<label for=\"tall\" class=\"custom-unchecked\">"+datos["temas"][i]["tema"]+"</label>";
                var divTemas = $("<div class = \"w3-container w3-hide\"></div>").attr("id","subtemas"+i).append("<ul></ul>");

                for(var j =0; j< datos["subtemas"][i].length;j++){
                    var subtemaActual = datos["subtemas"][i][j];

                    var l1Subtema = "<li></li>";
                    var inputSubtemas = $("<input type=\"checkbox\" name = \"tall\" >").attr("onclick","OcultAcordion("+ JSON.stringify("items" +i +"-"+j)+")");

                    var labelSubtemas = "<label for=\"tall\" class=\"custom-unchecked\">"+subtemaActual["subtema"]+"</label>";
                    var divSubtemas = $("<div class = \"w3-container w3-hide\"></div>").attr("id","items"+i+"-"+j).append("<ul></ul>");

                    for(var w = 0; w < datos["items"][indexItem].length; w++){
                        var itemActual = datos["items"][indexItem][w];

                        var l1Item = "<li></li>";
                        var inputItems = $("<input type=\"checkbox\" name='items'>").attr("value",datos["descripcionItems"][cantItems]+","+
                            itemActual["id"] + ","+ itemActual["puntaje"]);
                        var labelItems = "<label for=\"tall\" class=\"custom-unchecked\">"+itemActual["idLargo"] + "/Item"+ itemActual["id"]+ "</label>";

                        var ojo = $("<i id=\"descripcionDesplegar\" class=\"fa fa-eye eyeI\"></i>").attr("onclick","descripcionItemsExamen(" + JSON.stringify(datos["descripcionItems"]) +","+ cantItems+")");
                        divSubtemas.find("ul:last").append($(l1Item).append(inputItems).append(labelItems).append(ojo));

                        cantItems+=1;
                    }

                    indexItem +=1;
                    l1Subtema = $(l1Subtema).append(inputSubtemas).append(labelSubtemas).append(divSubtemas);
                    divTemas.find("ul:first").append(l1Subtema);

                }
                l1Tema = $(l1Tema).append(inputTemas).append(labelTemas).append(divTemas);
                tagPadre.append(l1Tema)
            }

            if(funcion !== null)
                funcion()
        }
    })
}

function procesarAjaxGenerarExamen(encabezado,tipoExamen,conSolucion,itemsSeleccionados){

    $.ajax({

        url: "/generarExamen",
        type: 'post',
        data:JSON.stringify({encabezado:encabezado,tipoExamen:tipoExamen,solucionado:conSolucion,items:itemsSeleccionados}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            var codigo = "";

            if(datos["success"]){
                var retVal = confirm("¿Desea descargar el examen en formato PDF? De igual forma puede descargarlo en la sección de Filtrado de Exámenes");
                if( retVal === true ) { //../static/
                    $("#secretDownload").attr("href","../static/"+datos["archivoPDF"])[0].click();
                }

                while(true) {
                    codigo = prompt("Ingrese un código de 9 caracteres si desea publicar el examen para obtener retroalimentación por parte de los estudiantes.");
                    if (codigo === null) {
                        window.location.href = "/CreacionExamen";
                        break;
                    }
                    else if (codigo.length === 9) {
                        procesarAjaxPublicarExamen(codigo, datos["idExamen"]);
                        break;
                    }
                }
            }
        }
    })
}

function procesarAjaxPublicarExamen(codigo,idExamen){
    $.ajax({

        url: "/publicarExamenFeedback",
        type: 'post',
        data:JSON.stringify({codigo: codigo, idExamen: idExamen}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            if(datos["success"]){
                window.location.href = "/CreacionExamen"
            }
        }
    })
}

function procesarAjaxDescargarExamen(idExamen,botonDescargar){
    $.ajax({

        url: "/descargarExamen",
        type: 'post',
        data:JSON.stringify({idExamen:idExamen}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            if(datos["success"]){
                $(botonDescargar).removeAttr('onclick');
                $(botonDescargar).attr("href","../static/"+datos["nombreExamen"])[0].click();
                $(botonDescargar).attr("href","#").attr("onclick","descargarExamen(this);return false;")
            }
        }
    })
}

function procesarAjaxComentario(reaccion, codigoExamenComent, comentario){
    $.ajax({

        url: "/agregarComentario",
        type: 'post',
        data:JSON.stringify({codigoExamen: codigoExamenComent, comentario: comentario, reaccion: reaccion}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            if(datos["success"]){
                alert(datos["mensaje"]);
                window.location.reload();
            }
        }
    })
}

function procesarAjaxDatosComentarios(tipoFiltrado, examenID){
    $.ajax({

        url: "/filtrarComentariosFeedback",
        type: 'post',
        data: JSON.stringify({filtrado: tipoFiltrado, parametro: examenID}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            var emojis = ["😁", "🙂", "😶", "😕", "😭"];
            $("#tablaComentariosBody").children().remove();
            for (var i = 0; i < datos["comentarios"].length; i++) {
                var tupla = datos["comentarios"][i];

                $("#tablaComentariosBody").append($("<tr>").append($("<td>", {text: tupla[0]})).append($("<td>", {text: emojis[tupla[1]-1]})))
            }
        }
    })
}

function procesarAjaxGrafico(consulta, titulo, datos){

    $.ajax({
        url: "/obtenerDatosGraficos",
        type: 'post',
        data:JSON.stringify({consulta: consulta, datos: datos}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            if(datos["success"]){
                $("#containerChart").removeClass("w3-hide");
                google.charts.setOnLoadCallback(function () { drawChart(titulo, datos["estadisticas"]);});
            }
        }
    })
}

function procesarAjaxAgregarEquipo(codigo,nombreEquipo){
    $.ajax({
        url: "/JuegoLogIn",
        type: 'post',
        data:JSON.stringify({codigo: codigo, nombreEquipo: nombreEquipo}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            if(datos["success"]) {
                alert("Su equipo ha sido agregado con éxito");
                window.location.href = "/EstudiantesInicio";
            }
            else {
                alert("Código de juego incorrecto");
                window.location.reload();
            }
        }
    })
}

function procesarAjaxCalificar(equipo,puntaje){
    $.ajax({
        url: "/calificarEquipo",
        type: 'post',
        data: JSON.stringify({equipo: equipo, puntaje:puntaje}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            imprimirMensaje("Puntaje Actualizado Correctamente")
        }
    })
}

function ejecutarModalCalificar(datos,nuevoPuntaje){
     $("#selectEquipos").children().remove();

     $("#selectEquipos").append($("<option>",{
         text:"Escoger Equipo"
     }));

    for(var i =0; i< datos["equipos"].length;i++){

        $("#selectEquipos").append($("<option>",{
            text: datos["equipos"][i][0] + "-" + datos["equipos"][i][1]
        }));
    }

    $("#botonCalificar").attr("onclick","calificar("+JSON.stringify(nuevoPuntaje)+")");

    $("#modalCalificar").modal({
        show:true
    })
}

function calificar(nuevoPuntaje){
    var equipoSeleccionado = $("#selectEquipos").val();

    if (equipoSeleccionado.trim() === "Escoger Equipo")
        imprimirMensaje("Debe seleccionar un equipo válido.");
    else
        procesarAjaxCalificar(equipoSeleccionado,nuevoPuntaje);

    $("#modalCalificar").modal("hide");

}


function procesarAjaxEquipos(puntaje) {

    $.ajax({
        url: "/obtenerEquipoPuntaje",
        type: 'post',
        dataType: "json",

        success: function (datos) {
            ejecutarModalCalificar(datos,puntaje)
        }
    })

}

function obtenerSubtemas(selectEscogido, idObjHTML){

    var temaEscogido = selectEscogido.options[selectEscogido.selectedIndex].text;

    procesarAjaxSubtemas(temaEscogido, idObjHTML)
}

function obtenerItems(selectEscogido,tipoFiltrado ,idSelectItems,idPopDescripcion){

    var subtemaEscogido = selectEscogido.options[selectEscogido.selectedIndex].text;

    procesarAjaxItems(subtemaEscogido,tipoFiltrado,idSelectItems,idPopDescripcion,"/filtrarItems")

}

function obtenerDatosComentarios(botonPresionado,examenID = -1){
    var tipoFiltrado = $(botonPresionado).val();

    if (tipoFiltrado === "cod"){
        examenID = $("#codigoExamenFeedback").val();
    }
    procesarAjaxDatosComentarios(tipoFiltrado, examenID);
}

function obtenerItemsRespuestas(selectEscogido, tipoFiltrado, idSelectItems, idPopDescripcion){

    var subtemaEscogido = selectEscogido.options[selectEscogido.selectedIndex].text;

    procesarAjaxItems(subtemaEscogido, tipoFiltrado, idSelectItems, idPopDescripcion, "/filtrarItemsRespuestas")


}

function cargarDatosModificar(selectItem){

    if(selectItem.selectedIndex !== 0) {

        var itemSeleccionado = selectItem.options[selectItem.selectedIndex].text;

        procesarAjaxItemModificar(itemSeleccionado)
    }
    else
        $("#divModificarItem").attr("hidden",true)

}

function cargarRespuestasModificar(selectItem){
    if(selectItem.selectedIndex!== 0) {
        var itemSeleccionado = selectItem.options[selectItem.selectedIndex].text;
        var tipoItem = itemSeleccionado.split("/Item")[0].split("-")[2];

        procesarAjaxRespuestasViejas(itemSeleccionado, tipoItem)
    }
    else{
        $("#divrespModSelect").attr("hidden", true);
        $("#divrespModDesarrollo").attr("hidden", true);
        $("#botonModResp").attr("hidden",true);
    }
}

function agregarIndiceDiscriminacion(descripItems) {
    var idItemSecreto = $('#idItemSecretoAdd').val();

    var nuevoIndice = $('#addIndice').val();

    var valorBoton = $('#agregarIndiceBoton').val();

    var idSubtema = $('#idSubtemaSecretAdd').val();

    if(nuevoIndice.trim() !== "" && !isNaN(nuevoIndice)) {

        procesarAjaxIndice(idItemSecreto, nuevoIndice, idSubtema, valorBoton, descripItems);

        closeFormAdd()
    }
    else
        imprimirMensaje("Debe ingresar un índice de discriminación válido.")
}

function modificarEliminarIndiceDiscriminacion(valorBoton,descripItems) {

    var idItemSecreto = $('#idItemSecretoMod').val();

    var nuevoIndice = $('#modIndice').val();

    var idSubtema = $('#idSubtemaSecretMod').val();

    if(valorBoton === "eliminarIndiceBoton" || (nuevoIndice.trim() !== "" && !isNaN(nuevoIndice))) {

        procesarAjaxIndice(idItemSecreto, nuevoIndice, idSubtema, valorBoton, descripItems);

        closeFormModDel()
    }
    else
        imprimirMensaje("Debe ingresar un índice de discriminación válido.")
}

function verificarIndiceDiscriminacion(botonClickeado,descripItems) {
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

    var curso = "Probabilidades";
    var escuela = "Escuela de Matemáticas";
    var periodo = $("#selectPeriodo").val();
    var fecha = $("#fechaEncabezado").val();

    var tiempoHoras = $("#tiempoEncabezadoHoras").val();
    var tiempoMin = $("#tiempoEncabezadoMinutos").val();
    var tiempo = tiempoHoras + ":" + tiempoMin;

    var tipo = $("#selectTipo").val();
    var instrucciones = $("#instruccionesEncabezado").val();

    if(validarEncabezado())
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

    if(nuevaEdicion.trim() === "" || comentarios.trim() === "")
        imprimirMensaje("Se debe ingresar una nueva descripción como sugerencia y comentarios respecto a dicha sugerencia");
    else
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

    var divRespAddSel = $("#divrespAddSelect");
    var divRespAddDes = $("#divrespAddDesarrollo");
    var botonAddResp = $("#botonAddResp");

    var item = $(selectItems).children("option:selected").val();
    var tipo = item.split("/Item")[0];
    tipo = tipo.split("-")[2];

    if(selectItems.selectedIndex !== 0) {

        if (tipo === "S" || tipo === "PS") {
            divRespAddSel.removeAttr("hidden");
            divRespAddDes.attr("hidden", true);
        } else {
            divRespAddDes.removeAttr("hidden");
            divRespAddSel.attr("hidden", true);
        }

        botonAddResp.removeAttr("hidden")
    }
    else{
        divRespAddDes.attr("hidden", true);
        divRespAddSel.attr("hidden", true);
        botonAddResp.attr("hidden", true);
    }

}

function loadInformacionExamen(){

    var tipoExamen = $("input[name='tipoExamen']:checked").val();

    procesarAjaxInformacionExamen(tipoExamen);

}

function ObtenerDatosdeEstadistica(selectItem) {

    if(itemValido(selectItem)) {
        var idEstadistica = $("#selectEstadisticas").children("option:selected").val().split("-")[0];

        var idItem = $("#selectItemEstadisticas").children("option:selected").val().split("/Item")[1];

        obtenerAjaxEstadisticasItems(idItem, idEstadistica)
    }
}

function obtenerAjaxEstadisticasItems(idItem,idEstadistica) {
    var mensajes = ["Cantidad de Veces Usado ","Semestres y Años en el que ha sido Utilizado","Total de Sugerencias de Edición Asociadas"];
    var index = parseFloat(idEstadistica) -1;
    $.ajax({
        url: "/ObtenerEstadisticas",
        type: 'post',
        data:JSON.stringify({idItem:idItem, idEstadistica:idEstadistica}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",
        success: function (datos) {
            var bodyModalEstadisticas = $("#vistaEstadisticas");

            bodyModalEstadisticas.children().remove();

            bodyModalEstadisticas.append($("<h3>", {
                        text: mensajes[index]
                    }
                ));

            if(idEstadistica !== "2") {

                bodyModalEstadisticas.append($("<h3>", {
                    text: datos["estadistica"]
                }));
            }

            else{

                bodyModalEstadisticas.append($("<table>").attr("id","tablaEstadistica").append($("<thead>").append($("<tr>").append($("<th>",{text:"Periodo"})).append($("<th>",{text:"Año"})))))
                $("#tablaEstadistica").append($("<tbody>").attr("id","tbodyEstadistica"));

                for(var i =0; i<datos["estadistica"].length;i++){
                    var tupla = datos["estadistica"][i];

                    $("#tbodyEstadistica").append($("<tr>").append($("<td>",{text: tupla[0]})).append($("<td>",{text: tupla[1]})))
                }
            }

             $("#estadisticasModal").modal({
                show:true
            });
        }
    })
}

function generarExamen(botonSeleccionado){

    var encabezado = $("#selectEncabezados").children("option:selected").val();

    var tipoExamen = $("input[name='tipoExamen']:checked").val();

    var conSolucion = $(botonSeleccionado).val();

    var itemsSeleccionados = [];

    $.each($("input[name='items']:checked"), function(){
        itemsSeleccionados.push($(this).val());
});

    if(encabezado === "Escoger Encabezado" || tipoExamen === undefined || itemsSeleccionados.length === 0)
        imprimirMensaje("Se debe escoger un encabezado válido, un tipo de examen y al menos un ítem de examen. Por favor intente de nuevo.");
    else
        procesarAjaxGenerarExamen(encabezado,tipoExamen,conSolucion,itemsSeleccionados);


}

function descargarExamen(botonDescargar){

    var indice = $(botonDescargar).parent().parent().index();
    var filaTablaExamenes = $("#tablaExamenes tr").eq(indice+1).find('td');
    var idExamen = filaTablaExamenes.eq(0).text();

    procesarAjaxDescargarExamen(idExamen,botonDescargar);

}

function guardarBorrador(){

    var encabezado = $("#selectEncabezados").children("option:selected").val();

    var tipoExamen = $("input[name='tipoExamen']:checked").val();

    var idItems = [];

    if(encabezado === "Escoger Encabezado" || tipoExamen === undefined)
        imprimirMensaje("Debe seleccionar un encabezado válido y un tipo de examen para poder generar un borrador de examen.");

    else
    {
        $.each($("input[name ='items']:checked"), function () {
            idItems.push($(this).val().split(",")[1])
        });

        var data = encabezado + "%" + tipoExamen + "%" + JSON.stringify(idItems);

        download("Borrador.exam", data)
    }

}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

function cargarBorrador(){

    var input = document.createElement('input');
    input.type = 'file';

    input.onchange = e => {

        // getting a hold of the file reference
        var file = e.target.files[0];

        // setting up the reader
        var reader = new FileReader();
        reader.readAsText(file); // this is reading as data url

        // here we tell the reader what to do when it's done reading...
        reader.onload = readerEvent => {
            var contenidoArchivo = readerEvent.target.result; // this is the content!

            estructurarExamen(contenidoArchivo)

        }

    };

input.click();

}

function estructurarExamen(contenido){

    var valorEncabezado = contenido.split("%")[0];
    var tipoExamen = contenido.split("%")[1];
    var listaIdItems = JSON.parse(contenido.split("%")[2]);

    procesarAjaxInformacionExamen(tipoExamen,function () {
        marcarExamen(valorEncabezado,tipoExamen,listaIdItems)
    });

}

function marcarExamen(valorEncabezado,tipoExamen,listaItems){

    $.each($("input[name = 'items']"),function () {
        for (var i = 0; i<listaItems.length; i++){
            if($(this).val().split(",")[1] === listaItems[i]) {
                $( this ).attr( 'checked', true );
                listaItems.splice(i,1);
                break;
            }
        }
    });

    $.each($("#selectEncabezados").children("option"),function () {
        if($(this).val() === valorEncabezado)
            $(this).attr('selected', true);
    });

    $.each($("input[name = 'tipoExamen']"),function () {

        if($(this).val() === tipoExamen)
            $(this).prop('checked', true);
    });


}

function mostrarSelectGraficos(selectEscogido){
    var graficoEscogido = selectEscogido.options[selectEscogido.selectedIndex].text;

    $("#divGraf-3").removeClass("w3-hide");
    $("#divGraf-3").addClass("w3-hide");
    $("#containerChart").removeClass("w3-hide");
    $("#containerChart").addClass("w3-hide");

    if (graficoEscogido === "3-Conteo de Reacciones en una Prueba"){
        $("#divGraf-3").removeClass("w3-hide");
    }
}

function drawChart(titulo, datos) {
    // Define the chart to be drawn.
    var data = google.visualization.arrayToDataTable(datos);

    var options = {title: titulo};

    // Instantiate and draw the chart.
    var chart = new google.visualization.ColumnChart(document.getElementById('containerChart'));
    chart.draw(data, options);
}

function graficar(selectEscogido){
    var select = $("#"+selectEscogido);

    if(select[0].selectedIndex!== 0){
        var id = select.val().split("-")[0];
        var graficoEscogido = select.val().split("-")[1];

        var datos = "";

        switch(graficoEscogido){
            case "Promedio de Índice de Discriminación":
                break;
            case "Conteo de Ítems por Tipo":
                break;
            case "Conteo de Reacciones en una Prueba":
                datos = $("#selectExamenesGrafico").val().split("-")[0];
                break;
        }
        if(isNaN(datos))
            imprimirMensaje("Debe seleccionar un exámen válido");
        else
            procesarAjaxGrafico(id, graficoEscogido, datos);
    }
    else
        imprimirMensaje("Seleccione una opción para graficar.")
}

function mostrarTiempo(selectEscogido){
    var tipoEscogido = selectEscogido.options[selectEscogido.selectedIndex].text;

    $("#tiempoJuego").removeClass("w3-hide");
    if (tipoEscogido === "1-Contrarreloj"){
        $("#tiempoJuego").addClass("w3-hide");
        $("#tiempoJuego").removeClass("w3-hide");
    }
    else{
        $("#tiempoJuego").addClass("w3-hide");
    }
}

function chequearCodigo(){
    var codigo = $("#codigoComentarExamen").val();

    $.ajax({

        url: "/codigoFeedback",
        type: 'post',
        data:JSON.stringify({codigo: codigo}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",

        success: function (datos) {
            if (datos["success"]){
                $("#divComent").addClass("w3-hide");
                $("#divComent").removeClass("w3-hide");
                $("#divCodComent").removeClass("w3-hide");
                $("#divCodComent").addClass("w3-hide");
            }
            else{
                $("#divComent").removeClass("w3-hide");
                $("#divComent").addClass("w3-hide");
                alert("Código Incorrecto");
            }
        }
    })
}

function procesarComentario(reaccionEscogida){
    var reaccion = $(reaccionEscogida).val();
    var codigoExamenComent = $("#codigoComentarExamen").val();
    var comentario = $("#comentarioReaccion").val();

    if(comentario.trim() === "")
        imprimirMensaje("El comentario no puede ir vacío.")
    else
        procesarAjaxComentario(reaccion, codigoExamenComent, comentario);
}

function imprimirMensaje(mensaje){

    var modal = "<div class=\"modal fade\" id=\"modalAlerta\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"exampleModalLabel\" aria-hidden=\"true\">\n" +
        "        <div class=\"modal-dialog modal-dialog-centered\" role=\"document\">\n" +
        "            <div class=\"modal-content\">\n" +
        "                <div class=\"modal-header\">\n" +
        "                    <h2 class=\"modal-title\" id=\"exampleModalLabel\">Alerta</h2>\n" +
        "                    <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">\n" +
        "                        <span aria-hidden=\"true\">&times;</span>\n" +
        "                    </button>\n" +
        "                </div>\n" +
        "                <div id='descripcionAlerta' class=\"modal-body\">\n" +
        "                    ...\n" +
        "                </div>\n" +
        "                <div class=\"modal-footer\">\n" +
        "                    <button type=\"button\" class=\"btn btn-secondary modalB\" data-dismiss=\"modal\">Cerrar</button>\n" +
        "                </div>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>";

    var modalJquery = $(modal);
    modalJquery.find("#descripcionAlerta").text(mensaje);

    modalJquery.modal({
        show:true
    })

}

function subtemaValido(idSelect){

    var select =  $("#"+idSelect);
    if(select.val() === null ||select.val() === "Escoger Subtema"){
        imprimirMensaje("Debe escoger un subtema válido.");
        return false;
    }

    return true
}

function itemValido(idSelect){
    var select =  $("#"+idSelect);
    if(select.val() === null ||select.val() === "Escoger Item"){

        imprimirMensaje("Debe escoger un item válido.");
        return false;
    }

    return true
}

function validarItem(descripcion,puntaje,selectSubtema){

    var subtemaValidado = subtemaValido(selectSubtema);
    var puntajeObj = $("#"+puntaje);
    if(subtemaValidado){
        if($("#"+descripcion).val().trim() === "" || puntajeObj.val().trim() === "" || isNaN(puntajeObj.val()) ) {
            imprimirMensaje("Ingrese una descripción y un puntaje válidos. Ninguno puede estar vacío.");
            return false
        }
        return true
    }
    else{
        return false
    }

}

function validarItemModificar(descripcion,puntaje){

    var puntajeObj = $("#"+puntaje);

    if(itemValido("itemModiEli")) {
        if ($("#" + descripcion).val().trim() === "" || puntajeObj.val().trim() === "" || isNaN(puntajeObj.val())) {
            imprimirMensaje("Ingrese una descripción y un puntaje válidos. Ninguno puede estar vacío.");
            return false
        }
        return true
    }
    return false



}

function validarRespuestas(idSelectItem,listaRespuestas,idRespDesarrollo){
    var itemValidado = itemValido(idSelectItem);

    if(itemValidado){
        var tipoItem = $("#"+idSelectItem).val().split("/Item")[0].split("-")[2];
        if (tipoItem === "S" || tipoItem === "PS"){

            for(var i =0; i< listaRespuestas.length; i++){
                if($(listaRespuestas[i]).val().trim() === "") {
                    imprimirMensaje("Se deben ingresar todas las respuestas.");
                    return false
                }
            }
        }
        else{
            if ($("#"+idRespDesarrollo).val().trim() === "") {
                imprimirMensaje("La respuesta del item seleccionado no puede ser vacía.");
                return false
            }
        }
        return true


    }
    return false



}

function validarEncabezado(){

    var fecha = $("#fechaEncabezado").val();

    var tiempoHoras = $("#tiempoEncabezadoHoras").val();
    var tiempoMin = $("#tiempoEncabezadoMinutos").val();

    var instrucciones = $("#instruccionesEncabezado").val();

    if (fecha.trim() === ""  || tiempoHoras.trim() === "" || tiempoMin.trim() === "" || instrucciones.trim() === "") {
        imprimirMensaje("Se deben ingresar todos los datos para la previsualización del encabezado");
        return false
    }

    return true
}

function validarTema(idInputTema){

    if($("#"+idInputTema).val().trim() === ""){
        imprimirMensaje("El tema ingresado no puede ser vacío. Intente de nuevo");
        return false
    }

    return true

}

function validarSubtema(idInputSubtema){
    if($("#"+idInputSubtema).val().trim() === ""){
        imprimirMensaje("El subtema ingresado no puede ser vacío. Intente de nuevo");
        return false
    }

    return true
}

function validarSelectTema(idSelect){
    if($("#"+idSelect).val() === "Escoger Tema"){
        imprimirMensaje("Debe escoger un tema válido");
        return false
    }
    return true
}

function validarSelectSubtema(idSelect){
    var selectSubtema = $("#"+idSelect).val();
    if(selectSubtema === "Escoger Subtema" || selectSubtema === null){
        imprimirMensaje("Debe escoger un subtema válido");
        return false
    }
    return true
}

function validarModTema(){

    return validarSelectTema('selectTemaModEli') && validarTema('nuevoModificarTema')
}

function validarAddSubtema(){

    return validarSelectTema('selectTemaAddSub') && validarSubtema('subtemaNuevo')
}

function validarModSubtema(){

    return validarSelectSubtema('selectSubModificar') && validarSubtema('nuevoModificarSubtema')
}

function guardarJuego(){
    var codigo = $("#codigoSesion").val();
    var cantItems = $("#cantItems").val();
    var idSubtema = $("#subtemaJuego").val();
    var tipoJuego = $("#selectTipoJuego").val();
    var cantidadTiempo = 0 ? $("#tiempoJuego").val().trim() === "": $("#tiempoJuego").val();

    if(codigo.trim() === "" || cantItems.trim()===""||isNaN(cantItems) || idSubtema=== null || idSubtema ==="Escoger Subtema" ||
    tipoJuego === "Escoger Tipo")
        print("Error, verifique que todos los campos hayan sido llenados y con los datos correctos.");
    else
        procesarAjaxJuego(codigo)
}

function agregarEquipo(){
    var codigo = $("#codigoSesion").val();
    var nombreEquipo = $("#nombreEquipo").val();

    if(codigo.trim() === "" || nombreEquipo.trim()==="")
        imprimirMensaje("Error, ingrese todos los datos");
    else
        procesarAjaxAgregarEquipo(codigo,nombreEquipo)
}

function mostrarRespuestaJuego(respuestaActual){

    var modal = "<div class=\"modal fade\" id=\"modalRespuestaJuego\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"exampleModalLabel\" aria-hidden=\"true\">\n" +
        "        <div class=\"modal-dialog modal-dialog-centered\" role=\"document\">\n" +
        "            <div class=\"modal-content\">\n" +
        "                <div class=\"modal-header\">\n" +
        "                    <h2 class=\"modal-title\" id=\"exampleModalLabel\">Respuesta Correcta</h2>\n" +
        "                    <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">\n" +
        "                        <span aria-hidden=\"true\">&times;</span>\n" +
        "                    </button>\n" +
        "                </div>\n" +
        "                <div id='descripcionRespuestaJuego' class=\"modal-body\">\n" +
        "                    ...\n" +
        "                </div>\n" +
        "                <div class=\"modal-footer\">\n" +
        "                    <button type=\"button\" class=\"btn btn-secondary modalB\" data-dismiss=\"modal\">Cerrar</button>\n" +
        "                </div>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>";

    var modalJquery = $(modal);
    modalJquery.find("#descripcionRespuestaJuego").text(respuestaActual);

    modalJquery.modal({
        show:true
    })
}

function iniciarCronometro(boton,tiempo, idCronometro,respuesta){
    var tiempoActual = new Date().getTime() + 60* parseFloat(tiempo) * 1000 + 2000;
    $(boton).attr("disabled",true);
    var x = setInterval(function() {

      var now = new Date().getTime();

      // Find the distance between now and the count down date
      var distance = tiempoActual - now;

      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);

      $("#"+idCronometro).text(minutes+"m :"+seconds+"s");

    if (distance <= 0) {
        clearInterval(x);
        $(boton).removeAttr("disabled",true);
        $("#"+idCronometro).text("Tiempo Finalizado.");

         mostrarRespuestaJuego(respuesta)
      }

    },1000);
}

function mostrarEquiposCalificar(puntaje){

    procesarAjaxEquipos(puntaje)

}

function mostrarScoreboard(){
    $.ajax({
        url: "/cargarScoreboard",
        type: 'post',
        dataType: "json",

        success: function (datos) {
            var tbody =  $("#tablaScoreboardBody");

            tbody.children().remove();
            for(var i = 0; i< datos["listaEquipos"].length; i++){
                tbody.append($('<tr>').append($('<td>',{text:datos["listaEquipos"][i][1]})).append($('<td>',{text:datos["listaEquipos"][i][2]})));
            }

            $("#modalScoreboard").modal({
                show:true
            })
        }
    })
}

function finalizarSesion(){
    $.ajax({
        url: "/finalizarSesion",
        type: 'post',
        dataType: "json",

        success: function () {
            window.location.href = "/OpcionesPrincipales";
        }
    })
}