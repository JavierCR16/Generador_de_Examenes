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
from Gestores import GestorLaTeX
from Gestores import GestorJSON
from Modelo.ObjetoItem import ObjetoItem
from Modelo.ObjetoSubtema import ObjetoSubtema
from Modelo.ObjetoTema import ObjetoTema
from Modelo.ObjetoTipoExamen import ObjetoTipoExamen
from Modelo.ObjetoPeriodo import ObjetoPeriodo
from Modelo.ObjetoUsuario import ObjetoUsuario
from Modelo.ObjetoEncabezado import ObjetoEncabezado
from Modelo.ObjetoRespuesta import ObjetoRespuesta
from Modelo.ObjetoSugerencia import ObjetoSugerencia
from Modelo.ObjetoExamen import ObjetoExamen

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

    def filtrarItemsRespuestas(self,subtemaSeleccionado, tipoFiltrado, usuario, contrasenna):

        idSubtema = subtemaSeleccionado.split("-")[0]

        listaItems = GestorBase.filtrarItemsRespuestas(idSubtema,tipoFiltrado,usuario,contrasenna)

        return listaItems

    def obtenerItemByID(self,itemSeleccionado,usuario,contrasenna):

        idItem = itemSeleccionado.split("/Item")[1]

        return GestorBase.obtenerInformacionItem(idItem,usuario,contrasenna)

    def filtrarItemsSeleccion(self,subtemaRespuestas,usuario,contrasenna): #FIXME NOT IN USE.

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

        nuevoEncabezado=ObjetoEncabezado(None,curso,escuela,instrucciones,anno,tiempo,periodoId,tipoId)

        GestorBase.agregarEncabezado(nuevoEncabezado,usuario,contrasenna)

    def generarPreview(self,curso,escuela,instrucciones ,periodo,fecha,tiempo,tipo,usuario):
        periodo= periodo.split('-')[1]
        tipo = tipo.split('-')[1]
        fecha = fecha.split("-")[0]

        nuevoEncabezado = ObjetoEncabezado(None,curso,escuela,instrucciones, fecha, tiempo,periodo, tipo)

        return GestorEncabezado.previewEncabezado(nuevoEncabezado,usuario)

    def obtenerEncabezados(self,usuario,contrasenna):

        return GestorBase.cargarEncabezados(usuario,contrasenna)

    #Funciones Gestion Respuestas
    def agregarRespuestas(self,itemSeleccionado,listaRespuestas, respCorrecta,usuario,contrasenna):
        idItem = itemSeleccionado.split("/Item")[1]

        objetoRespuesta = ObjetoRespuesta(idItem,listaRespuestas,int(respCorrecta))

        GestorBase.agregarRespuestas(objetoRespuesta,usuario,contrasenna)

    def obtenerRespuestasViejas(self,itemSeleccionado,usuario,contrasenna):

        idItem = itemSeleccionado.split("/Item")[1]

        return GestorBase.filtrarRespuestasViejas(idItem,usuario,contrasenna)

    def modificarRespuestas(self,itemSeleccionado,listaRespuestas,respCorrecta,usuario,contrasenna):

        idItem = itemSeleccionado.split("/Item")[1]

        objetoRespuesta = ObjetoRespuesta(idItem, listaRespuestas, int(respCorrecta))

        GestorBase.modificarRespuestas(objetoRespuesta,usuario,contrasenna)

    def obtenerRespuestasExamen(self,listaIdItems,usuario,contrasenna):

        listaRespuestas = []

        for id in listaIdItems:
            listaRespuestas.append(GestorBase.filtrarRespuestasViejas(id,usuario,contrasenna))

        return listaRespuestas

    #Funciones JSON

    def convertirSubtemasJson(self,listaSubtemas):

        return GestorJSON.convertirListaAJSON(listaSubtemas)

    def convertirItemsJson(self,listaItems):

        return GestorJSON.convertirListaAJSON(listaItems)

    def convertirMatrixJSON(self,matriz):

        return GestorJSON.convertirMatrixJSON(matriz)

    def convertirJson(self,objetoSimple):

        return GestorJSON.convertirJsonSingleObject(objetoSimple)

    def convertirDictAObjeto(self,stringDict):

        return GestorJSON.convertirDictAObjeto(stringDict)

    #Funciones Sugerencia y Verificacion Edicion

    def enviarSugerencia(self,idItem,nuevaEdicion, comentarios, usuario,contrasenna):

        objetoSugerencia = ObjetoSugerencia(idItem,nuevaEdicion,comentarios,usuario)

        GestorBase.enviarSugerencia(objetoSugerencia,contrasenna)

    def filtrarSugerencias(self,usuario,contrasenna):

        return GestorBase.filtrarSugerencias(usuario,contrasenna)

    def rechazarSugerencia(self,idSugerencia,usuario,contrasenna):

        GestorBase.rechazarSugerencia(idSugerencia,usuario,contrasenna)

    def aprobarSugerencia(self,idSugerencia,sugerencia,idItem,usuario,contrasenna):

        GestorBase.aprobarSugerencia(idSugerencia,sugerencia,idItem,usuario,contrasenna)

    #Funciones Construir Examen
    def loadInformacionExamen(self,tipoExamen,usuario,contrasenna):

        return GestorBase.loadInformacionGenerarExamen(tipoExamen,usuario,contrasenna)

    #Funciones Compartir Examenes
    def cargarUsuarios(self,usuario,contrasenna):

        return GestorBase.cargarUsuarios(usuario,contrasenna)

    def enviarExamen(self,usuarioLogueado,asunto,cuerpo,examenes,listaCorreos):

        GestorCorreo.enviarExamen(usuarioLogueado,asunto,cuerpo,examenes,listaCorreos)

    def getNombreUsuario(self,usuario,contrasenna):

        return GestorBase.getNombreUsuario(usuario,contrasenna)

    #Funciones Generar Examen

    def generarExamen(self,objEncabezado,items,respuestas,tipoExamen,conSolucion,puntajes):
        objEncabezado.idPeriodo =  objEncabezado.getIdPeriodo().split('-')[1]
        objEncabezado.idTipoExamen = objEncabezado.getIdTipoExamen().split('-')[1]
        objEncabezado.anno = objEncabezado.getAnno().split("-")[0]

        return GestorLaTeX.generarExamen(objEncabezado,items,respuestas,tipoExamen,conSolucion,puntajes)

    def guardarExamen(self,encabezado,tipoExamen,archivoPDF,idItems,usuario,contrasenna):

        fechaCreacion = datetime.datetime.now()
        fechaParseada = str(fechaCreacion.strftime("%Y/%m/%d"))

        with open(archivoPDF,'rb') as f: archivoPDF= f.read()

        objetoExamen = ObjetoExamen(None,encabezado,tipoExamen,fechaParseada,usuario,archivoPDF,idItems)

        GestorBase.guardarExamen(objetoExamen,usuario,contrasenna)

    def obtenerExamenes(self,usuario,contrasenna):

        return GestorBase.obtenerExamenes(usuario,contrasenna)

    def descargarExamen(self,idExamen,usuario,contrasenna):

        return GestorBase.descargarExamen(idExamen,usuario,contrasenna)

    #Funciones Estadisticas

    def obtenerEstadisticas(self,usuario,contrasenna,idEstadistica,idItem):
        resultado = ""

        if(idEstadistica == 1): #Frecuencia de Uso
            resultado = GestorBase.obtenerCantVecesItem(usuario,contrasenna,idItem)
        elif(idEstadistica == 2):#Lista de Semestres en los que se ha usado
            resultado = GestorBase.obtenerListaSemestresItem(usuario,contrasenna,idItem)
        else: #Cantidad de Uso en ambos semestres
            resultado = GestorBase.obtenerCantidadSugerenciasItem(usuario,contrasenna,idItem)

        return resultado

    def obtenerItemsModalidad(self,usuario,contrasenna):

        return GestorBase.obtenerItemsModalidad(usuario,contrasenna)