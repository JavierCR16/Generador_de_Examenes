import json

def convertirListaAJSON(lista):
    arregloObjetos = []
    for objeto in lista:
        arregloObjetos.append(objeto.__dict__)
    return arregloObjetos

def convertirJsonSingleObject(objetoSimple):

    return json.dumps(objetoSimple)