class ObjetoUsuario:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

    def getNombre(self):
        return self.nombre

    def getCorreo(self):
        return self.correo
