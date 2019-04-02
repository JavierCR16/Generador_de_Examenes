class ObjetoSugerencia:

    def __init__(self,idItem, sugerencia,comentarios,usuarioSugeridor):

        self.idItem = idItem
        self.sugerencia = sugerencia
        self.comentarios = comentarios
        self.usuarioSugeridor = usuarioSugeridor

        def getIdItem():
            return self.idItem

        def getSugerencia():
            return self.sugerencia

        def getComentarios():
            return self.comentarios

        def getUsuario():
            return self.usuarioSugeridor