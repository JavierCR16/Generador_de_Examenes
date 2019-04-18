import json
from Modelo.ObjetoEncabezado import ObjetoEncabezado

def convertirListaAJSON(lista):
    arregloObjetos = []
    for objeto in lista:
        arregloObjetos.append(objeto.__dict__)
    return arregloObjetos

def convertirJsonSingleObject(objetoSimple):

    return json.dumps(objetoSimple)

def convertirMatrixJSON(matriz):
    filaNueva = []
    matrizNueva = []

    for fila in matriz:
        for objeto in fila:
            filaNueva.append(objeto.__dict__)
        matrizNueva.append(filaNueva.copy())
        filaNueva.clear()

    return matrizNueva

def convertirDictAObjeto(stringDict):

    diccionario = eval(stringDict)

    return ObjetoEncabezado(**diccionario)

