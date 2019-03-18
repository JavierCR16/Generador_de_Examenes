from flask import Flask

@app.route('/Encabezado')

def Encabezado():
    return "Ahora estoy en el encabezado"