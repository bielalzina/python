from flask import Flask, render_template, request, session
import numpy as np
from database import gimnas
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


@app.route('/')
def index():
    avui = datetime.date.today()
    dilluns = avui-datetime.timedelta(days=avui.weekday())
    divendres = dilluns+datetime.timedelta(days=4)
    session['avui'] = avui.strftime("%d-%m-%Y")
    session['dilluns'] = dilluns.strftime("%d-%m-%Y")
    session['divendres'] = divendres.strftime("%d-%m-%Y")
    print(session['avui'])
    print(session['dilluns'])
    print(session['divendres'])
    llistaRes = gimnas.carregaReserves(session['dilluns'])


if __name__ == '__main__':
    app.run(debug=True)
