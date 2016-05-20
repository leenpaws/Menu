from flask import Flask
# instance with name of running app
app = Flask(__name__)

"""decorator"""


@app.route('/')
@app.route('/hello')

def HelloWorld():
    return "Hello World"
# main is app run by interpreter, other file have __name of pythonfile__
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)