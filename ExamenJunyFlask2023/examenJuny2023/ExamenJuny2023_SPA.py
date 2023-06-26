from flask import Flask, render_template, request, session, redirect, url_for
import numpy as np
import datetime
import urllib.request
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


@app.route('/')
def index():
    session['aeroportCode'] = "PMI"
    session['pantalla'] = "arribades"
    url = "http://127.0.0.1:5001/vols/aeroports"
    response = urllib.request.urlopen(url)
    dataAeroports = response.read()
    jsonAeroports = json.loads(dataAeroports)
    session['aeroports'] = jsonAeroports
    print(jsonAeroports)
    return redirect(url_for('arribades'))


@app.route('/sortides')
def sortides():
    session['pantalla'] = "sortides"

    # DEMANAM VOLS NACIONALS
    urlNacionals = "http://127.0.0.1:5001/vols/sortidesNacionals/" + \
        session['aeroportCode']
    response = urllib.request.urlopen(urlNacionals)
    data = response.read()
    jsonVolsNacionals = json.loads(data)
    print(jsonVolsNacionals)
    # DEMANAM VOLS INTERNACIONALS
    urlInternacionals = "http://127.0.0.1:5001/vols/sortidesInternacionals/" + \
        session['aeroportCode']
    response = urllib.request.urlopen(urlInternacionals)
    data = response.read()
    jsonVolsInternacionals = json.loads(data)
    print(jsonVolsInternacionals)
    return render_template('aeroport.html',
                           volsNacionals=jsonVolsNacionals,
                           volsInternacionals=jsonVolsInternacionals,
                           aeroports=session['aeroports'])

# This page will have the sign up form


@app.route('/arribades')
def arribades():
    session['pantalla'] = "arribades"
    url = "http://127.0.0.1:5001/vols/arribades/" + \
        session['aeroportCode']+"/2022-05-01_00:00"
    response = urllib.request.urlopen(url)
    data = response.read()
    jsonVols = json.loads(data)
    print(jsonVols)
    return render_template('aeroport.html', aeroports=session['aeroports'], vols=jsonVols)


@app.route("/cancela")
def cancela():
    id_vol = request.args.get("id_vol")
    DATA = None
    url = "http://127.0.0.1:5001/vols/cancelar/" + id_vol
    req = urllib.request.Request(url=url, data=DATA, method="PUT")
    with urllib.request.urlopen(req) as f:
        pass
    # print(f.status)
    # print(f.reason)

    if session["pantalla"] == "arribades":
        return redirect(url_for("arribades"))
    else:
        return redirect(url_for("sortides"))


@app.route('/aeroport')  # la utilitzam per canviar d'aeroport
def aeroport():
    nouAeroport = request.args.get('codi')
    session['aeroportCode'] = nouAeroport
    if session['pantalla'] == "arribades":
        return redirect(url_for('arribades'))
    else:
        return redirect(url_for('sortides'))


if __name__ == '__main__':
    app.run(debug=True)
