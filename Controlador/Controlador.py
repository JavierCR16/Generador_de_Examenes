import datetime
from Gestores import GestorBase
from Gestores import GestorCorreo
from Gestores import GestorEncabezado
from Gestores import GestorExamenes
from Gestores import GestorIndiceDiscriminacion
from Gestores import GestorItems
from Gestores import GestorLaTeX
from Gestores import GestorPDF
from Gestores import GestorRespuestas
from Gestores import GestorTemasSubtemas
from Modelo.ObjetoItem import ObjetoItem
from Modelo.ObjetoSubtema import ObjetoSubtema
from Modelo.ObjetoTema import ObjetoTema
from Modelo.ObjetoTipoExamen import ObjetoTipoExamen
from Modelo.ObjetoPeriodo import ObjetoPeriodo
from Modelo.ObjetoUsuario import ObjetoUsuario


class Controlador:

    def __init__(self):
        pass

    def obtenerTemas(self):
        listaTemas = GestorBase.cargarTemas()
        listaTemas = [str(tema.getId())+"-"+tema.getTema() for tema in listaTemas]
        return ["Escoger Tema"]+listaTemas

    def insertarNuevoTema(self,temaNuevo):

        GestorBase.agregarTema(temaNuevo)

    def insertarNuevoSubtema(self,subtemaNuevo,temaSeleccionado):

        idTema =temaSeleccionado.split("-")[0]

        GestorBase.agregarSubtema(ObjetoSubtema(None,subtemaNuevo,idTema))

    def modificarTema(self,nuevoNombreTema,temaSeleccionado):

        idTema = temaSeleccionado.split("-")[0]

        GestorBase.modificarTema(ObjetoTema(idTema,nuevoNombreTema))

    def eliminarTema(self,temaSeleccionado):

        GestorBase.eliminarTema(temaSeleccionado.split("-")[0])

    def filtrarSubtemas(self,temaFiltro):
        listaSubtemas = GestorBase.filtrarSubtemas(temaFiltro.split("-")[0])
        listaSubtemas = [str(subtema.getId()) + "-" + subtema.getSubtema() for subtema in listaSubtemas]

        return ["Escoger Subtema"]+ listaSubtemas

    def modificarSubtema(self,subtemaSeleccionado, nuevoNombreSub):
        idSubtema = subtemaSeleccionado.split("-")[0]

        GestorBase.modificarSubtema(ObjetoSubtema(idSubtema,nuevoNombreSub,None))

    def eliminarSubtema(self,subAEliminar):
        idSubtema = subAEliminar.split("-")[0]
        GestorBase.eliminarSubtema(idSubtema)

    def agregarItem(self,descripcion,tipo,subtemaSeleccionado,puntaje):
        fechaActual =datetime.datetime.now()

        annoCreacion = fechaActual.year

        numSem = "I" if fechaActual.month <=6 else "II"
        idItem = numSem+" Sem-"+str(annoCreacion)+"-"+tipo

        idSubtema = subtemaSeleccionado.split("-")[0]


        GestorBase.agregarItem(ObjetoItem(idItem,descripcion,tipo,idSubtema,puntaje,None))
