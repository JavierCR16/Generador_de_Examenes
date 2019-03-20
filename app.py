from flask import Flask, render_template,request
from Controlador.Controlador import Controlador


app = Flask(__name__)
Controller = Controlador()

@app.route('/')
def main():
    return render_template('OpcionesPrincipales.html')#TODO Aqui que redireccione a la de login

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
    objetosItemsFiltrados = []

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
            objetosItemsFiltrados = [item .getDescripcion() for item in Controller.filtrarObjetoItems(subtemaFiltro)]

    temasExistentes = Controller.obtenerTemas()
    return render_template('CRUDItems.html', temas=temasExistentes, temaFiltroItemModificar=temaFiltroModificar,
                           subtemasItemModificar=subtemasFiltrados, itemsFiltro = itemsFiltrados, objetosItemsFil = objetosItemsFiltrados)

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

    if(valor_boton == "Buscar"):
        subtemaFiltro = request.form.get("subtemaIndice")

        itemsIndiceFiltrados = Controller.filtrarObjetoItems(subtemaFiltro)

    else:
        temaFiltroIndice = request.form.get("selectBuscarTemaIndDis")
        subtemasFiltrados = Controller.filtrarSubtemas(temaFiltroIndice)




    listaTemas = Controller.obtenerTemas()

    return render_template("CRUDIndiceDiscriminacion.html", temas = listaTemas, subtemasItemIndice = subtemasFiltrados,
                           temaFiltroItemIndice = temaFiltroIndice, itemsFiltroIndice = itemsIndiceFiltrados)


@app.route("/ConstruirExamen.html")

def construirExamen():

    return render_template("ConstruirExamen.html")

@app.route("/CRUDTemasSubtemas.html")
def ventanaCRUDTemasSubtemas():
    listaTemas = Controller.obtenerTemas()
    return render_template("CRUDTemasSubtemas.html", temas = listaTemas)


@app.route("/CRUDItems.html")
def ventanaCRUDItems():
    listaTemas = Controller.obtenerTemas()

    return render_template("CRUDItems.html", temas = listaTemas)

@app.route("/CRUDEncabezado.html")
def ventanaCRUDEncabezado():

    Periodos = Controller.obtenerPeriodos()
    Tipos = Controller.obtenerTExamen()
    return render_template("CRUDEncabezado.html", tiposExamen = Tipos, periodos = Periodos)

@app.route("/CRUDRespuestas.html")
def ventanaCRUDRespuestas():
    listaTemas = Controller.obtenerTemas()
    return render_template("CRUDRespuestas.html", temas = listaTemas)

@app.route("/crudRespuestasAgregar", methods=['post']) ##Revisar
def crudRespuestasAgregar():
    return render_template("CRUDRespuestas.html")

@app.route("/crudRespuestasModificar", methods=['post'])  ##Revisar
def crudRespuestasModificar():
    return render_template("CRUDRespuestas.html")

if __name__ == '__main__':

    app.run()
