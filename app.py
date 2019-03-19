from flask import Flask, render_template,request
from Controlador.Controlador import Controlador

app = Flask(__name__)
Controller = Controlador()

@app.route('/')
def main():
    temasExistentes = Controller.obtenerTemas()
    return render_template('CRUDTemasSubtemas.html',temas = temasExistentes)#TODO Aqui que redireccione a la de login

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


if __name__ == '__main__':

    app.run()
