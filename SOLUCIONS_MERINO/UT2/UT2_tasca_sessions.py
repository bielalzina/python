from flask import Flask, render_template, request, session
import numpy as np
app = Flask(__name__)
app.config['SECRET_KEY']='mysecretkey'


# COMPROVA DADES FORM I DISPONIBILITAT RESERVA
def comprova(reserva, llista):
    retorno=0
    
    
    
    if reserva['telefon']=="":
        retorno="NO HAS INTRODUÏT EL TELEFON"
    if reserva['nom']=="":
        retorno="NO HAS INTRODUÏT EL TEU NOM"
    if not reserva['tipopista']:
        retorno="NO HAS INTRODUÏT EL TIUPS DE PISTA"
    
    
    if retorno==0:
        for valor in llista:
            if valor['dia']==reserva['dia'] and valor['hora']==reserva['hora'] and valor['tipopista']==reserva['tipopista']:
                retorno="AQUESTA PISTA ESTÀ RESERVADA AQUEST DIA A AQUESTA HORA"
                
    return retorno

# DADES RESERVES PER PINTAR TAULA HTML
def TaulaPistes(llista):
    taula = []
    for fila in range (0,5):
        filaTemp=[]
        for columna in range (0,6):
            tempVal=""
            for reserva in llista:
                if int(reserva['dia'])==fila+1 and int(reserva['hora'])==columna+15:
                    tempVal=tempVal+reserva['nom']+" ("+reserva['tipopista']+") "
            filaTemp.append(tempVal)
        taula.append(filaTemp)
    return taula



@app.route('/')
def index():
    return render_template('UT2_registre.html')

@app.route('/formulari')
def formulari():
    return render_template('UT2_registre.html')

@app.route('/reservar')
def reservar():
    if not session:
        session['reserves']=[]
    LlistaReserves=session['reserves']
    
    nom=request.args.get('nom')
    telefon=request.args.get('telefon')
    tipopista=request.args.get('tipopista')
    hora=request.args.get('hora')
    dia=request.args.get('dia')
    
    ReservaActual = {
        'nom': nom,
        'telefon': telefon,
        'tipopista': tipopista,
        'hora': hora,
        'dia': dia
    }
    
    comp = comprova(ReservaActual, LlistaReserves)
    
    if comp==0:
        LlistaReserves.append(ReservaActual)
        session['reserves']=LlistaReserves
        taulaReserves = TaulaPistes(LlistaReserves)
        print(taulaReserves)
        return render_template('UT2_reserves.html', res=LlistaReserves, taula=taulaReserves)
    else:
        return render_template('UT2_registre.html', alerta=comp)
    
    

@app.route('/reserves')
def reserves():
    if not session:
        session['reserves']=[]
    LlistaReserves=session['reserves']
    taulaReserves = TaulaPistes(LlistaReserves)
    print(taulaReserves)
    return render_template('UT2_reserves.html', res=LlistaReserves, taula=taulaReserves)


if __name__ == '__main__':
    app.run(debug=True)