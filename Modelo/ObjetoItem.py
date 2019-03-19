class ObjetoItem:
    def __init__(self,id,idLargo, descripcion, tipo, idSubtema,puntaje, indiceDiscriminacion):
        self.id = id
        self.idLargo = idLargo
        self.descripcion = descripcion
        self.tipo = tipo
        self.idSubtema = idSubtema
        self.puntaje = puntaje
        self.indiceDiscriminacion = indiceDiscriminacion

    def getId(self):
        return self.id

    def getIdLargo(self):
        return self.idLargo

    def getDescripcion(self):
        return self.descripcion

    def getTipo(self):
        return self.tipo

    def getIdSubtema(self):
        return self.idSubtema

    def getPuntaje(self):
        return self.puntaje

    def getIndice(self):
        return self.indiceDiscriminacion
