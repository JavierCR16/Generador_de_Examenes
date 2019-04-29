import os,subprocess,datetime
from Gestores import GestorArchivos

def generarExamen(objEncabezado,listaItems,respuestas,tipoExamen,conSolucion,puntajes):
    GestorArchivos.eliminarArchivos(objEncabezado.getCurso())

    header = r'''\documentclass{article}
    \usepackage{enumerate}
    \usepackage{xcolor}
    \usepackage[utf8]{inputenc}
    \usepackage[spanish]{babel}
    \begin{document}
    '''

    footer = r'''\end{document}'''

    encabezado = generarStringEncabezado(objEncabezado,puntajes)

    body = generarStringSeleccionUnica(listaItems,respuestas,conSolucion,puntajes) \
        if tipoExamen == "S" else generarStringDesarrollo(listaItems,respuestas,conSolucion,puntajes)

    content = header + encabezado+body + footer

    fechaActual =datetime.datetime.now()

    identificadorExamen = objEncabezado.getCurso()+"_"+objEncabezado.getIdPeriodo()+"_"+objEncabezado.getAnno()+"_"\
                          + str(fechaActual.strftime("%Y-%m-%d_%H-%M-%S"))

    with open("static/" +identificadorExamen +".tex",'w',encoding='utf-8') as f:
         f.write(content)

    commandLine = subprocess.Popen(['pdflatex','-output-directory', "static/","static/" +identificadorExamen])
    commandLine.communicate()

    os.unlink("static/" +identificadorExamen +'.aux')
    os.unlink("static/" +identificadorExamen +'.log')
    os.unlink("static/" +identificadorExamen +'.tex')

    return identificadorExamen + ".pdf"

def generarStringSeleccionUnica(listaItems,listaRespuestas,conSolucion,puntajes):
    seleccion = "\\begin{enumerate}\n"
    finSeleccion = "\\end{enumerate}"
    for indexItem,item in enumerate(listaItems):

        seleccion+= "\\item "+item + "\\hfill" + "\\textbf{" + "(" + str(puntajes[indexItem]) + " Puntos)}" +"\n "

        if(listaRespuestas[indexItem].getRespuestas()!= []):
            objetoResp = listaRespuestas[indexItem]
            seleccion += "\\begin{enumerate}\n"

            for index,respuesta in enumerate(objetoResp.getRespuestas(), start=1):

                #TODO En esta  primera, poner algo que identifique la respuesta correcta de forma mas tuanis
                seleccion += "\\item \\colorbox{red}{" + respuesta + "} \n" \
                    if(conSolucion and index == objetoResp.getRespuestaCorrecta()) else "\\item " + respuesta + "\n"

            seleccion+="\\end{enumerate}\n \\vspace{0.5cm}"

    return seleccion + finSeleccion

def generarStringDesarrollo(listaItems, listaRespuestas,conSolucion,puntajes):
    desarrollo = "\\begin{enumerate}\n"
    finDesarrollo = "\\end{enumerate}"

    for index,item in enumerate(listaItems):
        desarrollo+= "\\item "+item + "\\hfill" + "\\textbf{" + str(puntajes[index])+ " (Puntos)}"+"\n \\vspace{7cm} \n"

        if(conSolucion):
            desarrollo+= "\\paragraph{} "+listaRespuestas[index].getRespuestas()[0] +" \\vspace{7cm}"

    return desarrollo + finDesarrollo

def generarStringEncabezado(objEncabezado,puntajes):

    stringEncabezado = "\\paragraph{Instituto Tecnológico de Costa Rica \\hfill   " + objEncabezado.getIdPeriodo() + ", " + \
    objEncabezado.getAnno() + "}" + "\\paragraph{" + objEncabezado.getEscuela()+" \\hfill  Total: "+str(sum(puntajes))+" Puntos}" + \
    "\\paragraph{Curso: "+ objEncabezado.getCurso()+ "\\hfill Tiempo: " + objEncabezado.getTiempo().split(":")[0] + " horas, " + \
    objEncabezado.getTiempo().split(":")[1] + " minutos} " + "\\paragraph{}" + \
    "\\centering{ " + objEncabezado.getIdTipoExamen() + "}" + "\\\\ \\hrulefill \\paragraph{INSTRUCCIONES: }" \
                       + objEncabezado.getInstrucciones() + "\\\\ \\hrulefill"

    return stringEncabezado






