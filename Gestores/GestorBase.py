import pymysql
from Modelo.ObjetoItem import ObjetoItem
from Modelo.ObjetoSubtema import ObjetoSubtema
from Modelo.ObjetoTema import ObjetoTema
from Modelo.ObjetoTipoExamen import ObjetoTipoExamen
from Modelo.ObjetoPeriodo import ObjetoPeriodo
from Modelo.ObjetoUsuario import ObjetoUsuario
#TODO AGREGAR A LA SECCION DE ENCABEZADO BASE Y SISTEMA, LA OPCION DE METER ESCUELA Y CURSO.
#TODO AGREGAR FUNCIONES PARA CARGAR TODOS LOS ENCABEZADOS(PLANTILLAS) Y QUE ESTOS SEAN PREVISUALIZADOS POR EL USUARIO.
#TODO EN UN FUTURO, QUE LE PUEDA CAMBIAR EL TEMA ASOCIADO A UN SUBTEMA,AHORITA SI SE EQUIVOCA DI QUE LO BORRE.
#TODO EN UN FUTURO, QUE LE PUEDA CAMBIAR EL SUBTEMA ASOCIADO A UN ITEM,AHORITA SI SE EQUIVOCA DI QUE LO BORRE.

def establecerConexion():#usuario,password): #Definida por el momento como una conexion root, luego todas las conexiones deben hacerse a traves de los usuarios con los permisos respectivos.

    try:
        return pymysql.connect(host = '127.0.0.1', user = 'root', password = 'mySQLexamenes16', db = 'db_exam_it1')
    except Exception as e:

        print("Error de Conexión")

        return False

def cerrarConexion(objetoConexion):
    objetoConexion.close()

def cargarUsuarios():

    nuevaConexion = establecerConexion()
    listaUsuarios = []
    if(nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as usuarios:
                queryUsuarios = "SELECT nombreCompleto, correo FROM USUARIOS"

                usuarios.execute(queryUsuarios)

                for atributos in usuarios:
                    nuevoUsuario = ObjetoUsuario(atributos[0],atributos[1])
                    listaUsuarios += [nuevoUsuario]

        except:
            print("Error al cargar los usuarios.")

        finally:
            nuevaConexion.close()

    return listaUsuarios

def cargarPeriodoExamenes():

    nuevaConexion = establecerConexion()
    listaPeriodos = []
    if(nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as periodos:

                queryPeriodos = "SELECT id, descPeriodo FROM PERIODO"

                periodos.execute(queryPeriodos)

                for atributos in periodos:
                    nuevoPeriodo = ObjetoPeriodo(atributos[0],atributos[1])

                    listaPeriodos+= [nuevoPeriodo]

        except:
            print("Error al cargar los periódos de examen")

        finally:
            nuevaConexion.close()

    return listaPeriodos

def cargarTipoExamenes():
    nuevaConexion = establecerConexion()

    listaTipos=[]

    if(nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as  tipoexamenes:
                queryTipos = "SELECT id, descTipo FROM TipoExamen"
                tipoexamenes.execute(queryTipos)

                for atributos in tipoexamenes:
                    nuevoTipoExamen = ObjetoTipoExamen(atributos[0],atributos[1])
                    listaTipos+= [nuevoTipoExamen]
        except:
            print("Error al cargar los periódos de examen")
        finally:
            nuevaConexion.close()

    return listaTipos

def cargarTemas():
    nuevaConexion = establecerConexion()

    listaTemas = []

    if (nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as  temas:
                queryTemas = "SELECT id, tema FROM Tema"
                temas.execute(queryTemas)

                for atributos in temas:
                    nuevoTema = ObjetoTema(atributos[0],atributos[1])
                    listaTemas += [nuevoTema]
        except:
            print("Error al cargar los temas de estudio")
        finally:
            nuevaConexion.close()

    return listaTemas

def filtrarSubtemas(idTema):
    nuevaConexion = establecerConexion()

    listaSubtemas = []

    if (nuevaConexion.open):
        try:
            with nuevaConexion.cursor() as  subtemas:
                querySubtemas = "SELECT id, subtema FROM SubTema WHERE idTema = %s"
                subtemas.execute(querySubtemas,(idTema))

                for atributos in subtemas:
                    nuevoSubtema = ObjetoSubtema(atributos[0],atributos[1],idTema)
                    listaSubtemas += [nuevoSubtema]
        except:
            print("Error al filtrar los subtemas de estudio")
        finally:
            nuevaConexion.close()

    return listaSubtemas

def filtrarItems(idSubtema):
    nuevaConexion = establecerConexion()

    listaItems = []

    if (nuevaConexion.open):
        try:
            with nuevaConexion.cursor() as items:
                queryitems = "SELECT id, descripcion,tipo, puntaje, indiceDiscriminacion FROM Item WHERE idSubtema = %s"
                items.execute(queryitems, (idSubtema))

                for atributos in items:
                    nuevoItem = ObjetoItem(atributos[0], atributos[1],atributos[2],idSubtema,atributos[3],atributos[4])
                    listaItems += [nuevoItem]
        except:
            print("Error al filtrar los subtemas de estudio")
        finally:
            nuevaConexion.close()

    return listaItems

def agregarEncabezado(objetoEncabezado):
    nuevaConexion = establecerConexion()

    if(nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as nuevoEncabezado:
                insertEncabezado = "INSERT INTO Encabezado (instrucciones,anno,tiempo,idPeriodo,idTipoExamen) VALUES(%s, %s, %s, %s, %s)"
                nuevoEncabezado.execute(insertEncabezado,(objetoEncabezado.getInstrucciones(),objetoEncabezado.getAnno(),
                                                          objetoEncabezado.getTiempo(),objetoEncabezado.getIdPeriodo(),
                                                          objetoEncabezado.getIdTipoExamen()))

        except:
            print("Error al agregar un nuevo encabezado.")

        finally:
            nuevaConexion.close()

def agregarTema(nuevoTemaIngresado):
    nuevaConexion = establecerConexion()

    if(nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as nuevoTema:

                insertTema = "INSERT INTO Tema (tema) VALUES(%s)"
                nuevoTema.execute(insertTema,(nuevoTemaIngresado))
        except:
            print("Error al agregar un nuevo tema")
        finally:
            nuevaConexion.close()

def agregarSubtema(nuevoObjetoSubtema):

    nuevaConexion = establecerConexion()

    if(nuevaConexion.open):
        try:
            with nuevaConexion.cursor() as nuevoSubtema:
                insertSubtema = "INSERT INTO Subtema (subtema,idTema) VALUES (%s,%s)"
                nuevoSubtema.execute(insertSubtema,(nuevoObjetoSubtema.getSubtema(),
                                                    nuevoObjetoSubtema.getIdTema()))
        except:
            print("Error al agregar un nuevo subtema")
        finally:
            nuevaConexion.close()

def modificarTema(objetoModTema):

    nuevaConexion = establecerConexion()

    if(nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as temaModificar:

                updateTema = "UPDATE Tema set tema = %s WHERE id = %s"
                temaModificar.execute(updateTema,(objetoModTema.getTema(),
                                                  objetoModTema.getId()))
        except:
            print("Error al modificar el tema")

        finally:
            nuevaConexion.close()

def eliminarTema(idTema):
    nuevaConexion = establecerConexion()

    if (nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as temaEliminar:

                deleteTema = "DELETE FROM Tema WHERE id = %s"
                temaEliminar.execute(deleteTema, (idTema))
        except:
            print("Error al eliminar el tema")

        finally:
            nuevaConexion.close()

def modificarSubtema(objetoModSubtema):

    nuevaConexion = establecerConexion()

    if (nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as subtemaModificar:
                modifySubtema = "UPDATE Subtema SET subtema = %s WHERE id = %s"
                subtemaModificar.execute(modifySubtema, (objetoModSubtema.getSubtema(),
                                                         objetoModSubtema.getId()))
        except:
            print("Error al modificar el subtema")
        finally:
            nuevaConexion.close()


def eliminarSubtema(idSubtema):

    nuevaConexion = establecerConexion()

    if(nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as subtemaEliminar:
                deleteSubtema = "DELETE FROM Subtema WHERE id = %s"
                subtemaEliminar.execute(deleteSubtema, (idSubtema))
        except:
            print("Error al eliminar el subtema")
        finally:
            nuevaConexion.close()
