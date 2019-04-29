import os

def eliminarArchivos(inicio):

    for file in os.listdir("static"):
        if file.startswith(inicio):
            os.remove("static/"+file)