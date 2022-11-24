from flask import Flask, render_template, request, session
app = Flask(__name__)

app.secret_key = 'mysecretkey'
totesReserves=[]
titolsCol=['Dilluns','Dimarts','Dimecres','Dijous','Divendres']
titolsFil=['15:00','16:00','17:00','18:00','19:00','20:00']

# FUNCIÓ PER CREAR UN ID PER A CADA RESERVA
# FORMAT PER diaReserva + horaReserva + tipusPista
# PODREM ORDENAR LES RESERVES I CONTROLAR DUPLICATS MÉS FACILMENT
def crear_id_reserva(diaReserva,horaReserva,tipusPista):

    idReserva = diaReserva + horaReserva + tipusPista
    return idReserva


# FUNCIÓ PER CREAR L'ARRAY DE DICCIONARIS AMB TOTES LES RESERVES
def crear_reserva(diaReserva,horaReserva,tipusPista,nomPersona,telPersona):
    # VARIABLES NECESSARIES
    global totesReserves


    # CREAM UNA VARIABLE PER DESAR NOM DIA

    if diaReserva == "1":
        diaSetmana="Dilluns"
    elif diaReserva == "2":
        diaSetmana="Dimarts"
    elif diaReserva == "3":
        diaSetmana="Dimecres"
    elif diaReserva == "4":
        diaSetmana="Dijous"
    else:
        diaSetmana="Divendres"
    
    # CREAM idReserva
    idReserva=crear_id_reserva(diaReserva,horaReserva,tipusPista)

    reservaEnCurs={'idReserva': idReserva,
                    'diaReserva': diaReserva,
                    'diaSetmana': diaSetmana,
                    'horaReserva': horaReserva,
                    'tipusPista': tipusPista,
                    'nomPersona': nomPersona,
                    'telPersona': telPersona}
    
    #INSERTAM RESERVA EN CURS EN ARRAY
    totesReserves.append(reservaEnCurs)

    # ORDENAM totesReserves PER idReserva
    totesReserves = sorted(totesReserves, key=lambda k: k['idReserva'])

    # DESAM EL CONTINGUT DE totesReserves EN VARIABLE SESSIÓ
    session['reserves']=totesReserves



@app.route('/')
def index():
    return render_template('UT2_exemple4_registre.html')

@app.route('/formulari')
def formulari():
    return render_template('UT2_exemple4_registre.html')

@app.route('/reserves')
def reserves():

    return render_template('UT2_exemple4_reserves.html',
                            dadesReserves=totesReserves,
                            columnes=titolsCol,
                            files=titolsFil)


@app.route('/reservar')
def reservar():
    
    # VARIABLES NECESSARIES
    global totesReserves
    global titolsCol
    global titolsFil

    # SI LA VARIABLE DE SESSIÓ TÉ RESERVES ANTERIORS DESADES, PASSAM EL SEU
    # CONTINGUT A totesReserves

    if 'reserves' in session:
        totesReserves = session['reserves']
    else:
        totesReserves=[]

    # RECUPERAM VALORS DEL FORMAULARI
    diaReserva= request.args.get('dia')
    horaReserva= request.args.get('hora')
    tipusPista= request.args.get('tipopista')
    nomPersona= request.args.get('nom')
    telPersona= request.args.get('telefon')
    
    # COMPROVAM QUE ELS CAMPS tipopista, nom i telefon NO ESTIGUIN BUITS

    if (tipusPista==None):
        problema=True
        cadenaError="CAL INDICAR EL TIPUS DE PISTA: EXTERIOR o COBERTA"
        return render_template('UT2_exemple4_registre.html', 
                                problema=problema, 
                                cadenaError=cadenaError)
    elif (nomPersona==""):
        problema=True
        cadenaError="CAL INDICAR EL NOM DE LA PERSONA QUE FA LA RESERVA"
        return render_template('UT2_exemple4_registre.html', 
                                problema=problema, 
                                cadenaError=cadenaError)
    elif (telPersona==""):
        problema=True
        cadenaError="CAL INDICAR UN TELEFON DE CONTACTE"
        return render_template('UT2_exemple4_registre.html', 
                                problema=problema, 
                                cadenaError=cadenaError)
    
    else:
        # SI NO HI HA RESERVES FETES, PODEM CREAR LA RESERVA DIRECTAMENT
        if not totesReserves:
            crear_reserva(diaReserva,horaReserva,tipusPista,nomPersona,telPersona)
            return render_template('UT2_exemple4_reserves.html',
                                    dadesReserves=totesReserves,
                                    columnes=titolsCol,
                                    files=titolsFil)

        # SI HI HA RESERVES FETES CAL COMPROVAR QUE NO HI HAGI DUPLICITATS
        else:

            existeixReserva=False

            # CREAM ID RESERVA POTENCIAL
            idReservaPotencial=crear_id_reserva(diaReserva,horaReserva,tipusPista)

            # COMPARAM AQUEST VALOR AMB LES ID EXISTENTS EN ARRAY

            for valor in totesReserves:
                if valor['idReserva']==idReservaPotencial:
                    existeixReserva=True
            
            if existeixReserva:
                # JA EXISTEIX UNA RESERVA AMB AQUESTS VALORS
                problema=True
                cadenaError="LA PISTA JA ESTÀ RESERVADA AQUEST DIA I A AQUESTA HORA"
                return render_template('UT2_exemple4_registre.html',
                                        problema=problema,
                                        cadenaError=cadenaError)
            
            else:
                # NO EXISTEIX UNA RESERVA AMB AQUESTS VALORS
                crear_reserva(diaReserva,horaReserva,tipusPista,nomPersona,telPersona)
                return render_template('UT2_exemple4_reserves.html',
                                        dadesReserves=totesReserves,
                                        columnes=titolsCol,
                                        files=titolsFil)


if __name__ == '__main__':
    app.run(debug=True)