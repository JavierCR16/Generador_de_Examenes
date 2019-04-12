import os,glob,subprocess

def generarExamen(objEncabezado,listaItems,respuestas,tipoExamen,conSolucion):
    header = r'''\documentclass{article}
    \usepackage{enumerate}
    \begin{document}
    '''

    footer = r'''\end{document}'''
    body = generarStringSeleccionUnica(listaItems,respuestas,conSolucion) \
        if tipoExamen == "S" else generarStringDesarrollo(listaItems,respuestas,conSolucion)

    content = header + body + footer

    with open('myfile.tex','w') as f:
         f.write(content)

    commandLine = subprocess.Popen(['pdflatex', 'myfile.tex'])
    commandLine.communicate()

    os.unlink('myfile.aux')
    os.unlink('myfile.log')
    os.unlink('myfile.tex')

def generarStringSeleccionUnica(listaItems,listaRespuestas,conSolucion):
    seleccion = "\\begin{enumerate}\n"
    finSeleccion = "\\end{enumerate}"
    for indexItem,item in enumerate(listaItems):

        seleccion+= "\\item "+item +"\n"

        if(listaRespuestas[indexItem].getRespuestas()!= []):
            objetoResp = listaRespuestas[indexItem]
            seleccion += "\\begin{enumerate}\n"

            for index,respuesta in enumerate(objetoResp.getRespuestas()):

                #TODO En esta  primera, poner algo que identifique la respuesta correcta
                seleccion += "\\item " + respuesta + "\n" \
                    if(conSolucion and index == objetoResp.getRespuestaCorrecta()) else "\\item " + respuesta + "\n"

            seleccion+="\\end{enumerate}"

    return seleccion + finSeleccion

def generarStringDesarrollo(listaItems, listaRespuestas,conSolucion):

    desarrollo = "\\begin{enumerate}\n"
    finDesarrollo = "\\end{enumerate}"

    for index,item in enumerate(listaItems):
        desarrollo+= "\\item "+item +"\n \\vspace{7cm} \n"

        if(conSolucion):
            desarrollo+= "\\paragraph{} "+listaRespuestas[index].getRespuestas()[0] +" \\vspace{7cm}"

    return desarrollo + finDesarrollo







