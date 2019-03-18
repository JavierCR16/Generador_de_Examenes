import pymysql


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
    if(not nuevaConexion):

        try:
            with nuevaConexion.cursor() as usuarios:
                queryUsuarios = "SELECT nombreCompleto, correo FROM USUARIOS"

                usuarios.execute(queryUsuarios)

                for atributos in usuarios:
                    listaUsuarios += [[atributos[0],atributos[1]]]

        except:
            print("Error al cargar los usuarios.")

        finally:
            nuevaConexion.close()

    return listaUsuarios

def cargarPeriodoExamenes():

    nuevaConexion = establecerConexion()
    listaPeriodos = []
    if(not nuevaConexion):

        try:
            with nuevaConexion.cursor() as periodos:

                queryPeriodos = "SELECT id, descPeriodo FROM PERIODO"

                periodos.execute(queryPeriodos)

                for atributos in periodos:
                    listaPeriodos+= [[atributos[0],atributos[1]]]

        except:
            print("Error al cargar los periódos de examen")

        finally:
            nuevaConexion.close()

    return listaPeriodos

def cargarTipoExamenes():
    nuevaConexion = establecerConexion()

    listaTipos=[]

    if(not nuevaConexion):

        try:
            with nuevaConexion.cursor() as  tipoexamenes:
                queryTipos = "SELECT id, descTipo FROM TipoExamen"
                tipoexamenes.execute(queryTipos)

                for atributos in tipoexamenes:
                    listaTipos+= [[atributos[0],atributos[1]]]
        except:
            print("Error al cargar los periódos de examen")
        finally:
            nuevaConexion.close()

    return listaTipos

def cargarTemas():
    nuevaConexion = establecerConexion()

    listaTemas = []

    if (not nuevaConexion):

        try:
            with nuevaConexion.cursor() as  temas:
                queryTemas = "SELECT id, tema FROM Tema"
                temas.execute(queryTemas)

                for atributos in temas:
                    listaTemas += [[atributos[0], atributos[1]]]
        except:
            print("Error al cargar los temas de estudio")
        finally:
            nuevaConexion.close()

    return listaTemas

def filtrarSubtemas(idTema):
    nuevaConexion = establecerConexion()

    listaSubtemas = []

    if (not nuevaConexion):
        try:
            with nuevaConexion.cursor() as  subtemas:
                querySubtemas = "SELECT id, subtema FROM SubTema WHERE idTema = %s"
                subtemas.execute(querySubtemas,(idTema))

                for atributos in subtemas:
                    listaSubtemas += [[atributos[0], atributos[1]]]
        except:
            print("Error al filtrar los subtemas de estudio")
        finally:
            nuevaConexion.close()

    return listaSubtemas

def filtrarItems(idSubtema):
    nuevaConexion = establecerConexion()

    listaItems = []

    if (not nuevaConexion):
        try:
            with nuevaConexion.cursor() as items:
                queryitems = "SELECT id, descripcion,tipo, puntaje, indiceDiscriminacion FROM Item WHERE idSubtema = %s"
                items.execute(queryitems, (idSubtema))

                for atributos in items:
                    listaItems += [[atributos[0], atributos[1],atributos[2],atributos[3],atributos[4]]]
        except:
            print("Error al filtrar los subtemas de estudio")
        finally:
            nuevaConexion.close()

    return listaItems


