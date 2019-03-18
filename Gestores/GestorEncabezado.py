from app import app

@app.route('/Encabezado')

def Encabezado():
    return "Ahora estoy en el encabezado"