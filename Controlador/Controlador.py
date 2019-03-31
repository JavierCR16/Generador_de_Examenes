import datetime
#from sympy import preview
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
from Gestores import GestorJSON
from Modelo.ObjetoItem import ObjetoItem
from Modelo.ObjetoSubtema import ObjetoSubtema
from Modelo.ObjetoTema import ObjetoTema
from Modelo.ObjetoTipoExamen import ObjetoTipoExamen
from Modelo.ObjetoPeriodo import ObjetoPeriodo
from Modelo.ObjetoUsuario import ObjetoUsuario
from Modelo.ObjetoEncabezado import ObjetoEncabezado
from Modelo.ObjetoRespuesta import ObjetoRespuesta

class Controlador:

    def __init__(self):
        pass

    def obtenerTemas(self):
        return GestorBase.cargarTemas()

    def filtrarSubtemas(self, temaFiltro):
        return GestorBase.filtrarSubtemas(temaFiltro.split("-")[0])

    def filtrarItems(self, subtemaSeleccionado):

        idSubtema = subtemaSeleccionado.split("-")[0]
        listaItems = GestorBase.filtrarItems(idSubtema)

        return listaItems

    def obtenerItemByID(self,itemSeleccionado):

        idItem = itemSeleccionado.split("/Item")[1]

        return GestorBase.obtenerInformacionItem(idItem)

    def filtrarItemsSeleccion(self,subtemaRespuestas):

        idSubtema = subtemaRespuestas.split("-")[0]

        return GestorBase.filtrarItemsSeleccion(idSubtema)

    def obtenerTExamen(self):
        return GestorBase.cargarTipoExamenes()

    def obtenerPeriodos(self):
        return GestorBase.cargarPeriodoExamenes()

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


    #Funciones Indice Discriminacion
    def agregarIndice(self,idItem, nuevoIndice):
        objetoItem = ObjetoItem(idItem,None,None,None,None,None,nuevoIndice)

        GestorBase.modificarIndice(objetoItem)

    def eliminarIndice(self,idItem):

        GestorBase.eliminarIndice(idItem)

    #Funciones de encabezado
    def insertarNuevoEncabezado(self, nuevoEncabezado):
        GestorBase.agregarEncabezado(nuevoEncabezado)

    def previewEncabezado(self):

        #Aqui poner todo lo del objeto
        LatexWords = "\\paragraph{Tecnologico de Costa Rica} \\paragraph{ II Semestre, 2018} "

        preview(LatexWords , viewer = "file",filename= "static/Preview.png")

    #Funciones Gestion Respuestas
    def agregarRespuestas(self,itemSeleccionado, listaRespuestas, respCorrecta):
        idItem = itemSeleccionado.split("/Item")[1]

        objetoRespuesta = ObjetoRespuesta(idItem,listaRespuestas,respCorrecta)

        GestorBase.agregarRespuestas(objetoRespuesta)

    def obtenerRespuestasViejas(self,itemSeleccionado):

        idItem = itemSeleccionado.split("/Item")[1]

        return GestorBase.filtrarRespuestasViejas(idItem)

    def modificarRespuestas(self,itemSeleccionado,listaRespuestas,respCorrecta):

        idItem = itemSeleccionado.split("/Item")[1]

        objetoRespuesta = ObjetoRespuesta(idItem, listaRespuestas, respCorrecta)

        GestorBase.modificarRespuestas(objetoRespuesta)

    #Funciones JSON

    def convertirSubtemasJson(self,listaSubtemas):

        return GestorJSON.convertirListaAJSON(listaSubtemas)

    def convertirItemsJson(self,listaItems):

        return GestorJSON.convertirListaAJSON(listaItems)

    def convertirJson(self,objetoSimple):

        return GestorJSON.convertirJsonSingleObject(objetoSimple)

