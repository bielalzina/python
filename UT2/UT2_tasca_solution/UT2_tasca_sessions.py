from flask import Flask, render_template, request, session
import numpy as np
app = Flask(__name__)
app.config['SECRET_KEY']='mysecretkey'


def comprova(reserva,llista):
	
	retorno=0
	
	# Comprovam que no hi hagi camps buits en el formulari
	if reserva['telefon']=="":
		retorno="No has introduit el telefon"
	if reserva['nom']=="":
		retorno="No has introduit el nom"
	if not reserva['tipopista']:
		retorno="Indica el tipus de pista"
	
	# Comprovam que no existeixi reserva anterior

	if retorno==0:
		for r in llista:
			if r['dia']==reserva['dia'] and r['hora']==reserva['hora'] and r['tipopista']==reserva['tipopista']:
				retorno="Pista RESERVADA, intenta una altra dia/hora"
	
	return retorno
	

def TaulaPistes(llista):
	taula=[]
	for fila in range (0,5):
		filaTemp=[]
		for columna in range(0,6):
			tempVal=""
			for reserva in llista:
				if int(reserva['dia'])==fila+1 and int(reserva['hora'])==columna+15:
					tempVal=tempVal+reserva['nom']+" ("+reserva['tipopista']+")"
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

	# Comprovam si hi ha una sessió activa
	if not session:

		# Si no hi ha sessió inicialitzam variable de sessió
		session['reserves']=[]
	
	# Tan si hi ha sessió activa com no 
	LlistaReserves = session['reserves']

	# Recuperam valors del formulari
	nom=request.args.get('nom')
	telefon=request.args.get('telefon')
	tipopista=request.args.get('tipopista')
	hora=request.args.get('hora')
	dia=request.args.get('dia')

	# Possible reserva en curs
	ReservaActual={'nom':nom,'telefon':telefon,'tipopista':tipopista,'hora':hora,'dia':dia}

	# Comprovam que la pista NO estigui ja reservada

	comp=comprova(ReservaActual,LlistaReserves)

	if comp == 0:
		# No hi ha errades en el formulari i la pista NO està reservada
		# Afegim reserva en curs a la llista de reserves
		LlistaReserves.append(ReservaActual)
		# Actualitzam la variable de sessió
		session['Reserves']=LlistaReserves
		# Obtenim els valors que hem de traspassar a les taules
		taulaReserves=TaulaPistes(LlistaReserves)

		return render_template('UT2_reserves.html',res=LlistaReserves,taula=taulaReserves)
	
	else:
		# Hi ha errades en el formulari o la pista JA està reservada
		return render_template('UT2_registre.html',alerta=comp)

@app.route('/reserves')
def reserves():

	# Comprovam si hi ha una sessió activa
	if not session:

		# Si no hi ha sessió inicialitzam variable de sessió
		session['reserves']=[]
	
	# Tan si hi ha sessió activa com no 
	LlistaReserves = session['reserves']

	# Recuperam valors de les taules
	taulaReserves=TaulaPistes(LlistaReserves)
	
	return render_template('UT2_reserves.html',res=LlistaReserves,taula=taulaReserves)



if __name__ == '__main__':
	app.run(debug=True)