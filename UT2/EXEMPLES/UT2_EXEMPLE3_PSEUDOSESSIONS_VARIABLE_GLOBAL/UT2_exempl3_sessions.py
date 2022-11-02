from distutils.log import debug
from flask import Flask, render_template, request
app = Flask (__name__)
varInterna = 1

@app.route('/')
def index():
    global varInterna
    return render_template('Home.html', valor=varInterna)

@app.route('/actualitzar')
def actualitzar():
    global varInterna
    bot = request.args.get('operacion')
    if bot=="mas1":
        varInterna=varInterna+1
    if bot=="mas5":
        varInterna=varInterna+5
    if bot=="menos2":
        varInterna=varInterna-2
    return render_template('Boton.html', valor=varInterna, boton=bot)


if __name__ == '__main__':
    app.run(debug=True)