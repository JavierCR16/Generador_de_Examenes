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

    def obtenerTemas(self,usuario,contrasenna):
        return GestorBase.cargarTemas(usuario,contrasenna)

    def filtrarSubtemas(self, temaFiltro,usuario,contrasenna):
        return GestorBase.filtrarSubtemas(temaFiltro.split("-")[0],usuario,contrasenna)

    def filtrarItems(self, subtemaSeleccionado,tipoFiltrado,usuario,contrasenna):

        idSubtema = subtemaSeleccionado.split("-")[0]
        listaItems = GestorBase.filtrarItems(idSubtema,tipoFiltrado,usuario,contrasenna)

        return listaItems

    def obtenerItemByID(self,itemSeleccionado,usuario,contrasenna):

        idItem = itemSeleccionado.split("/Item")[1]

        return GestorBase.obtenerInformacionItem(idItem,usuario,contrasenna)

    def filtrarItemsSeleccion(self,subtemaRespuestas,usuario,contrasenna):

        idSubtema = subtemaRespuestas.split("-")[0]

        return GestorBase.filtrarItemsSeleccion(idSubtema,usuario,contrasenna)

    def obtenerTExamen(self,usuario,contrasenna):
        return GestorBase.cargarTipoExamenes(usuario,contrasenna)

    def obtenerPeriodos(self,usuario,contrasenna):
        return GestorBase.cargarPeriodoExamenes(usuario,contrasenna)

    def insertarNuevoTema(self,temaNuevo,usuario,contrasenna):

        GestorBase.agregarTema(temaNuevo,usuario,contrasenna)

    def insertarNuevoSubtema(self,subtemaNuevo,temaSeleccionado,usuario,contrasenna):

        idTema =temaSeleccionado.split("-")[0]

        GestorBase.agregarSubtema(ObjetoSubtema(None,subtemaNuevo,idTema),usuario,contrasenna)

    def modificarTema(self,nuevoNombreTema,temaSeleccionado,usuario,contrasenna):

        idTema = temaSeleccionado.split("-")[0]

        GestorBase.modificarTema(ObjetoTema(idTema,nuevoNombreTema),usuario,contrasenna)

    def eliminarTema(self,temaSeleccionado,usuario,contrasenna):

        GestorBase.eliminarTema(temaSeleccionado.split("-")[0],usuario,contrasenna)

    def modificarSubtema(self,subtemaSeleccionado, nuevoNombreSub,usuario,contrasenna):
        idSubtema = subtemaSeleccionado.split("-")[0]

        GestorBase.modificarSubtema(ObjetoSubtema(idSubtema,nuevoNombreSub,None),usuario,contrasenna)

    def eliminarSubtema(self,subAEliminar,usuario,contrasenna):
        idSubtema = subAEliminar.split("-")[0]
        GestorBase.eliminarSubtema(idSubtema,usuario,contrasenna)

    def agregarItem(self,descripcion,tipo,subtemaSeleccionado,puntaje,usuario,contrasenna): #TODO VALIDAR LA DESCRIPCION QUE TENGA BUEN FORMATO LATEX
        fechaActual =datetime.datetime.now()

        annoCreacion = fechaActual.year

        numSem = "I" if fechaActual.month <=6 else "II"
        idItem = numSem+" Sem-"+str(annoCreacion)+"-"+tipo

        idSubtema = subtemaSeleccionado.split("-")[0]

        GestorBase.agregarItem(ObjetoItem(None,idItem,descripcion,tipo,idSubtema,puntaje,None),usuario,contrasenna)

    def eliminarItem(self,itemSeleccionado,usuario,contrasenna):

        idItem = itemSeleccionado.split("/Item")[1]

        GestorBase.eliminarItem(idItem,usuario,contrasenna)

    def modificarItem(self,itemModificarSeleccionado,tipoItem, descripcionModificar,puntajeModificar,usuario,contrasenna): #TODO VALIDAR LA DESCRIPCION QUE TENGA BUEN FORMATO LATEX

        idItem = itemModificarSeleccionado.split("/Item")[1]

        informacionItem = GestorBase.obtenerInformacionItem(idItem,usuario,contrasenna)

        listaidLargo = informacionItem.idLargo.split("-")

        listaidLargo[2] = tipoItem

        informacionItem.tipo = tipoItem

        informacionItem.idLargo = '-'.join(listaidLargo)

        informacionItem.descripcion = descripcionModificar if descripcionModificar != "" else informacionItem.descripcion

        informacionItem.puntaje = puntajeModificar if puntajeModificar != "" else informacionItem.puntaje

        GestorBase.modificarItem(informacionItem,usuario,contrasenna)

    def comprobarConexion(self,user,contra):
        return GestorBase.establecerConexion(user,contra)

    def cerrarConexion(self,objetoConexion):

        GestorBase.cerrarConexion(objetoConexion)


    #Funciones Indice Discriminacion
    def agregarIndice(self,idItem, nuevoIndice,usuario,contrasenna):
        objetoItem = ObjetoItem(idItem,None,None,None,None,None,nuevoIndice)

        GestorBase.modificarIndice(objetoItem,usuario,contrasenna)

    def eliminarIndice(self,idItem,usuario,contrasenna):

        GestorBase.eliminarIndice(idItem,usuario,contrasenna)

    #Funciones de encabezado
    def insertarNuevoEncabezado(self,curso,escuela,instrucciones ,periodo,fecha,tiempo,tipo,usuario,contrasenna):
        periodoId = periodo.split('-')[0]
        tipoId= tipo.split('-')[0]
        anno = fecha.split('-')[0]

        nuevoEncabezado=ObjetoEncabezado(curso,escuela,instrucciones,anno,tiempo,periodoId,tipoId)

        GestorBase.agregarEncabezado(nuevoEncabezado,usuario,contrasenna)

    def generarPreview(self,curso,escuela,instrucciones ,periodo,fecha,tiempo,tipo):
        periodo= periodo.split('-')[1]
        tipo = tipo.split('-')[1]
        fecha = fecha.split("-")[0]

        nuevoEncabezado = ObjetoEncabezado(curso,escuela,instrucciones, fecha, tiempo,periodo, tipo)
        GestorEncabezado.previewEncabezado(nuevoEncabezado)


    #Funciones Gestion Respuestas
    def agregarRespuestas(self,itemSeleccionado, listaRespuestas, respCorrecta,usuario,contrasenna):
        idItem = itemSeleccionado.split("/Item")[1]

        objetoRespuesta = ObjetoRespuesta(idItem,listaRespuestas,respCorrecta)

        GestorBase.agregarRespuestas(objetoRespuesta,usuario,contrasenna)

    def obtenerRespuestasViejas(self,itemSeleccionado,usuario,contrasenna):

        idItem = itemSeleccionado.split("/Item")[1]

        return GestorBase.filtrarRespuestasViejas(idItem,usuario,contrasenna)

    def modificarRespuestas(self,itemSeleccionado,listaRespuestas,respCorrecta,usuario,contrasenna):

        idItem = itemSeleccionado.split("/Item")[1]

        objetoRespuesta = ObjetoRespuesta(idItem, listaRespuestas, respCorrecta)

        GestorBase.modificarRespuestas(objetoRespuesta,usuario,contrasenna)

    #Funciones JSON

    def convertirSubtemasJson(self,listaSubtemas):

        return GestorJSON.convertirListaAJSON(listaSubtemas)

    def convertirItemsJson(self,listaItems):

        return GestorJSON.convertirListaAJSON(listaItems)

    def convertirJson(self,objetoSimple):

        return GestorJSON.convertirJsonSingleObject(objetoSimple)

    #Funciones Sugerencia Edicion

    def enviarSugerencia(self,idItem,nuevaEdicion, comentarios, usuario,contrasenna):

        GestorBase.enviarSugerencia(idItem,nuevaEdicion,comentarios,usuario,contrasenna)

