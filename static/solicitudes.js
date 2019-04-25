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
                var boton = $('<button class="consult-button"><i class="material-icons" style="font-size:20px;">info</i></button>').attr(
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
            if(datos["success"]){
                var retVal = confirm("¿Desea descargar el examen en formato PDF? De igual forma puede descargarlo en la sección de Filtrado de Exámenes");
                if( retVal === true ) { //../static/
                    $("#secretDownload").attr("href","../static/"+datos["archivoPDF"])[0].click();
                }

                window.location.href = "CreacionExamen.html";
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

function obtenerSubtemas(selectEscogido, idObjHTML){

    var temaEscogido = selectEscogido.options[selectEscogido.selectedIndex].text;

    procesarAjaxSubtemas(temaEscogido, idObjHTML)
}

function obtenerItems(selectEscogido,tipoFiltrado ,idSelectItems,idPopDescripcion){

    var subtemaEscogido = selectEscogido.options[selectEscogido.selectedIndex].text;

    procesarAjaxItems(subtemaEscogido,tipoFiltrado,idSelectItems,idPopDescripcion,"/filtrarItems")

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

function verificarIndiceDiscriminacion(botonClickeado,descripItems) {
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

function ObtenerDatosdeEstadistica() {

    var TemaDOM = document.getElementById("SelectTemaEstadisticas");
    var tema = TemaDOM.options[TemaDOM.selectedIndex].text;
    var idtema = tema.split('-')[0]

    var SubTemaDOM = document.getElementById("SelectSubtemaEstadisticas");
    var subTema = SubTemaDOM.options[SubTemaDOM.selectedIndex].text;
    var idsubTema = subTema.split('-')[0]

    var itemDOM = document.getElementById("SelectItemEstadisticas");
    var item = itemDOM.options[itemDOM.selectedIndex].text;
    var iditem = item.split('-')[0]

    obtenerAjaxEstadisticas(idtema,idsubTema,iditem)
}

function obtenerAjaxEstadisticas(idTema,idsubTema,idItem) {
    $.ajax({

        url: "/ObtenerEstadisticas",
        type: 'post',
        data:JSON.stringify({idTema:idTema,idsubTema:idsubTema,idItem:idItem}),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",
        success: function (datos) {
            var bodyModalEstadisticas = $("#VistaEstadisticas");
            bodyModalEstadisticas.find('h2').remove();

            bodyModalEstadisticas.append("<h2>Cantidad de veces usado:" + datos["cantVeces"]+ "</h2>");
            bodyModalEstadisticas.append("<h2>Promedio de indice de Discriminación del subtema:" + datos["PromedioSubtema"]+ "</h2>");

            var modalEstadisticas = $("#estadisticasModal");

            modalEstadisticas.modal({
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

    $.each($("input[name ='items']:checked"), function () {
            idItems.push($(this).val().split(",")[1])
    });

    var data = encabezado + "%" +tipoExamen + "%" + JSON.stringify(idItems);

    download("Borrador.exam",data)

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
            $(this).attr('checked', true);
    });


}