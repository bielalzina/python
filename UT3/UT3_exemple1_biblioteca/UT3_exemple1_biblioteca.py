from flask import Flask, render_template, request
from database import Biblioteca
app=Flask(__name__)

@app.route('/')
def index():
    departaments=Biblioteca.carregaDepartaments()
    return render_template('template_base.html',departaments=departaments)

@app.route('/llibres')
def llibres():
    dep=request.args.get('departament')
    departaments=Biblioteca.carregaDepartaments()
    llibres=Biblioteca.carregaLlibres(dep)
    return render_template('llibres.html',departaments=departaments,llibres=llibres)



if __name__ == '__main__':
    app.run(debug=True)