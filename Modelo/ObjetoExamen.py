class ObjetoExamen:

    def __init__(self,id,encabezado,modalidad,fechaCreacion,usuarioCreador,archivoExamen,items):

        self.id = id
        self.encabezado = encabezado
        self.modalidad = modalidad
        self.fechaCreacion = fechaCreacion
        self.usuarioCreador = usuarioCreador
        self.archivoExamen = archivoExamen
        self.items = items

    def getId(self): return self.id

    def getEncabezado(self): return self.encabezado

    def getModalidadExamen(self): return self.modalidad

    def getFechaCreacion(self): return self.fechaCreacion

    def getCreador(self): return self.usuarioCreador

    def getArchivoExamen(self): return self.archivoExamen

    def getItems(self): return self.items
