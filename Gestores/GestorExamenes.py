from collections import defaultdict
from Modelo.ObjetoItem import ObjetoItem
from Modelo.ObjetoSubtema import ObjetoSubtema
from Modelo.ObjetoTema import ObjetoTema

def informacionExamen(respuestaTuplas):
    group = defaultdict(list)
    listaItem = []

    temas = []
    subtemas = []
    items = []

    for tupla in respuestaTuplas:
        group[tupla[0]].append(tupla)

    for key in group:
        listaSubtemas = []
        subtemaActual = 0
        executed = False

        for tupla in group[key]:

            if (not executed):
                temas.append(ObjetoTema(key, tupla[1]))
                subtemaActual = tupla[2] #Lo ejecuta solo la primera vez
                executed = True

            if(not any(subtema.getId() == tupla[2] for subtema in listaSubtemas)):
                listaSubtemas.append(ObjetoSubtema(tupla[2], tupla[3], None))

            if(subtemaActual != tupla[2]):
                items.append(listaItem.copy())
                listaItem.clear()

            listaItem.append(ObjetoItem(tupla[4], tupla[5], tupla[6], tupla[7], None, tupla[8], None))

            subtemaActual = tupla[2]

        items.append(listaItem.copy())
        listaItem.clear()
        subtemas.append(listaSubtemas)

    return temas,subtemas,items
