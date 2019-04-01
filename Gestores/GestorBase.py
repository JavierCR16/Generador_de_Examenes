import pymysql
from Modelo.ObjetoItem import ObjetoItem
from Modelo.ObjetoSubtema import ObjetoSubtema
from Modelo.ObjetoTema import ObjetoTema
from Modelo.ObjetoTipoExamen import ObjetoTipoExamen
from Modelo.ObjetoPeriodo import ObjetoPeriodo
from Modelo.ObjetoUsuario import ObjetoUsuario
from Modelo.ObjetoRespuesta import ObjetoRespuesta

#TODO AGREGAR A LA SECCION DE ENCABEZADO (BASE Y SISTEMA), LA OPCION DE METER ESCUELA Y CURSO.
#TODO AGREGAR FUNCIONES PARA CARGAR TODOS LOS ENCABEZADOS(PLANTILLAS) Y QUE ESTOS SEAN PREVISUALIZADOS POR EL USUARIO.
#TODO EN UN FUTURO, QUE LE PUEDA CAMBIAR EL TEMA ASOCIADO A UN SUBTEMA,AHORITA SI SE EQUIVOCA DI QUE LO BORRE.
#TODO EN UN FUTURO, QUE LE PUEDA CAMBIAR EL SUBTEMA ASOCIADO A UN ITEM,AHORITA SI SE EQUIVOCA DI QUE LO BORRE.
#TODO POR EJEMPLO EN AGREGAR ITEMS, TEMAS, SUBTEMAS, PODER AGREGAR VARIOS DE UN SOLO Y EN ITEMS LA POSIBILIDAD DE METER LAS RESPUESTAS DE UN SOLO
#TODO Intentar usar pylatex para el encabezado
#TODO Hacer la seccion de preview de plantillas y modificacion en el html de encabezado

#FUNCIONES DE CONEXION Y QUERIES
def establecerConexion():#usuario,password): #Definida por el momento como una conexion root, luego todas las conexiones deben hacerse a traves de los usuarios con los permisos respectivos.

    try:
        return pymysql.connect(host = '127.0.0.1', user = 'root', password = 'mySQLexamenes16', db = 'db_exam_it1')
    except Exception as e:

        print("Error de Conexión")

        return False

def obtenerInformacionItem(idItem):

    nuevaConexion = establecerConexion()
    objetoItem = ""
    if(nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as infoItem:
                queryItem = "SELECT id, descripcion, tipo,puntaje FROM Item WHERE idItem = %s"
                infoItem.execute(queryItem,(idItem))

                for atributos in infoItem:
                    objetoItem = ObjetoItem(idItem,atributos[0],atributos[1],atributos[2], None,atributos[3],None)

        except:
            print("Error al obtener la informacion del item")
        finally:
            nuevaConexion.close()
    return objetoItem

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
                queryitems = "SELECT idItem,id, descripcion,tipo, puntaje, indiceDiscriminacion FROM Item WHERE idSubtema = %s"
                items.execute(queryitems, (idSubtema))

                for atributos in items:
                    nuevoItem = ObjetoItem(atributos[0], atributos[1],atributos[2],atributos[3],idSubtema,atributos[4],atributos[5])
                    listaItems += [nuevoItem]
        except:
            print("Error al filtrar los subtemas de estudio")
        finally:
            nuevaConexion.close()

    return listaItems\

def filtrarItemsSeleccion(idSubtema):
    nuevaConexion = establecerConexion()
    listaItemsSeleccion = []

    if(nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as itemsSelect:

                queryItems = "SELECT idItem,id, descripcion,tipo, puntaje, indiceDiscriminacion FROM Item WHERE idSubtema = %s AND tipo = 'S' "

                itemsSelect.execute(queryItems,(idSubtema))

                for atributos in itemsSelect:
                    listaItemsSeleccion+= [ObjetoItem(atributos[0],atributos[1],
                                                      atributos[2],atributos[3],idSubtema,atributos[4],atributos[5])]

        except:
            print("Error al filtrar los ítems de selección única")
        finally:
            nuevaConexion.close()
    return listaItemsSeleccion

#AQUI EMPIEZA EL CRUD TEMAS SUBTEMAS
def agregarTema(nuevoTemaIngresado):
    nuevaConexion = establecerConexion()

    if(nuevaConexion.open):
        try:
            with nuevaConexion.cursor() as nuevoTema:

                insertTema = "INSERT INTO Tema (tema) VALUES(%s)"
                nuevoTema.execute(insertTema,(nuevoTemaIngresado))
                nuevaConexion.commit()
        except :

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
                nuevaConexion.commit()
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
                nuevaConexion.commit()
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
                nuevaConexion.commit()
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
                nuevaConexion.commit()
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
                nuevaConexion.commit()
        except:
            print("Error al eliminar el subtema")
        finally:
            nuevaConexion.close()


#AQUI EMPIEZA EL CRUD DE ITEMS
def agregarItem(nuevoObjetoItem):

    nuevaConexion = establecerConexion()

    if(nuevaConexion.open):
        try:
            with nuevaConexion.cursor() as nuevoItem:

                insertItem = "INSERT INTO Item (id, descripcion,tipo,idSubtema,puntaje) VALUES(%s,%s,%s,%s,%s)"
                nuevoItem.execute(insertItem,(nuevoObjetoItem.getIdLargo(),nuevoObjetoItem.getDescripcion(),
                                  nuevoObjetoItem.getTipo(),nuevoObjetoItem.getIdSubtema(),nuevoObjetoItem.getPuntaje()))
                nuevaConexion.commit()
        except Exception as e:
            print(e)
            print("Error al agregar un nuevo item")
        finally:
            nuevaConexion.close()

def modificarItem(objetoModItem):

    nuevaConexion = establecerConexion()

    if(nuevaConexion.open):
        try:

            with nuevaConexion.cursor() as itemModificar:

                updateItem = "UPDATE Item SET id = %s, descripcion = %s, tipo = %s, puntaje = %s WHERE idItem =%s"
                itemModificar.execute(updateItem,(objetoModItem.getIdLargo(),objetoModItem.getDescripcion(),objetoModItem.getTipo(),
                                                  objetoModItem.getPuntaje(),objetoModItem.getId()))
                nuevaConexion.commit()

        except Exception as e:
            print(e)
            print("Error al modificar el item")

        finally:
            nuevaConexion.close()

def eliminarItem(idItem):
    nuevaConexion = establecerConexion()

    if (nuevaConexion.open):
        try:

            with nuevaConexion.cursor() as itemEliminar:

                deleteItem = "DELETE FROM Item WHERE idItem = %s"
                itemEliminar.execute(deleteItem, (idItem))
                nuevaConexion.commit()

        except:
            print("Error al eliminar el item")

        finally:
            nuevaConexion.close()

#AQUI EMPIEZA EL CRUD DE RESPUESTAS
def agregarRespuestas(objetoRespuesta):         #REVISAR

    nuevaConexion = establecerConexion()
    cont = 1
    if (nuevaConexion.open):
        try:
            with nuevaConexion.cursor() as nuevaRespuesta:
                for newResp in objetoRespuesta.getRespuestas():
                    insertRespuesta = "INSERT INTO Respuestas (idItem, respuesta,respuestaCorrecta) VALUES(%s,%s,%s)"
                    nuevaRespuesta.execute(insertRespuesta, (objetoRespuesta.getIdItem(), newResp,"S")) if str(cont) == objetoRespuesta.getRespuestaCorrecta() else nuevaRespuesta.execute(insertRespuesta, (objetoRespuesta.getIdItem(), newResp,"N"))

                    nuevaConexion.commit()
                    cont+=1
        except Exception as e:
            print(e)
            print("Error al agregar una nueva respuesta")
        finally:
            nuevaConexion.close()

def filtrarRespuestasViejas(idItem):
    nuevaConexion = establecerConexion()
    objetoRespuesta = ObjetoRespuesta(idItem,None,None)
    if (nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as respViejas:

                queryRespuestas = "SELECT respuesta,respuestaCorrecta FROM Respuestas WHERE idItem = %s"

                respViejas.execute(queryRespuestas,(idItem))
                listaRespuestas =[]
                contador =1
                for atributos in respViejas:
                    if(atributos[1] == "S"):
                        objetoRespuesta.respCorrecta = str(contador)
                    contador+= 1

                    listaRespuestas+= [atributos[0]]
                objetoRespuesta.respuestas = listaRespuestas

        except:
            print("Error al obtener las respuestas del item")
        finally:
            nuevaConexion.close()

    return objetoRespuesta

def obtenerIdFilaRespuestas(idItem):
    nuevaConexion = establecerConexion()
    idExtraido = ""
    if(nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as idExtraer:
                queryID = "SELECT id from Respuestas WHERE idItem = %s LIMIT 1"
                idExtraer.execute(queryID,(idItem))

                for atributos in idExtraer:
                    idExtraido = atributos[0]
        except:
            print("Error al extraer el id")
        finally:
            nuevaConexion.close()

    return idExtraido

def modificarRespuestas(objetoModRespuesta):
    idFila = obtenerIdFilaRespuestas(objetoModRespuesta.getIdItem())
    ids = [idFila+i for i in range(0,4)]

    nuevaConexion = establecerConexion()

    if (nuevaConexion.open):
        try:
            with nuevaConexion.cursor() as respuestaModificar:

                contador = 1
                index = 0
                for modResp in objetoModRespuesta.getRespuestas():

                    modifyRespuesta = "UPDATE Respuestas SET respuesta = %s, respuestaCorrecta = %s WHERE id = %s"
                    respuestaModificar.execute(modifyRespuesta, (modResp,"S",
                                                             ids[index])) if str(contador) == objetoModRespuesta.getRespuestaCorrecta() else respuestaModificar.execute(modifyRespuesta, (modResp,"N",
                                                             ids[index]))
                    contador+=1
                    index+=1
                    nuevaConexion.commit()
        except Exception as e:
            print(e)
            print("Error al modificar una respuesta")
        finally:
            nuevaConexion.close()


#AQUI EMPIEZA EL CRUD DE INDICE DE DISCRIMINACION

def modificarIndice(objetoModIndice):

    nuevaConexion = establecerConexion()

    if (nuevaConexion.open):
        try:
            with nuevaConexion.cursor() as indiceModificar:

                modifyIndice = "UPDATE Item SET indiceDiscriminacion = %s WHERE idItem = %s"
                indiceModificar.execute(modifyIndice, (objetoModIndice.getIndice(), objetoModIndice.getId()))
                nuevaConexion.commit()
        except Exception as e:
            print(e)
            print("Error al modificar el indice")
        finally:
            nuevaConexion.close()

def eliminarIndice(idItem):
    nuevaConexion = establecerConexion()

    if (nuevaConexion.open):
        try:
            with nuevaConexion.cursor() as indiceEliminar:

                deleteIndice = "UPDATE Item SET indiceDiscriminacion = NULL WHERE idItem = %s"
                indiceEliminar.execute(deleteIndice, (idItem))
                nuevaConexion.commit()
        except Exception as e:
            print(e)
            print("Error al eliminar el indice")
        finally:
            nuevaConexion.close()

#AQUI EMPIEZA EL CRUD DE ENCABEZADO
def agregarEncabezado(objetoEncabezado):
    nuevaConexion = establecerConexion()

    if(nuevaConexion.open):

        try:
            with nuevaConexion.cursor() as nuevoEncabezado:
                insertEncabezado = "INSERT INTO Encabezado (curso,escuela,instrucciones,anno,tiempo,idPeriodo,idTipoExamen) VALUES(%a,%s,%s, %s, %s, %s, %s)"
                nuevoEncabezado.execute(insertEncabezado,(objetoEncabezado.getCurso(),objetoEncabezado.getEscuela(),
                                                          objetoEncabezado.getInstrucciones(),objetoEncabezado.getAnno(),
                                                          objetoEncabezado.getTiempo(),objetoEncabezado.getIdPeriodo(),
                                                          objetoEncabezado.getIdTipoExamen()))
                nuevaConexion.commit()
        except:
            print("Error al agregar un nuevo encabezado.")

        finally:
            nuevaConexion.close()