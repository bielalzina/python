from flask import Flask, render_template, request, session, redirect, url_for
import numpy as np
import datetime
from datetime import date
import urllib.request, json

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"


@app.route("/")
def index():
    session["aeroportCode"] = "PMI"
    session["pantalla"] = "arribades"
    avui = date.today()
    # print(type(avui))
    # print(avui)
    avuiStr = avui.strftime("%Y-%m-%d")
    session["data"] = avuiStr
    # print(type(session["data"]))
    # print(session["data"])
    url = "http://127.0.0.1:5001//vols/aeroports"
    response = urllib.request.urlopen(url)
    data = response.read()
    session["llistaAeroport"] = json.loads(data)
    # print(session["llistaAeroport"])
    return redirect(url_for("arribades"))


@app.route("/sortides")
def sortides():
    session["pantalla"] = "sortides"
    url = (
        "http://127.0.0.1:5001/vols/sortides/"
        + session["aeroportCode"]
        + "/"
        + session["data"]
    )
    print(url)
    response = urllib.request.urlopen(url)
    data = response.read()
    jsonVols = json.loads(data)
    # print(jsonVols)
    return render_template("aeroport.html", vols=jsonVols)


# This page will have the sign up form
@app.route("/arribades")
def arribades():
    session["pantalla"] = "arribades"
    url = (
        "http://127.0.0.1:5001/vols/arribades/"
        + session["aeroportCode"]
        + "/"
        + session["data"]
    )
    response = urllib.request.urlopen(url)
    data = response.read()
    jsonVols = json.loads(data)
    # print(jsonVols)
    return render_template("aeroport.html", vols=jsonVols)


@app.route("/aeroport")  # la utilitzam per canviar d'aeroport
def aeroport():
    nouAeroport = request.args.get("codi")
    session["aeroportCode"] = nouAeroport
    novaData = request.args.get("data")
    session["data"] = novaData
    print(session["aeroportCode"])
    print(session["data"])

    if session["pantalla"] == "arribades":
        return redirect(url_for("arribades"))
    else:
        return redirect(url_for("sortides"))


@app.route("/retras")  # la utilitzam per canviar d'aeroport
def retras():
    id_vol = request.args.get("id_vol")
    DATA = None
    url = "http://127.0.0.1:5001/vols/retraso/" + id_vol
    req = urllib.request.Request(url=url, data=DATA, method="PUT")
    with urllib.request.urlopen(req) as f:
        pass
    # print(f.status)
    # print(f.reason)

    if session["pantalla"] == "arribades":
        return redirect(url_for("arribades"))
    else:
        return redirect(url_for("sortides"))


if __name__ == "__main__":
    app.run(debug=True)
