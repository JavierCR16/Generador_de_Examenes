
from sympy import preview


def previewEncabezado(ObjetoEncabezado):
        #Aqui poner todo lo del objeto

        LatexWords = "\\paragraph{Tecnologico de Costa Rica}  \\t \\paragraph{ II Semestre, 2018} \\paragraph{Tipo de Examen: " + ObjetoEncabezado.getIdTipoExamen() + "}"

        preview(LatexWords , viewer = "file",filename= "static/Preview.png")