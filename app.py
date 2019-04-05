from flask import Flask, render_template,request,session,jsonify
from Controlador.Controlador import Controlador

app = Flask(__name__)
app.secret_key = "super secret key"
Controller = Controlador()


@app.route('/')
def main():

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

        Controller.loadInformacionExamen(Controller.obtenerTemas(session['user'],session['contrasenna']),'S',session['user'],session['contrasenna'])

        return render_template('OpcionesPrincipales.html')

    return render_template('LogIn.html')


#CRUD TEMAS SUBTEMAS
@app.route("/CRUDTemasSubtemas.html")
def ventanaCRUDTemasSubtemas():
    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template("CRUDTemasSubtemas.html", temas = listaTemas)

@app.route('/crudTemasSubtemas', methods=['post'])
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

@app.route("/CRUDIndiceDiscriminacion.html")
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
@app.route("/CRUDItems.html")
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

    tipoFiltrado = filtroItems['tipo'] #total, usuario

    subtemaFiltro = filtroItems['informacionSubtema']

    listaItems = Controller.filtrarItems(subtemaFiltro,tipoFiltrado,session['user'],session['contrasenna'])
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
@app.route("/CRUDRespuestas.html")
def ventanaCRUDRespuestas():
    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])
    return render_template("CRUDRespuestas.html", temas = listaTemas)

@app.route("/crudRespuestasAgregar", methods=['post']) ##Revisar
def crudRespuestasAgregar():

    itemSeleccionado = request.form.get("selectItemRespAgregar")
    respCorrecta = request.form.get("Arespuesta")
    respuestas = [request.form.get("Arespuesta1"),request.form.get("Arespuesta2"),request.form.get("Arespuesta3")
                      ,request.form.get("Arespuesta4")]

    Controller.agregarRespuestas(itemSeleccionado,respuestas,respCorrecta,session['user'],session['contrasenna'])

    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])
    return render_template("CRUDRespuestas.html",temas = listaTemas)

@app.route("/extraerRespuestasItem", methods = ['post'])
def extraerRespuestasItem():

    infoJson = request.get_json()
    objetoRespuesta = Controller.obtenerRespuestasViejas(infoJson["item"],session['user'],session['contrasenna'])

    return jsonify({'informacionItem':objetoRespuesta.__dict__})

@app.route("/crudRespuestasModificar", methods=['post'])  ##Revisar
def crudRespuestasModificar():

    itemSeleccionado = request.form.get("selectItemRespModificar")
    respCorrecta = request.form.get("Mrespuesta")
    respuestas = [request.form.get("Mrespuesta1"), request.form.get("Mrespuesta2"), request.form.get("Mrespuesta3")
            , request.form.get("Mrespuesta4")]

    Controller.modificarRespuestas(itemSeleccionado,respuestas,respCorrecta,session['user'],session['contrasenna'])
    listaTemas = Controller.obtenerTemas(session['user'],session['contrasenna'])

    return render_template("CRUDRespuestas.html", temas=listaTemas)


#CRUD ENCABEZADO
@app.route("/CRUDEncabezado.html")
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

    Controller.generarPreview(curso,escuela,instrucciones,periodo,fecha,tiempo,tipo)

    return jsonify(status = "success")

@app.route("/guardarEncabezado", methods= ['post'])
def guardarEncabezado():

    curso = "Probabilidades" #TODO Agarrar de un combobox
    escuela = "Escuela de Matemática" #TODO Agarrar de un combobox
    instrucciones = request.form.get("txtInstrucciones")
    periodo = request.form.get("selectPeriodo")
    fecha = request.form.get("inputFecha")
    tiempo = request.form.get("inputTiempo")
    tipo = request.form.get("selectTipo")

    Controller.insertarNuevoEncabezado(curso,escuela,instrucciones, periodo, fecha, tiempo, tipo,session['user'],session['contrasenna'])

    Periodos = Controller.obtenerPeriodos(session['user'],session['contrasenna'])
    Tipos = Controller.obtenerTExamen(session['user'],session['contrasenna'])

    return render_template("CRUDEncabezado.html", tiposExamen=Tipos, periodos=Periodos)

#CRUD CONSTRUIR EXAMEN
@app.route("/ConstruirExamen.html")
def construirExamen():

    return render_template("ConstruirExamen.html")


#CRUD SUGERIR EDICIONES

@app.route("/SugerenciaEdicion.html")
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

@app.route("/VerificacionEdicion.html")
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

if __name__ == '__main__':

    app.run(host = '0.0.0.0')

