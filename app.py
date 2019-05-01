from flask import Flask, render_template,request,session,jsonify,redirect, url_for
from Controlador.Controlador import Controlador

app = Flask(__name__)
app.secret_key = "super secret key"
Controller = Controlador()


@app.route('/')
def main():

    if (session.get('user') is not None):
        return redirect(url_for('opcionesPrincipales'))

    return render_template('LogIn.html')

@app.route('/login',methods=['post'])
def login():
    user = request.form.get("correo")
    contrasenna = request.form.get("contrasenna")
    conexion = Controller.comprobarConexion(user,contrasenna)

    if(conexion!= False):
        session['user'] = user
        session['contrasenna'] = contrasenna
        Controller.cerrarConexion(conexion)

        return redirect(url_for('opcionesPrincipales'))

    return render_template('LogIn.html')

@app.route('/OpcionesPrincipales')
def opcionesPrincipales():
    usuario = Controller.getNombreUsuario(session['user'],session['contrasenna'])
    return render_template("OpcionesPrincipales.html", nombre = usuario)

@app.route('/cerrarSesion',methods = ['post'])
def cerrarSesion():

    session.pop('user',None)
    session.pop('contrasenna',None)

    return render_template("LogIn.html")

#CRUD TEMAS SUBTEMAS
@app.route("/CRUDTemasSubtemas")
def ventanaCRUDTemasSubtemas():
    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template("CRUDTemasSubtemas.html", temas = listaTemas)

@app.route('/crudTemasSubtemas', methods=['post']) #TODO PONER MENSAJE DE EXITO O FALLO
def crudTemasSubtemas():

    valor_boton = request.form.get("accioncrudtemassubtemas")

    if(valor_boton == "Agregar Tema"):
        Controller.insertarNuevoTema(request.form.get("temaNuevo"),session['user'],session['contrasenna'])

    elif(valor_boton == "Agregar Subtema"):

        nuevoSubtema = request.form.get("subtemaNuevo")
        temaSeleccionado = request.form.get("selectTema")

        Controller.insertarNuevoSubtema(nuevoSubtema,temaSeleccionado,session['user'],session['contrasenna'])

    elif(valor_boton == "Modificar Tema"):
         nuevoTemaMod = request.form.get("nuevoModificarTema")
         temaSeleccionado = request.form.get("selectTemaModEli")

         Controller.modificarTema(nuevoTemaMod,temaSeleccionado,session['user'],session['contrasenna'])

    elif(valor_boton == "Eliminar Tema"):
        temaAEliminar = request.form.get("selectTemaModEli")
        Controller.eliminarTema(temaAEliminar,session['user'],session['contrasenna'])

    elif (valor_boton == "Modificar Subtema"):
        nuevoSubMod = request.form.get("nuevoModificarSubtema")
        subtemaSeleccionado = request.form.get("selectSub")

        Controller.modificarSubtema(subtemaSeleccionado,nuevoSubMod,session['user'],session['contrasenna'])

    elif (valor_boton == "Eliminar Subtema"):
        subAEliminar = request.form.get("selectSub")
        Controller.eliminarSubtema(subAEliminar,session['user'],session['contrasenna'])

    temasExistentes = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template('CRUDTemasSubtemas.html',temas = temasExistentes)

@app.route('/filtrarSubtemas', methods=["post"])
def filtrarSubtemas():
    tema = request.get_json()
    subtemas = Controller.filtrarSubtemas(tema['informacion'],session['user'],session['contrasenna'])
    return jsonify({"subtemas":Controller.convertirSubtemasJson(subtemas)})

#CRUD INDICE DISCRIMINACION
@app.route("/cambioIndiceDiscriminacion", methods=['post'])
def cambioIndiceDiscriminacion():
    datosItem = request.get_json()

    nuevoIndice = datosItem['newIndex']
    idItemModificar = datosItem['idItem']
    valorBoton = datosItem['botonPresionadoIndice']
    idSubtemaFiltro = datosItem['idSubtema']

    if(valorBoton == "agregarIndiceBoton" or valorBoton == "modificarIndiceBoton" ):
        Controller.agregarIndice(idItemModificar, nuevoIndice,session['user'],session['contrasenna'])
    else:
        Controller.eliminarIndice(idItemModificar,session['user'],session['contrasenna'])

    itemsActualizados = Controller.filtrarItems(idSubtemaFiltro,"total",session['user'],session['contrasenna'])

    return jsonify({'items':Controller.convertirItemsJson(itemsActualizados)})

@app.route("/CRUDIndiceDiscriminacion")
def crudIndiceDiscriminacion():
    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])
    return render_template("CRUDIndiceDiscriminacion.html", temas = listaTemas)

@app.route("/BuscarSubtemasItems", methods=['post'])
def buscarSubtemasItems():

    subtemaFiltroIndice = request.form.get("subtemaIndice")

    itemsIndiceFiltrados = Controller.filtrarItems(subtemaFiltroIndice,"total",session['user'],session['contrasenna'])

    descripcionesItems = [item.getDescripcion() for item in itemsIndiceFiltrados]

    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template("CRUDIndiceDiscriminacion.html", temas = listaTemas, itemsFiltroIndice = itemsIndiceFiltrados,
                           descripItems = descripcionesItems)

#CRUD ITEMS
@app.route("/CRUDItems")
def ventanaCRUDItems():
    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template("CRUDItems.html", temas = listaTemas)

@app.route('/crudItemsAgregar', methods = ['post'])
def crudItemsAgregar():

    descripcion = request.form.get("descripcionItemAgregar")
    tipo = request.form.get("tiposItemAgregar")
    subtemaSeleccionado = request.form.get("selectSubAgregar")
    puntaje = request.form.get("puntajeAgregar")

    Controller.agregarItem(descripcion,tipo,subtemaSeleccionado,puntaje,session['user'],session['contrasenna'])

    temasExistentes = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template('CRUDItems.html', temas = temasExistentes)

@app.route('/filtrarItems', methods = ['post'])
def filtrarItems():
    filtroItems = request.get_json()

    tipoFiltrado = filtroItems['tipo'] #total, parcial, cualquier otro

    subtemaFiltro = filtroItems['informacionSubtema']

    listaItems = Controller.filtrarItems(subtemaFiltro,tipoFiltrado,session['user'],session['contrasenna'])

    descripcionesItems = [item.getDescripcion() for item in listaItems]

    return jsonify({'items':Controller.convertirItemsJson(listaItems), 'descripcionItems':Controller.convertirJson(descripcionesItems)})

@app.route('/filtrarItemsRespuestas', methods=['post'])
def filtrarItemsRespuestas():
    filtroItems = request.get_json()

    tipoFiltrado = filtroItems['tipo']

    subtemaFiltro = filtroItems['informacionSubtema']

    listaItems = Controller.filtrarItemsRespuestas(subtemaFiltro,tipoFiltrado,session['user'],session['contrasenna'])

    descripcionesItems = [item.getDescripcion() for item in listaItems]

    return jsonify({'items':Controller.convertirItemsJson(listaItems), 'descripcionItems':Controller.convertirJson(descripcionesItems)})

@app.route('/crudItemsModificar', methods = ['post'])
def crudItemsModificar():

    valor_boton = request.form.get("accioncruditems")

    if(valor_boton == "Modificar Item"):

        itemModificar = request.form.get("selectItemModificarEliminar")
        tipoItemModificar = request.form.get("tiposItemModificar")
        descripcionModificar = request.form.get("descripcionItemModificar")
        puntajeModificar = request.form.get("puntajeModificar")

        Controller.modificarItem(itemModificar, tipoItemModificar, descripcionModificar,puntajeModificar,session['user'],session['contrasenna'])

    else:
        itemEliminar = request.form.get("selectItemModificarEliminar")
        Controller.eliminarItem(itemEliminar,session['user'],session['contrasenna'])

    temasExistentes = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template('CRUDItems.html', temas=temasExistentes)

@app.route("/extraerInformacionItem", methods=['post'])
def extraerInformacionItem():
    infoJson = request.get_json()
    idItem = infoJson['item']

    informacionItem = Controller.obtenerItemByID(idItem,session['user'],session['contrasenna'])

    return jsonify({'informacionItem':informacionItem.__dict__})

#CRUD RESPUESTAS
@app.route("/CRUDRespuestas")
def ventanaCRUDRespuestas():
    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])
    return render_template("CRUDRespuestas.html", temas = listaTemas)

@app.route("/crudRespuestasAgregar", methods=['post']) ##Revisar
def crudRespuestasAgregar():

    itemSeleccionado = request.form.get("selectItemRespAgregar")
    tipoItem = itemSeleccionado.split("/Item")[0].split("-")[2]

    respCorrecta = ""
    respuestas = []

    if(tipoItem == "S" or tipoItem == "PS"):
        respCorrecta = request.form.get("Arespuesta")
        respuestas = [request.form.get("Arespuesta1"),request.form.get("Arespuesta2"),request.form.get("Arespuesta3")
                      ,request.form.get("Arespuesta4")]
    else:
        respCorrecta = 1 #Para que pegue con la base
        respuestas = request.form.getlist("respAddDesarrollo")

    Controller.agregarRespuestas(itemSeleccionado,respuestas,respCorrecta,session['user'],session['contrasenna'])

    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])
    return render_template("CRUDRespuestas.html",temas = listaTemas)

@app.route("/crudRespuestasModificar", methods=['post'])  ##Revisar
def crudRespuestasModificar():

    itemSeleccionado = request.form.get("selectItemRespModificar")
    tipoItem = itemSeleccionado.split("/Item")[0].split("-")[2]

    respCorrecta = ""
    respuestas = []

    if (tipoItem == "S" or tipoItem == "PS"):
        respCorrecta = request.form.get("Mrespuesta")
        respuestas = [request.form.get("Mrespuesta1"), request.form.get("Mrespuesta2"), request.form.get("Mrespuesta3")
            , request.form.get("Mrespuesta4")]
    else:
        respCorrecta = 1  # Para que pegue con la base
        respuestas = request.form.getlist("respModDesarrollo")

    Controller.modificarRespuestas(itemSeleccionado,respuestas,respCorrecta,session['user'],session['contrasenna'])
    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template("CRUDRespuestas.html", temas=listaTemas)

@app.route("/extraerRespuestasItem", methods = ['post'])
def extraerRespuestasItem():

    infoJson = request.get_json()
    objetoRespuesta = Controller.obtenerRespuestasViejas(infoJson["item"],session['user'],session['contrasenna'])

    return jsonify({'informacionItem':objetoRespuesta.__dict__})

#CRUD ENCABEZADO
@app.route("/CRUDEncabezado")
def ventanaCRUDEncabezado():

    Periodos = Controller.obtenerPeriodos(session['user'],session['contrasenna'])
    Tipos = Controller.obtenerTExamen(session['user'],session['contrasenna'])
    return render_template("CRUDEncabezado.html", tiposExamen = Tipos, periodos = Periodos)

@app.route("/previewEncabezado",methods= ['post'])
def previewEncabezado():

    infoPreview = request.get_json()

    curso = infoPreview["curso"]
    escuela = infoPreview["escuela"]
    periodo = infoPreview["periodo"]
    fecha = infoPreview["fecha"]
    tiempo = infoPreview["tiempo"]
    tipo = infoPreview["tipo"]
    instrucciones = infoPreview["instrucciones"]

    nombreImagen = Controller.generarPreview(curso,escuela,instrucciones,periodo,fecha,tiempo,tipo)

    return jsonify({"imagen":nombreImagen})

@app.route("/guardarEncabezado", methods= ['post'])
def guardarEncabezado():

    curso = "Probabilidades" #TODO Agarrar de un combobox
    escuela = "Escuela de Matemática" #TODO Agarrar de un combobox
    instrucciones = request.form.get("txtInstrucciones")
    periodo = request.form.get("selectPeriodo")
    fecha = request.form.get("inputFecha")

    tiempoHoras = request.form.get("tiempoEncabezadoHoras")
    tiempoMinutos = request.form.get("tiempoEncabezadoMinutos")
    tiempo = tiempoHoras + ":" + tiempoMinutosx

    tipo = request.form.get("selectTipo")

    Controller.insertarNuevoEncabezado(curso,escuela,instrucciones, periodo, fecha, tiempo, tipo,session['user'],session['contrasenna'])

    Periodos = Controller.obtenerPeriodos(session['user'],session['contrasenna'])
    Tipos = Controller.obtenerTExamen(session['user'],session['contrasenna'])

    return render_template("CRUDEncabezado.html", tiposExamen=Tipos, periodos=Periodos)

#CRUD SUGERIR VERIFICAR EDICIONES

@app.route("/SugerenciaEdicion")
def sugerenciaEdicion():
    temas = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template("SugerenciaEdicion.html", temasItemEdicion=temas)

@app.route("/buscarItemsSugerencia",methods=['post'])
def sugerirEdicion():
    subtemaFiltro = request.form.get("subtemaSugerencia")

    objetosItems = Controller.filtrarItems(subtemaFiltro,'noparcial',session['user'],session['contrasenna'])

    descripcionesItems = [item.getDescripcion() for item in objetosItems]

    temas = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template("SugerenciaEdicion.html",temasItemEdicion =temas, descripItems = descripcionesItems, itemsFiltroSugerencia = objetosItems)

@app.route("/enviarSugerencia",methods=['post'])
def enviarSugerencia():

    datosSugerencia = request.get_json()

    nuevaEdicion = datosSugerencia['nuevaEdicion']
    comentarios = datosSugerencia['comentarios']
    idItem = datosSugerencia['idItem']

    Controller.enviarSugerencia(idItem,nuevaEdicion,comentarios,session['user'],session['contrasenna'])

    return jsonify({"status":"Sugerencia Enviada con Éxito"})

@app.route("/VerificacionEdicion")
def verificacionEdicion():

    objetosSugerencia = Controller.filtrarSugerencias(session['user'],session['contrasenna'])
    descripciones = [sugerencia.getDescripcionItem() for sugerencia in objetosSugerencia]
    sugerencias = [sugerencia.getSugerencia() for sugerencia in objetosSugerencia]
    comentarios = [sugerencia.getComentarios() for sugerencia in objetosSugerencia]

    return render_template("VerificacionEdicion.html",sugerenciasFiltradas  = objetosSugerencia,
                           sugerencias = sugerencias, comentarios= comentarios, descripItems = descripciones)

@app.route("/aprobarRechazarSugerencia",methods=['post'])
def aprobarRechazarSugerencia(): #1 = Aprobar, 0 = Rechazar

    informacionVerificacion = request.get_json()
    accion = informacionVerificacion['accion']
    idSugerencia =  informacionVerificacion['idSugerencia']
    sugerencia = informacionVerificacion['sugerencia']
    idItem = informacionVerificacion['idItem']


    Controller.aprobarSugerencia(idSugerencia,sugerencia,idItem,session['user'],session['contrasenna']) \
        if accion == 1 else Controller.rechazarSugerencia(idSugerencia,session['user'],session['contrasenna'])

    return jsonify({"status":"Sugerencia Revisada"})

#COMPARTIR EXAMENES
@app.route('/CompartirExamenes')
def compartirExamenes():
    usuarios = Controller.cargarUsuarios(session['user'],session['contrasenna'])

    return render_template("CompartirExamenes.html",usuarios = usuarios)

@app.route('/enviarCorreo',methods=['post'])
def enviarCorreo():

    asunto = request.form.get("asunto")
    cuerpo= request.form.get("cuerpoCorreo")
    archivosExamen = request.files.getlist("archivoExamen")
    listaCorreos = request.form.getlist("correo")
    nombreSender = Controller.getNombreUsuario(session['user'],session['contrasenna'])

    Controller.enviarExamen(nombreSender,asunto,cuerpo,archivosExamen,listaCorreos)

    usuarios = Controller.cargarUsuarios(session['user'], session['contrasenna'])

    return render_template("CompartirExamenes.html", usuarios=usuarios)

#GENERAR EXAMEN
@app.route("/CreacionExamen")
def creacionExamen():

    listaEncabezados = Controller.obtenerEncabezados(session['user'],session['contrasenna'])

    encabezadosDict = [encabezado.__dict__ for encabezado in listaEncabezados]

    return render_template("CreacionExamen.html",encabezadosDict = encabezadosDict,encabezados = listaEncabezados)

@app.route("/loadInformacionExamen",methods=['post'])
def loadInformacionExamen():
    infoExamen = request.get_json()

    tipoExamen = infoExamen["tipoExamen"]

    informacionExamen = Controller.loadInformacionExamen(tipoExamen, session['user'], session['contrasenna'])

    temas = Controller.convertirItemsJson(informacionExamen[0])
    subtemas = Controller.convertirMatrixJSON(informacionExamen[1])
    items = Controller.convertirMatrixJSON(informacionExamen[2])

    descripcionItems = [item["descripcion"] for lista in items for item in lista]

    return jsonify({"temas":temas, "subtemas":subtemas,"items":items,"descripcionItems":descripcionItems})

@app.route("/generarExamen",methods=['post'])
def generarExamen():

    informacionExamen = request.get_json()

    objEncabezado= Controller.convertirDictAObjeto(informacionExamen["encabezado"])

    itemsSeleccionados = informacionExamen["items"]

    items = [item.split(",")[0] for item in itemsSeleccionados]
    idItems = [item.split(",")[1] for item in itemsSeleccionados]
    puntajes = [int(item.split(",")[2]) for item in itemsSeleccionados]

    tipoExamen = informacionExamen["tipoExamen"]

    respuestas = Controller.obtenerRespuestasExamen(idItems,session['user'],session['contrasenna'])

    conSolucion = int(informacionExamen["solucionado"])

    nombrePDF = Controller.generarExamen(objEncabezado,items,respuestas,tipoExamen,conSolucion,puntajes)

    idExamen = Controller.guardarExamen(objEncabezado.getId(),tipoExamen,"static/"+nombrePDF,idItems,session['user'],session['contrasenna'])


    return jsonify({"success":1,"archivoPDF":nombrePDF, "idExamen":idExamen})

@app.route("/BancoExamenes")
def filtrarExamenes():

    listaExamenes = Controller.obtenerExamenes(session['user'],session['contrasenna'],"Banco")
    return render_template("BancoExamenes.html",examenes = listaExamenes)

@app.route("/descargarExamen", methods=['post'])
def descargarExamen():

    descargaInfo = request.get_json()

    idExamen = descargaInfo["idExamen"]

    nombreExamen = Controller.descargarExamen(idExamen,session['user'],session['contrasenna'])

    return jsonify({"success":1,"nombreExamen":nombreExamen})

#ESTADISTICAS
@app.route('/ConsultaEstadisticasItems')
def ConsultaEstadisticasItems():
    temas = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template('ConsultaEstadisticasItems.html', Temas = temas)

@app.route('/ObtenerEstadisticas',methods= ['post'])
def ObtenerEstadisticas():
    infoEstadisticas = request.get_json()
    idItem = infoEstadisticas["idItem"]
    idEstadistica = infoEstadisticas["idEstadistica"]

    estadistica = Controller.obtenerEstadisticas(session['user'],session['contrasenna'],int(idEstadistica),idItem)
    return jsonify({"estadistica":estadistica})

#GRAFICOS
@app.route('/Graficos')
def obtenerGraficos():
    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])
    listaExamenes = Controller.obtenerExamenes(session['user'], session['contrasenna'], "Feedback")
    return render_template("Graficos.html", temas = listaTemas, examenes = listaExamenes)

@app.route('/obtenerDatosGraficos', methods= ['post'])
def obtenerDatosGraficos():
    infoGraficos = request.get_json()
    datos = Controller.obtenerDatosGraficos(session['user'], session['contrasenna'],
                                            infoGraficos["consulta"], infoGraficos["datos"])

    return jsonify({"success": 1, "estadisticas": datos})

#FEEDBACK EXAMEN VISUALIZAR
@app.route('/filtrarComentariosFeedback',methods=['post'])
def filtrarExamenesFeedback():

    infoFeedback = request.get_json()
    filtrado = infoFeedback["filtrado"]
    parametro = infoFeedback["parametro"]  #Parametro puede ser el id del examen o el codigo alfanumerico

    comentarios = Controller.obtenerComentariosFeedback(session['user'],session['contrasenna'],[filtrado,parametro])

    return jsonify({"comentarios":comentarios})

@app.route('/publicarExamenFeedback',methods=['post'])
def publicarExamenFeedback():

    infoExamenFeed = request.get_json()

    idExamen = infoExamenFeed["idExamen"]
    codigo = infoExamenFeed["codigo"]

    Controller.publicarExamen(session['user'],session['contrasenna'],idExamen,codigo)

    return jsonify({"success":1})

@app.route("/ComentariosEstudiantes")
def filtrarComentariosEstudiantes():

    listaExamenesComentarios     = Controller.obtenerExamenes(session['user'],session['contrasenna'],"Feedback")
    return render_template("ComentariosEstudiantes.html",examenes = listaExamenesComentarios)

#JUEGO
@app.route('/SesionJuego')
def crearJuego():
    listaTemas = Controller.obtenerTemas(session['user'], session['contrasenna'])

    return render_template("SesionJuego.html", temas = listaTemas)

#ESTUDIANTES

@app.route('/EstudiantesInicio')
def estudiantesInicio():
    session['userEst'] = "estudiante.tec"
    session['contrasennaEst'] = "e5tuD1ant3"

    return render_template('EstudiantesInicio.html')

@app.route('/JuegoLogIn')
def juegoLogIn():

    return render_template('JuegoLogIn.html')

@app.route('/Comentarios')
def comentarios():
    return render_template('Comentarios.html')

@app.route('/codigoFeedback', methods=['post'])
def codigoFeedback():
    datoFeedback = request.get_json()

    codigo = datoFeedback["codigo"]

    existeCodigo = Controller.existeCodigo(session['userEst'], session['contrasennaEst'], codigo)

    return jsonify({"success": existeCodigo})

@app.route('/agregarComentario',methods=['post'])
def agregarComentario():

    infoComentario = request.get_json()

    codigo = infoComentario["codigoExamen"]
    comentario = infoComentario["comentario"]
    reaccion = infoComentario["reaccion"]

    Controller.agregarComentario(session['userEst'],session['contrasennaEst'],codigo,comentario,reaccion)

    return jsonify({"success":1,"mensaje":"Su comentario ha sido enviado con éxito"})

if __name__ == '__main__':

    app.run(host = '0.0.0.0')

