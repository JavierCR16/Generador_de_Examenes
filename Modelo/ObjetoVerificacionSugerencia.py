class ObjetoVerificacionSugerencia:

    def __init__(self,idItem,idItemLargo,descripcionItem,tipoItem,puntaje,tema, subtema,sugerencia,comentarios,idSugerencia,usuarioSugeridor):

        self.id = idItem
        self.idLargo = idItemLargo
        self.descripcionItem = descripcionItem
        self.tipo = tipoItem
        self.puntaje = puntaje
        self.tema = tema
        self.subtema = subtema
        self.sugerencia = sugerencia
        self.comentarios = comentarios
        self.idSugerencia = idSugerencia
        self.usuario = usuarioSugeridor

    def getIdSugerencia(self):
        return self.idSugerencia

    def getId(self):
        return self.id

    def getIdLargo(self):
        return self.idLargo

    def getDescripcionItem(self):
        return self.descripcionItem

    def getSugerencia(self):
        return self.sugerencia

    def getComentarios(self):
        return self.comentarios

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
