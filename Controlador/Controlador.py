import datetime
import symPy
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
from Modelo.ObjetoEncabezado import ObjetoEncabezado

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

    def agregarItem(self,descripcion,tipo,subtemaSeleccionado,puntaje): #TODO VALIDAR LA DESCRIPCION QUE TENGA BUEN FORMATO LATEX
        fechaActual =datetime.datetime.now()

        annoCreacion = fechaActual.year

        numSem = "I" if fechaActual.month <=6 else "II"
        idItem = numSem+" Sem-"+str(annoCreacion)+"-"+tipo

        idSubtema = subtemaSeleccionado.split("-")[0]

        GestorBase.agregarItem(ObjetoItem(None,idItem,descripcion,tipo,idSubtema,puntaje,None))

    def eliminarItem(self,itemSeleccionado):

        idItem = itemSeleccionado.split("/Item")[1]

        GestorBase.eliminarItem(idItem)

    def filtrarItems(self, subtemaSeleccionado):

        idSubtema = subtemaSeleccionado.split("-")[0]
        listaItems = GestorBase.filtrarItems(idSubtema)
        listaItems = [item.getIdLargo()+"/Item"+str(item.getId()) for item in listaItems]
        return listaItems

    def filtrarObjetoItems(self,subtemaSeleccionado):

        idSubtema = subtemaSeleccionado.split("-")[0]

        return GestorBase.filtrarItems(idSubtema)


    def modificarItem(self,itemModificarSeleccionado,tipoItem, descripcionModificar,puntajeModificar): #TODO VALIDAR LA DESCRIPCION QUE TENGA BUEN FORMATO LATEX


        idItem = itemModificarSeleccionado.split("/Item")[1]

        informacionItem = GestorBase.obtenerInformacionItem(idItem)

        listaidLargo = informacionItem.idLargo.split("-")

        listaidLargo[2] = tipoItem

        informacionItem.tipo = tipoItem

        informacionItem.idLargo = '-'.join(listaidLargo)

        informacionItem.descripcion = descripcionModificar if descripcionModificar != "" else informacionItem.descripcion

        informacionItem.puntaje = puntajeModificar if puntajeModificar != "" else informacionItem.puntaje

        GestorBase.modificarItem(informacionItem)

    #Funciones de encabezado
    def insertarNuevoEncabezado(self, nuevoEncabezado):
        GestorBase.agregarEncabezado(nuevoEncabezado)
    def previewDeEncabezado(self, nuevoEncabezado):

        LatexConfig = " \documentclass{exam} \usepackage[utf8]{inputenc} \begin{document} \maketitle "

        LatexWords = "\paragraph{Tecnologico de Costa Rica} \paragraph{ II Semestre, 2018} "

        LatexEnd = "\end{document}"


