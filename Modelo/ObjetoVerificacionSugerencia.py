class ObjetoVerificacionSugerencia:

    def __init__(self,idItem,idItemLargo,tipoItem,puntaje,tema, subtema,usuarioSugeridor):
        self.id = idItem
        self.idLargo = idItemLargo
        self.tipo = tipoItem
        self.puntaje = puntaje
        self.tema = tema
        self.subtema = subtema
        self.usuario = usuarioSugeridor


    def getId(self):
        return self.id

    def getIdLargo(self):
        return self.idLargo

    def getTipo(self):
        return self.tipo

    def getPuntaje(self):
        return self.puntaje

    def getTema(self):
        return self.tema

    def getSubtema(self):
        return self.subtema

    def getUsuario(self):
        return self.usuario
