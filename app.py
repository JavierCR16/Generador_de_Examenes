from flask import Flask, render_template,request,session
from Controlador.Controlador import Controlador


app = Flask(__name__)
app.secret_key = "super secret key"
Controller = Controlador()

@app.route('/')
def main():
    return render_template('OpcionesPrincipales.html')#TODO Aqui que redireccione a la de login

@app.route("/CRUDTemasSubtemas.html")
def ventanaCRUDTemasSubtemas():
    listaTemas = Controller.obtenerTemas()
    return render_template("CRUDTemasSubtemas.html", temas = listaTemas)

@app.route('/crudTemasSubtemas', methods=['post'])
def crudTemasSubtemas():

    temaAFiltrar = ""
    subtemasFiltrados = []

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

    else:
        temaAFiltrar = request.form.get("selectTemaSub")
        subtemasFiltrados = Controller.filtrarSubtemas(temaAFiltrar)

    temasExistentes = Controller.obtenerTemas()

    return render_template('CRUDTemasSubtemas.html',temas = temasExistentes, temaFiltro = temaAFiltrar,
                           subFiltrados = subtemasFiltrados)

@app.route("/CRUDItems.html")
def ventanaCRUDItems():
    listaTemas = Controller.obtenerTemas()

    return render_template("CRUDItems.html", temas = listaTemas)

@app.route('/crudItemsAgregar', methods = ['post'])
def crudItemsAgregar():

    valor_boton = request.form.get("accioncruditems")
    temaFiltroAgregar = ""
    subtemasFiltrados = []

    if(valor_boton == "Agregar Item"):

        descripcion = request.form.get("descripcionItemAgregar")
        tipo = request.form.get("tiposItemAgregar")
        subtemaSeleccionado = request.form.get("selectSubAgregar")
        puntaje = request.form.get("puntajeAgregar")

        Controller.agregarItem(descripcion,tipo,subtemaSeleccionado,puntaje)

    else:
        temaFiltroAgregar = request.form.get("selectTemaItemAgregar")
        subtemasFiltrados = Controller.filtrarSubtemas(temaFiltroAgregar)



    temasExistentes = Controller.obtenerTemas()
    return render_template('CRUDItems.html', temas = temasExistentes, temaFiltroItemAgregar = temaFiltroAgregar,
                           subtemasItemAgregar = subtemasFiltrados)

@app.route('/crudItemsModificar', methods = ['post'])
def crudItemsModificar():

    valor_boton = request.form.get("accioncruditems")
    temaFiltroModificar = ""
    subtemasFiltrados = []
    itemsFiltrados = []
    descripcionesItems = []

    if(valor_boton == "Modificar Item"):

        itemModificar = request.form.get("selectItemModificarEliminar")
        tipoItemModificar = request.form.get("tiposItemModificar")
        descripcionModificar = request.form.get("descripcionItemModificar")
        puntajeModificar = request.form.get("puntajeModificar")

        Controller.modificarItem(itemModificar, tipoItemModificar, descripcionModificar,puntajeModificar)


    elif(valor_boton == "Eliminar Item"):

        itemEliminar = request.form.get("selectItemModificarEliminar")

        Controller.eliminarItem(itemEliminar)

    else:
        if(request.form.get("selectSubModificar") == None or request.form.get("selectSubModificar") == "Escoger Subtema"):

            temaFiltroModificar = request.form.get("selectTemaItemModificar")
            subtemasFiltrados = Controller.filtrarSubtemas(temaFiltroModificar)

        else:
            subtemaFiltro = request.form.get("selectSubModificar")
            itemsFiltrados = Controller.filtrarItems(subtemaFiltro)
            descripcionesItems = [item.getDescripcion() for item in itemsFiltrados]

    temasExistentes = Controller.obtenerTemas()
    return render_template('CRUDItems.html', temas=temasExistentes, temaFiltroItemModificar=temaFiltroModificar,
                           subtemasItemModificar=subtemasFiltrados, itemsFiltro = itemsFiltrados, descripItems = descripcionesItems)

@app.route("/CRUDIndiceDiscriminacion.html")
def crudIndiceDiscriminacion():

    listaTemas = Controller.obtenerTemas()
    return render_template("CRUDIndiceDiscriminacion.html", temas = listaTemas)

@app.route("/BuscarSubtemasItems", methods=['post'])
def buscarSubtemasItems():

    valor_boton = request.form.get("buscarItems")
    temaFiltroIndice = ""
    subtemasFiltrados = []
    itemsIndiceFiltrados = []
    descripcionesItems = []

    if(valor_boton == "Buscar"):
        subtemaFiltroIndice = request.form.get("subtemaIndice")

        itemsIndiceFiltrados = Controller.filtrarItems(subtemaFiltroIndice)

        descripcionesItems = [item.getDescripcion() for item in itemsIndiceFiltrados]

    else:
        temaFiltroIndice = request.form.get("selectBuscarTemaIndDis")
        subtemasFiltrados = Controller.filtrarSubtemas(temaFiltroIndice)

    listaTemas = Controller.obtenerTemas()

    return render_template("CRUDIndiceDiscriminacion.html", temas = listaTemas, subtemasItemIndice = subtemasFiltrados,
                           temaFiltroItemIndice = temaFiltroIndice,itemsFiltroIndice = itemsIndiceFiltrados,
                           descripItems = descripcionesItems)

@app.route("/agregarIndiceDiscriminacion", methods=['post'])
def agregarIndiceDiscriminacion(): #TODO, ACTUALIZAR TABLA SIN QUE SE REFRESQUE LA PAGINA
    nuevoIndice = request.form.get("addIndice")
    idItemModificar = request.form.get("idItemSecreto")

    print("PICHA" + str(idItemModificar))

    Controller.agregarIndice(idItemModificar,nuevoIndice)

    temasExistentes = Controller.obtenerTemas()
    return render_template("CRUDIndiceDiscriminacion.html", temas = temasExistentes)

@app.route("/modiEliIndiceDiscriminacion", methods=['post'])
def modEliIndiceDiscriminacion(): #TODO, ACTUALIZAR TABLA SIN QUE SE REFRESQUE LA PAGINA

    nuevoIndice = request.form.get("modIndice")
    idItemModificar = request.form.get("idItemSecreto")
    valor_boton = request.form.get("accionDiscriMod")

    if(valor_boton == "modificarIndice"):
        Controller.agregarIndice(idItemModificar,nuevoIndice)

    else:
        Controller.eliminarIndice(idItemModificar)

    temasExistentes = Controller.obtenerTemas()
    return render_template("CRUDIndiceDiscriminacion.html", temas = temasExistentes)

@app.route("/ConstruirExamen.html")

def construirExamen():

    return render_template("ConstruirExamen.html")

@app.route("/CRUDEncabezado.html")
def ventanaCRUDEncabezado():

    Periodos = Controller.obtenerPeriodos()
    Tipos = Controller.obtenerTExamen()
    return render_template("CRUDEncabezado.html", tiposExamen = Tipos, periodos = Periodos)

@app.route("/crudEncabezado",methods= ['post'])
def crudEncabezado():

    instrucciones = request.form.get("txtInstrucciones")
    periodo = request.form.get("selectPeriodo")
    anno = request.form.get("inputAño")
    tiempo = request.form.get("inputTiempo")
    tipo = request.form.get("selectTipo")

    if (opcionBoton == "PreviewEncabezado"):
        Controller.generarPreview(instrucciones,periodo,anno,tiempo,tipo)
    else:
        Controller.insertarNuevoEncabezado(instrucciones,periodo,anno,tiempo,tipo)



    Periodos = Controller.obtenerPeriodos()
    Tipos = Controller.obtenerTExamen()

    return render_template("CRUDEncabezado.html",tiposExamen = Tipos, periodos = Periodos)

@app.route("/CRUDRespuestas.html")
def ventanaCRUDRespuestas():
    listaTemas = Controller.obtenerTemas()
    return render_template("CRUDRespuestas.html", temas = listaTemas)

@app.route("/crudRespuestasAgregar", methods=['post']) ##Revisar
def crudRespuestasAgregar():

    valor_boton = request.form.get("respuestasAdd")

    temaFiltroRespuestas = ""
    subtemasFiltrados = []
    itemsFiltrados = []
    descripcionesItems = []

    if(valor_boton == "Agregar Respuestas"):
        itemSeleccionado = request.form.get("selectItemRespAgregar")
        respCorrecta = request.form.get("Arespuesta")
        respuestas = [request.form.get("Arespuesta1"),request.form.get("Arespuesta2"),request.form.get("Arespuesta3")
                      ,request.form.get("Arespuesta4")]

        Controller.agregarRespuestas(itemSeleccionado,respuestas,respCorrecta)

    else:
        if (request.form.get("selectSubAgregarResp") == None or request.form.get(
                "selectSubAgregarResp") == "Escoger Subtema"):

            temaFiltroRespuestas = request.form.get("selectTemaRespAgregar")
            subtemasFiltrados = Controller.filtrarSubtemas(temaFiltroRespuestas)

        else:
            subtemaFiltro = request.form.get("selectSubAgregarResp")
            itemsFiltrados = Controller.filtrarItemsSeleccion(subtemaFiltro) #TODO Y que no tengan respuestas
            descripcionesItems = [item.getDescripcion() for item in itemsFiltrados]

    listaTemas = Controller.obtenerTemas()
    return render_template("CRUDRespuestas.html",temas = listaTemas, subtemasAgregarResp = subtemasFiltrados,itemsAgregarResp = itemsFiltrados,
                           descripItemsAgregar = descripcionesItems, temaFiltroRespAgregar = temaFiltroRespuestas)

@app.route("/crudRespuestasModificar", methods=['post'])  ##Revisar
def crudRespuestasModificar():
    valor_boton = request.form.get("respuestasMod")

    temaFiltroRespuestas = ""
    itemRespuestasMod = ""
    subtemasFiltrados = []
    itemsFiltrados = []
    descripcionesItems = []
    objetoRespuesta = ""

    if (valor_boton == "Modificar Respuestas"):

        itemSeleccionado = request.form.get("selectItemRespModificar")
        respCorrecta = request.form.get("Mrespuesta")
        respuestas = [request.form.get("Mrespuesta1"), request.form.get("Mrespuesta2"), request.form.get("Mrespuesta3")
            , request.form.get("Mrespuesta4")]

        Controller.modificarRespuestas(itemSeleccionado,respuestas,respCorrecta)

    else:
        if (request.form.get("selectTemaRespModificar") =="Escoger Tema" and
        request.form.get("selectSubModificarResp") == "Escoger Subtema"):

            itemRespuestasMod = request.form.get("selectItemRespModificar")

            objetoRespuesta = Controller.obtenerRespuestasViejas(itemRespuestasMod)

        elif(request.form.get("selectSubModificarResp") == None or request.form.get(
                "selectSubModificarResp") == "Escoger Subtema"):

            temaFiltroRespuestas = request.form.get("selectTemaRespModificar")
            subtemasFiltrados = Controller.filtrarSubtemas(temaFiltroRespuestas)

        else:
            subtemaFiltro = request.form.get("selectSubModificarResp")
            itemsFiltrados = Controller.filtrarItemsSeleccion(subtemaFiltro)
            descripcionesItems = [item.getDescripcion() for item in itemsFiltrados]
            descripcionesItems.insert(0,"")
            session['descripItemsModificar'] = descripcionesItems

    listaTemas = Controller.obtenerTemas()

    return render_template("CRUDRespuestas.html", temas=listaTemas, subtemasModificarResp=subtemasFiltrados,
                           itemsModificarResp=itemsFiltrados,
                           descripItemsModificar=descripcionesItems, temaFiltroRespModificar=temaFiltroRespuestas,respViejas = objetoRespuesta,
                           itemSelectMod = itemRespuestasMod)


if __name__ == '__main__':

    app.run()
