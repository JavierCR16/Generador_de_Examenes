from flask import Flask, render_template,request
from Controlador.Controlador import Controlador

app = Flask(__name__)
Controller = Controlador()

@app.route('/')
def main():
    temasExistentes = Controller.obtenerTemas() #CRUDTemasSubtemas.html
    return render_template('CRUDItems.html',temas = temasExistentes)#TODO Aqui que redireccione a la de login

@app.route('/Encabezado')
def Encabezado():
    return render_template('Encabezado.html')

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

    if(valor_boton == "Modificar Item"):
        return None

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



    temasExistentes = Controller.obtenerTemas()
    return render_template('CRUDItems.html', temas=temasExistentes, temaFiltroItemModificar=temaFiltroModificar,
                           subtemasItemModificar=subtemasFiltrados, itemsFiltro = itemsFiltrados)
if __name__ == '__main__':

    app.run()
