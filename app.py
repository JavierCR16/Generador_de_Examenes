from flask import Flask, render_template,request,session,jsonify
from Controlador.Controlador import Controlador


app = Flask(__name__)
app.secret_key = "super secret key"
Controller = Controlador()

@app.route('/')
def main():
    return render_template('OpcionesPrincipales.html')#TODO Aqui que redireccione a la de login

#CRUD TEMAS SUBTEMAS
@app.route("/CRUDTemasSubtemas.html")
def ventanaCRUDTemasSubtemas():
    listaTemas = Controller.obtenerTemas()

    return render_template("CRUDTemasSubtemas.html", temas = listaTemas)

@app.route('/crudTemasSubtemas', methods=['post'])
def crudTemasSubtemas():

    valor_boton = request.form.get("accioncrudtemassubtemas")

    if(valor_boton == "Agregar Tema"):
        Controller.insertarNuevoTema(request.form.get("temaNuevo"))

    elif(valor_boton == "Agregar Subtema"):

        nuevoSubtema = request.form.get("subtemaNuevo")
        temaSeleccionado = request.form.get("selectTema")

        Controller.insertarNuevoSubtema(nuevoSubtema,temaSeleccionado)

    elif(valor_boton == "Modificar Tema"):
         nuevoTemaMod = request.form.get("nuevoModificarTema")
         temaSeleccionado = request.form.get("selectTemaModEli")

         Controller.modificarTema(nuevoTemaMod,temaSeleccionado)

    elif(valor_boton == "Eliminar Tema"):
        temaAEliminar = request.form.get("selectTemaModEli")
        Controller.eliminarTema(temaAEliminar)

    elif (valor_boton == "Modificar Subtema"):
        nuevoSubMod = request.form.get("nuevoModificarSubtema")
        subtemaSeleccionado = request.form.get("selectSub")

        Controller.modificarSubtema(subtemaSeleccionado,nuevoSubMod)

    elif (valor_boton == "Eliminar Subtema"):
        subAEliminar = request.form.get("selectSub")
        Controller.eliminarSubtema(subAEliminar)

    temasExistentes = Controller.obtenerTemas()

    return render_template('CRUDTemasSubtemas.html',temas = temasExistentes)

@app.route('/filtrarSubtemas', methods=["post"])
def filtrarSubtemas():
    tema = request.get_json()
    subtemas = Controller.filtrarSubtemas(tema['informacion'])
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
        Controller.agregarIndice(idItemModificar, nuevoIndice)
    else:
        Controller.eliminarIndice(idItemModificar)

    itemsActualizados = Controller.filtrarItems(idSubtemaFiltro)

    return jsonify({'items':Controller.convertirItemsJson(itemsActualizados)})

@app.route("/CRUDIndiceDiscriminacion.html")
def crudIndiceDiscriminacion():

    listaTemas = Controller.obtenerTemas()
    return render_template("CRUDIndiceDiscriminacion.html", temas = listaTemas)

@app.route("/BuscarSubtemasItems", methods=['post'])
def buscarSubtemasItems():

    subtemaFiltroIndice = request.form.get("subtemaIndice")

    itemsIndiceFiltrados = Controller.filtrarItems(subtemaFiltroIndice)

    descripcionesItems = [item.getDescripcion() for item in itemsIndiceFiltrados]

    listaTemas = Controller.obtenerTemas()

    return render_template("CRUDIndiceDiscriminacion.html", temas = listaTemas, itemsFiltroIndice = itemsIndiceFiltrados,
                           descripItems = descripcionesItems)

#CRUD ITEMS
@app.route("/CRUDItems.html")
def ventanaCRUDItems():
    listaTemas = Controller.obtenerTemas()

    return render_template("CRUDItems.html", temas = listaTemas)

@app.route('/crudItemsAgregar', methods = ['post'])
def crudItemsAgregar():

    descripcion = request.form.get("descripcionItemAgregar")
    tipo = request.form.get("tiposItemAgregar")
    subtemaSeleccionado = request.form.get("selectSubAgregar")
    puntaje = request.form.get("puntajeAgregar")

    Controller.agregarItem(descripcion,tipo,subtemaSeleccionado,puntaje)

    temasExistentes = Controller.obtenerTemas()

    return render_template('CRUDItems.html', temas = temasExistentes)

@app.route('/filtrarItems', methods = ['post'])
def filtrarItems():
    filtroItems = request.get_json()
    subtemaFiltro = filtroItems['informacionSubtema']
    listaItems = Controller.filtrarItems(subtemaFiltro)
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

        Controller.modificarItem(itemModificar, tipoItemModificar, descripcionModificar,puntajeModificar)

    else:
        itemEliminar = request.form.get("selectItemModificarEliminar")
        Controller.eliminarItem(itemEliminar)

    temasExistentes = Controller.obtenerTemas()

    return render_template('CRUDItems.html', temas=temasExistentes)

@app.route("/extraerInformacionItem", methods=['post'])
def extraerInformacionItem():
    infoJson = request.get_json()
    idItem = infoJson['item']

    informacionItem = Controller.obtenerItemByID(idItem)

    return jsonify({'informacionItem':informacionItem.__dict__})

#CRUD RESPUESTAS
@app.route("/CRUDRespuestas.html")
def ventanaCRUDRespuestas():
    listaTemas = Controller.obtenerTemas()
    return render_template("CRUDRespuestas.html", temas = listaTemas)

@app.route("/crudRespuestasAgregar", methods=['post']) ##Revisar
def crudRespuestasAgregar():

    itemSeleccionado = request.form.get("selectItemRespAgregar")
    respCorrecta = request.form.get("Arespuesta")
    respuestas = [request.form.get("Arespuesta1"),request.form.get("Arespuesta2"),request.form.get("Arespuesta3")
                      ,request.form.get("Arespuesta4")]

    Controller.agregarRespuestas(itemSeleccionado,respuestas,respCorrecta)

    listaTemas = Controller.obtenerTemas()
    return render_template("CRUDRespuestas.html",temas = listaTemas)

@app.route("/extraerRespuestasItem", methods = ['post'])
def extraerRespuestasItem():

    infoJson = request.get_json()
    objetoRespuesta = Controller.obtenerRespuestasViejas(infoJson["item"])

    return jsonify({'informacionItem':objetoRespuesta.__dict__})

@app.route("/crudRespuestasModificar", methods=['post'])  ##Revisar
def crudRespuestasModificar():

    itemSeleccionado = request.form.get("selectItemRespModificar")
    respCorrecta = request.form.get("Mrespuesta")
    respuestas = [request.form.get("Mrespuesta1"), request.form.get("Mrespuesta2"), request.form.get("Mrespuesta3")
            , request.form.get("Mrespuesta4")]

    Controller.modificarRespuestas(itemSeleccionado,respuestas,respCorrecta)
    listaTemas = Controller.obtenerTemas()

    return render_template("CRUDRespuestas.html", temas=listaTemas)

@app.route("/CRUDEncabezado.html")
def ventanaCRUDEncabezado():

    Periodos = Controller.obtenerPeriodos()
    Tipos = Controller.obtenerTExamen()
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

    Controller.insertarNuevoEncabezado(curso,escuela,instrucciones, periodo, fecha, tiempo, tipo)

    Periodos = Controller.obtenerPeriodos()
    Tipos = Controller.obtenerTExamen()

    return render_template("CRUDEncabezado.html", tiposExamen=Tipos, periodos=Periodos)

@app.route("/ConstruirExamen.html")
def construirExamen():

    return render_template("ConstruirExamen.html")

if __name__ == '__main__':

    app.run()
