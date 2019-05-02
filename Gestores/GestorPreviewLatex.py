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

def generarItemsLatex(itemsExtraidos,codigoSesion):
    listaImagenes = []
    for index, tupla in enumerate(itemsExtraidos):
        objImagen = tupla[0]

        latex= "\\paragraph{} "+objImagen.getDescripcion() +"\\hfill " +"("+str(objImagen.getPuntaje()) +" Puntos)"

        nombreImagen = codigoSesion+"-"+str(index)+ ".png"
        preview(latex, viewer="file", filename="static/" + nombreImagen)

        listaImagenes.append(nombreImagen)

    return listaImagenes


