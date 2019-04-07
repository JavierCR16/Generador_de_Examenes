from collections import defaultdict
from Modelo.ObjetoItem import ObjetoItem
from Modelo.ObjetoSubtema import ObjetoSubtema

def informacionExamen(respuestaTuplas):
    group = defaultdict(list)
    subtemas = []
    items = []

    for tupla in respuestaTuplas:
        group[tupla[0]].append(tupla)

    for key in group:

        listaItem = []
        executed = False
        for tupla in group[key]:
            if(not executed):
                subtemas.append(ObjetoSubtema(key,tupla[1],None))
                executed = True

            listaItem.append(ObjetoItem(tupla[2],tupla[3],tupla[4],None,None,tupla[5],None))

        items.append(listaItem)


    return subtemas,items