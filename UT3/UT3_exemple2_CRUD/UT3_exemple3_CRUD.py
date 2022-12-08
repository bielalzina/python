from flask import Flask, render_template, request, session
import numpy as np
from database import biblioteca
import datetime

app = Flask(__name__)

app.config['SECRET_KEY']='mysecretkey'

@app.route('/')
def index():
    llistaEditors=biblioteca.carregaEditors()
    print(llistaEditors)
    return render_template('UT3_exemple2_editors.html',editors=llistaEditors)


# ARRIBA AQUI TAN SI VOLEM MODIFICAR UN EDITOR COM SI VOLEM AFEGIR UN EDITOR
@app.route('/formulari')
def formulari():
    ideditor=request.args.get('id_edit')
    nom=request.args.get('nom')
    return render_template('UT3_exemple2_modifica.html',idedit=ideditor, nom=nom)


@app.route('/executacanvis')
def executacanvis():
    ideditor=request.args.get('id_edit')
    nom=request.args.get('nom')
    
    # si no tenim ideditor es que és un NOU editor
    # si tenim ideditor es una MODIFICACIÓ

    if ideditor!='None': # MODIFICACIÓ
        biblioteca.modificaEditor(nom,ideditor)
    else: # EDITOR NOU
        biblioteca.afegeixEditor(nom)
    
    llistaEditors=biblioteca.carregaEditors()
    return render_template('UT3_exemple2_editors.html',editors=llistaEditors)

@app.route('/elimina')
def elimina():
    ideditor=request.args.get('id_edit')
    biblioteca.eliminaEditor(ideditor)
    llistaEditors=biblioteca.carregaEditors()
    return render_template('UT3_exemple2_editors.html',editors=llistaEditors)


if __name__ == '__main__':
    app.run(debug=True)