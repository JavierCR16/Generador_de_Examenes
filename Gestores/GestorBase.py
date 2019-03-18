import pymysql


def establecerConexion():#usuario,password): #Definida por el momento como una conexion root, luego todas las conexiones deben hacerse a traves de los usuarios con los permisos respectivos.

    try:
        return pymysql.connect(host = '127.0.0.1', user = 'root', password = 'mySQLexamenes16', db = 'db_exam_it1')
    except Exception as e:

        print("Error de Conexión")

        return "ERROR"

def cerrarConexion(objetoConexion):
    objetoConexion.close()

def cargarUsuarios():

    nuevaConexion = establecerConexion()

    if(isinstance(nuevaConexion,pymysql.Connection)):

        listaUsuarios = []
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

def cargarPeriodoExamenes:

def cargarTipoExamenes:

def cargarTemas:

def cargarSubtemas: