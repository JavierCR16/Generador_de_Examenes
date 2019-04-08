class ObjetoEncabezado:
    def __init__(self,id,curso,escuela,instrucciones, anno,tiempo, idPeriodo, idTipoExamen):
        self.id = id
        self.curso = curso
        self.escuela = escuela
        self.instrucciones =  instrucciones
        self.anno = anno
        self.tiempo = tiempo
        self.idPeriodo = idPeriodo
        self.idTipoExamen = idTipoExamen

    def getId(self):
        return self.id

    def getCurso(self):
        return self.curso

    def getEscuela(self):
        return self.escuela

    def getInstrucciones(self):
        return self.instrucciones

    def getAnno(self):
        return self.anno

    def getTiempo(self):
        return self.tiempo

    def getIdPeriodo(self):
        return self.idPeriodo

    def getIdTipoExamen(self):
        return self.idTipoExamen
