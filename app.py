from flask import Flask
from Gestores import GestorBase

app = Flask(__name__)


@app.route('/')
def hello_world():
    GestorBase.establecerConexion(1, 1)
    return 'Hello World!'


if __name__ == '__main__':

    app.run()
