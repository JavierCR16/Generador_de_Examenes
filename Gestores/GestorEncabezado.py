import datetime
from Gestores import GestorArchivos
from sympy import preview

def previewEncabezado(ObjetoEncabezado):#TODO VER COMO SE INCLUYEN PAQUETES PARA QUE SE PUEDA USAR EN ESPANNOL

    GestorArchivos.eliminarArchivos("Preview")

    LatexWords = " \\paragraph{Instituto Tecnologico de Costa Rica \hfill   "+ ObjetoEncabezado.getIdPeriodo() + ", " + \
                    ObjetoEncabezado.getAnno() + "}" + "\\paragraph{Escuela de Matematica   \hfill  Total: 0 puntos}" + \
                    "\\paragraph{Curso: Probabilidades  \hfill Tiempo: "+ ObjetoEncabezado.getTiempo().split(":")[0] + " horas, " + ObjetoEncabezado.getTiempo().split(":")[1] + " minutos} "  + "\\paragraph{}" + \
                    "\\centering{ " + ObjetoEncabezado.getIdTipoExamen() + "}"+ "\\\\ \\hrulefill \\paragraph{INSTRUCCIONES: }"+ ObjetoEncabezado.getInstrucciones()+"\\\\ \\hrulefill"

    nombreImagen = "Preview-"+str(datetime.datetime.now()).replace(":","-")+".png"
    preview(LatexWords , viewer = "file",filename= "static/" +nombreImagen)

    return nombreImagen

