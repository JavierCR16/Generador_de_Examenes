
from sympy import preview


def previewEncabezado(ObjetoEncabezado):
        #Se arma el latex para el preview
        LatexWords = "\\paragraph{Tecnológico de Costa Rica \hfill   "+ ObjetoEncabezado.getIdTipoExamen() + " , " + \
                     ObjetoEncabezado.getAnno() + "}" + "\\paragraph{ Escuela de Matematica   \hfill  Total: 30 puntos}" + \
                     "\\paragraph{ Curso: Probabilidades  \hfill Tiempo: "+ ObjetoEncabezado.getTiempo() + "} "  + "\\paragraph{}"+ \
                     "\\centering{ " + ObjetoEncabezado.getIdTipoExamen() + "}"+ "\\paragraph{}" + "\\centering{ "+ObjetoEncabezado.getInstrucciones() + "}"

        preview(LatexWords , viewer = "file",filename= "static/Preview.png")