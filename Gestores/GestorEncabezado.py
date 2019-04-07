
from sympy import preview


def previewEncabezado(ObjetoEncabezado):#TODO VER COMO SE INCLUYEN PAQUETES PARA QUE SE PUEDA USAR EN ESPANNOL
    print("DATOS ENCABEZADO: "+ str(ObjetoEncabezado.__dict__))
    #Se arma el latex para el preview
    LatexWords = " \\paragraph{Instituto Tecnológico de Costa Rica \hfill   "+ ObjetoEncabezado.getIdPeriodo() + ", " + \
                    ObjetoEncabezado.getAnno() + "}" + "\\paragraph{Escuela de Matematica   \hfill  Total: 0 puntos}" + \
                    "\\paragraph{Curso: Probabilidades  \hfill Tiempo: "+ ObjetoEncabezado.getTiempo().split(":")[0] + " horas, "+ObjetoEncabezado.getTiempo().split(":")[1] + " minutos} "  + "\\paragraph{}"+ \
                    "\\centering{ " + ObjetoEncabezado.getIdTipoExamen() + "}"+ "\\\\ \\hrulefill \\paragraph{INSTRUCCIONES: }"+ObjetoEncabezado.getInstrucciones()+"\\\\ \\hrulefill"

    preview(LatexWords , viewer = "file",filename= "static/preview.png")