import os,glob,subprocess

def generarExamen(listaItems):
    header = r'''\documentclass{article}
    \usepackage{enumerate}
    \begin{document}
    '''

    footer = r'''\end{document}'''

    main = "\\begin{enumerate}"

    for item in listaItems:
        main+= "\\item "+item +"\n \\vspace{5cm}"

    main+="\\end{enumerate}"

    content = header + main + footer

    with open('myfile.tex','w') as f:
         f.write(content)

    commandLine = subprocess.Popen(['pdflatex', 'myfile.tex'])
    commandLine.communicate()

    os.unlink('myfile.aux')
    os.unlink('myfile.log')
    os.unlink('myfile.tex')