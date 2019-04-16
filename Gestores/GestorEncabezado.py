import datetime
from sympy import preview



def previewEncabezado(ObjetoEncabezado,usuario):#TODO VER COMO SE INCLUYEN PAQUETES PARA QUE SE PUEDA USAR EN ESPANNOL

    print("Tiempo:" ,ObjetoEncabezado.getTiempo())

    LatexWords = " \\paragraph{Instituto Tecnologico de Costa Rica \hfill   "+ ObjetoEncabezado.getIdPeriodo() + ", " + \
                    ObjetoEncabezado.getAnno() + "}" + "\\paragraph{Escuela de Matematica   \hfill  Total: 0 puntos}" + \
                    "\\paragraph{Curso: Probabilidades  \hfill Tiempo: "+ ObjetoEncabezado.getTiempo().split(":")[0] + " horas, " + ObjetoEncabezado.getTiempo().split(":")[1] + " minutos} "  + "\\paragraph{}" + \
                    "\\centering{ " + ObjetoEncabezado.getIdTipoExamen() + "}"+ "\\\\ \\hrulefill \\paragraph{INSTRUCCIONES: }"+ ObjetoEncabezado.getInstrucciones()+"\\\\ \\hrulefill"

    nombreImagen = usuario+"-"+str(datetime.datetime.now()).replace(":","-")+".png"
    preview(LatexWords , viewer = "file",filename= "static/" +nombreImagen)

    return nombreImagen
