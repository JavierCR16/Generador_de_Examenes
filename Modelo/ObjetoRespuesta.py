class ObjetoRespuesta:

    def __init__(self,idItem, listaRespuestas, numRespCorrecta):

        self.idItem = idItem
        self.respuestas = listaRespuestas
        self.respCorrecta  = numRespCorrecta

    def getIdItem(self):
        return self.idItem

    def getRespuestas(self):
        return self.respuestas

    def getRespuestaCorrecta(self):

        return self.respCorrecta
