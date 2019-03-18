from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!' + "<html><body><button type= button>Click Me</button></body></html>"


if __name__ == '__main__':
    app.run()
