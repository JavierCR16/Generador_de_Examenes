class ObjetoSugerencia:

    def __init__(self,idItem, sugerencia,comentarios,usuarioSugeridor):

        self.idItem = idItem
        self.sugerencia = sugerencia
        self.comentarios = comentarios
        self.usuarioSugeridor = usuarioSugeridor

    def getIdItem(self):
        return self.idItem

    def getSugerencia(self):
        return self.sugerencia

    def getComentarios(self):
        return self.comentarios

    def getUsuario(self):
        return self.usuarioSugeridor