from flask import Flask, render_template
from Templates import *
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!' + "<html><body><button type= button>Click Me</button></body></html>"

@app.route('/Encabezado/')
def Encabezado():
    return render_template('Encabezado.html')

if __name__ == '__main__':

    app.run()
