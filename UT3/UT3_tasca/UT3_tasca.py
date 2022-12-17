from flask import Flask, render_template, request
# import numpy as np
from database import gimnas
import datetime

app = Flask(__name__)

# Data d'avui en format string. La passam al formulari per crear una resreva
avuiDataHora=datetime.datetime.now()
avuiDataHoraStr=avuiDataHora.strftime("%Y-%m-%d")

# Variable on desam el resultat de comprovar si ja existeix una reserva anterior
# el mateix dia, hora i pista. També comprova si la reserva es fa en cap de setmana
# Inicialment = 0 (comprovació -> OK)
resultatComprovacio=0

# Variable amb la llista dels limits diaris inferiors i superiors necessaris
# per accedir a la taula de reserves
limitsDiaris=[]

# Variable per activar visualització o no del formulari d'alta del client
altaClient=False

# Variable per activar visualització o no del formulari d'edició de dades del client
editaClient=False

def tornaDiaSetmana(dataHoraReserva):
    diaSetmana=dataHoraReserva.strftime("%w")
    return diaSetmana

def comprova(llistaReserves,dataHoraReserva,tipusPistaReserva):
    resultatComprovacio=0
    diaSetmana=tornaDiaSetmana(dataHoraReserva)
    if diaSetmana=="0" or diaSetmana=="6":
        resultatComprovacio="No es possible reservar els caps de setmana"
    if resultatComprovacio==0:
        for r in llistaReserves:
            if dataHoraReserva==r['data'] and tipusPistaReserva==r['idpista']:
                resultatComprovacio="Aquest dia i hora aquesta pista JA està reservada"
                resultatComprovacio=resultatComprovacio+", prova amb uns altres valors"
    return resultatComprovacio

def tornaLimitsDiaris(dataAvui,diaAvui):
    if diaAvui==0: # Diumenge
        limitInferior=dataAvui-datetime.timedelta(days=6)
    else: # Dilluns, dimarts,.., dissabte
        limitInferior=dataAvui-datetime.timedelta(days=(diaAvui-1))
    limitSuperior=limitInferior+datetime.timedelta(days=4)
    limitSuperiorSQL=limitInferior+datetime.timedelta(days=5)

    return [limitInferior,limitSuperior,limitSuperiorSQL]

def tornaValorsTaula(reservesSetmana,dataDilluns):
    dataDilluns=dataDilluns.date()
    taula=[]
    for fila in range(0,5):
        filaTemp=[]
        for columna in range(0,6):
            tempVal=""
            for reserva in reservesSetmana:
                dataReserva=reserva['data'].date()
                dataDia=dataDilluns+datetime.timedelta(days=fila)
                horaReserva=int(reserva['data'].strftime("%H"))
                if dataReserva==dataDia and horaReserva==columna+15:
                    tempVal=tempVal+reserva['nom']+" "+reserva['llinatges']
                    tempVal=tempVal+" ["+reserva['tipo']+"] "
            filaTemp.append(tempVal)
        taula.append(filaTemp)
    return taula

@app.route('/')
def index():
    llistaPistes=gimnas.carregaPistes()
    llistaClients=gimnas.carregaClients()
    return render_template('UT3_tasca_registre.html',
                            pistes=llistaPistes,
                            clients=llistaClients,
                            avui=avuiDataHoraStr,
                            resultatComprovacio=resultatComprovacio)

@app.route('/formulari')
def formulari():
    llistaPistes=gimnas.carregaPistes()
    llistaClients=gimnas.carregaClients()
    return render_template('UT3_tasca_registre.html',
                            pistes=llistaPistes,
                            clients=llistaClients,
                            avui=avuiDataHoraStr,
                            resultatComprovacio=resultatComprovacio)


@app.route('/reserves')
def reserves():
    global dataDarrerDilluns
    # Cal determinar els limits de la setmana per fer la consulta SQL

    """
    diaAvui ens indica quin dia de la setmana és avui
    0 - Diumenge
    1 - Dilluns
    ...
    6 - Dissabte
    """
    diaAvui=int(tornaDiaSetmana(avuiDataHora))

    """
    Determinam el limit diaris inferior (dilluns) i superiors
       (divendres,dissabte) per consulta SQL i TAULA
       limitsDiaris[0] - Dilluns (SQL i TAULA)
       limitsDiaris[1] - Divendres (TAULA)
       limitsDiaris[2] - Dissabte (SQL)
    """

    limitsDiaris=tornaLimitsDiaris(avuiDataHora,diaAvui)

    """ print(limitsDiaris[0])
    print(limitsDiaris[1])
    print(limitsDiaris[2])
    print(type(limitsDiaris[0]))
    print(type(limitsDiaris[1]))
    print(type(limitsDiaris[2])) """

    # Valors per insertar en HTML
    diaIniciSetmana=limitsDiaris[0].strftime("%d/%m/%Y")
    diaFinalSetmana=limitsDiaris[1].strftime("%d/%m/%Y")

    # Valors per fer consulta SQL
    diaIniciSQL=limitsDiaris[0].strftime("%Y-%m-%d")
    diaFinalSQL=limitsDiaris[2].strftime("%Y-%m-%d")

    # Obtenim llista de reserves de la setmana

    reservesSetmana=gimnas.carregaReservesSetmana(diaIniciSQL,diaFinalSQL)

    """ for reserves in reservesSetmana:
            print(reserves['data'])
            print(type(reserves['data']))
            print(reserves['idpista'])
            print(reserves['tipo'])
            print(reserves['idclient'])
            print(reserves['nom'])
            print(reserves['llinatges']) """

    # Obtenim els valors per pintar la taula
    dataDarrerDilluns=limitsDiaris[0]

    valorsTaula=tornaValorsTaula(reservesSetmana,dataDarrerDilluns)

    #print(valorsTaula)

    return render_template('UT3_tasca_reserves.html',
                            diaInici=diaIniciSetmana,
                            diaFinal=diaFinalSetmana,
                            reserves=valorsTaula)

@app.route('/setmanamenys')
def setmanamenys():
    # Cal determinar els limits de la setmana per fer la consulta SQL
    # El dilluns de la darrera setmana consultada esta desat
    # en la variable dataDarrerDilluns
    # Cal doncs restar-li 7 dies i obtindrem el nou limit inferior
    global dataDarrerDilluns
    dataDarrerDilluns=dataDarrerDilluns-datetime.timedelta(days=7)


    # Determinam el limits diaris inferior (dilluns) i superiors
    # (divendres,dissabte) per consulta SQL i TAULA

    limitsDiaris=tornaLimitsDiaris(dataDarrerDilluns,1)

    # Valors per insertar en HTML
    diaIniciSetmana=limitsDiaris[0].strftime("%d/%m/%Y")
    diaFinalSetmana=limitsDiaris[1].strftime("%d/%m/%Y")

    # Valors per fer consulta SQL
    diaIniciSQL=limitsDiaris[0].strftime("%Y-%m-%d")
    diaFinalSQL=limitsDiaris[2].strftime("%Y-%m-%d")

    # Obtenim llista de reserves de la setmana

    reservesSetmana=gimnas.carregaReservesSetmana(diaIniciSQL,diaFinalSQL)

    # Obtenim els valors per pintar la taula
    valorsTaula=tornaValorsTaula(reservesSetmana,dataDarrerDilluns)

    return render_template('UT3_tasca_reserves.html',
                            diaInici=diaIniciSetmana,
                            diaFinal=diaFinalSetmana,
                            reserves=valorsTaula)

@app.route('/setmanames')
def setmanames():
    # Cal determinar els limits de la setmana per fer la consulta SQL
    # El dilluns de la darrera setmana consultada esta desat
    # en la variable dataDarrerDilluns
    # Cal doncs sumar-li 7 dies i obtindrem el nou limit inferior
    global dataDarrerDilluns

    dataDarrerDilluns=dataDarrerDilluns+datetime.timedelta(days=7)


    # Determinam el limits diaris inferior (dilluns) i superiors
    # (divendres,dissabte) per consulta SQL i TAULA

    limitsDiaris=tornaLimitsDiaris(dataDarrerDilluns,1)

    # Valors per insertar en HTML
    diaIniciSetmana=limitsDiaris[0].strftime("%d/%m/%Y")
    diaFinalSetmana=limitsDiaris[1].strftime("%d/%m/%Y")

    # Valors per fer consulta SQL
    diaIniciSQL=limitsDiaris[0].strftime("%Y-%m-%d")
    diaFinalSQL=limitsDiaris[2].strftime("%Y-%m-%d")

    # Obtenim llista de reserves de la setmana

    reservesSetmana=gimnas.carregaReservesSetmana(diaIniciSQL,diaFinalSQL)

    # Obtenim els valors per pintar la taula
    valorsTaula=tornaValorsTaula(reservesSetmana,dataDarrerDilluns)

    return render_template('UT3_tasca_reserves.html',
                            diaInici=diaIniciSetmana,
                            diaFinal=diaFinalSetmana,
                            reserves=valorsTaula)

@app.route('/novaReserva')
def novaReserva():
    global dataDarrerDilluns
    # Recuperam dades del formulari
    dia=request.args.get('dia')
    horaReserva=int(request.args.get('hora'))
    tipusPistaReserva=int(request.args.get('tipopista'))
    clientReserva=int(request.args.get('usuari'))

    dia=dia.split("-")
    #print(dia)
    anyReserva=int(dia[0])
    mesReserva=int(dia[1])
    diaReserva=int(dia[2])

    dataHoraReserva = datetime.datetime(anyReserva, mesReserva, diaReserva, horaReserva)
    dataHoraReservaString=dataHoraReserva.strftime("%Y-%m-%d %X")

    # Recuperam reserves
    llistaReserves=gimnas.carregaReserves()

    # Comprovam correcció reserva
    resultatComprovacio=comprova(llistaReserves,dataHoraReserva,tipusPistaReserva)

    llistaPistes=gimnas.carregaPistes()
    llistaClients=gimnas.carregaClients()

    if resultatComprovacio==0:
        # Afegim Reserva en BBDD
        gimnas.afegeixReserva(dataHoraReservaString,tipusPistaReserva,clientReserva)

        # Cal determinar els limits de la setmana per fer la consulta SQL
        diaAvui=int(tornaDiaSetmana(dataHoraReserva))

        # Determinam el limit diaris inferior (dilluns) i superiors
        # (divendres,dissabte) per consulta SQL i TAULA

        limitsDiaris=tornaLimitsDiaris(dataHoraReserva,diaAvui)

        # Valors per insertar en HTML
        diaIniciSetmana=limitsDiaris[0].strftime("%d/%m/%Y")
        diaFinalSetmana=limitsDiaris[1].strftime("%d/%m/%Y")

        # Valors per fer consulta SQL
        diaIniciSQL=limitsDiaris[0].strftime("%Y-%m-%d")
        diaFinalSQL=limitsDiaris[2].strftime("%Y-%m-%d")

        # Obtenim llista de reserves de la setmana
        reservesSetmana=gimnas.carregaReservesSetmana(diaIniciSQL,diaFinalSQL)

        # Obtenim els valors per pintar la taula
        dataDarrerDilluns=limitsDiaris[0]
        valorsTaula=tornaValorsTaula(reservesSetmana,dataDarrerDilluns)

        return render_template('UT3_tasca_reserves.html',
                            diaInici=diaIniciSetmana,
                            diaFinal=diaFinalSetmana,
                            reserves=valorsTaula)

    else:
        return render_template('UT3_tasca_registre.html',
                            pistes=llistaPistes,
                            clients=llistaClients,
                            avui=avuiDataHoraStr,
                            resultatComprovacio=resultatComprovacio)



@app.route('/usuaris')
def usuaris():
    # Obtenim llista de clients
    llistaClients=gimnas.carregaClients()
    # print(llistaClients)
    return render_template('UT3_tasca_usuaris.html',
                            llistaClients=llistaClients)


@app.route('/eliminaUsuari')
def eliminaUsuari():
    # Recuperam idclient
    idclient=request.args.get('idclient')
    # Executam query eliminacio
    gimnas.eliminaClient(idclient)
    # Obtenim llista de clients
    llistaClients=gimnas.carregaClients()
    return render_template('UT3_tasca_usuaris.html',
                            llistaClients=llistaClients)

@app.route('/afegeixUsuari')
def afegeixUsuari():
    # Variable per activar visualització o no del formulari d'alta del client
    altaClient=True
    # Obtenim el valor màxim d'idclient
    maxIdclient=gimnas.tornaMaximIdclient()
    nouId=maxIdclient['maxId']+1

    # Obtenim llista de clients
    llistaClients=gimnas.carregaClients()
    return render_template('UT3_tasca_usuaris.html',
                            llistaClients=llistaClients,
                            altaClient=altaClient,
                            nouId=nouId)


@app.route('/desaNouUsuari')
def desaNouUsuari():
    # Recuperam dades del formaulari
    idclient=request.args.get('idclient')
    nom=request.args.get('nom')
    llinatges=request.args.get('llinatges')
    telefon=request.args.get('telefon')
    # Afegim nou client a la BBDD
    gimnas.afegeixClient(idclient,nom,llinatges,telefon)
    # Obtenim llista de clients
    llistaClients=gimnas.carregaClients()
    return render_template('UT3_tasca_usuaris.html',
                            llistaClients=llistaClients)

@app.route('/editaUsuari')
def editaUsuari():
    # Variable per activar visualització o no del formulari d'edició de dades del client
    editaClient=True
    # Recuperam dades del formaulari
    idclientEditable=int(request.args.get('idclient'))
    # Obtenim llista de clients
    llistaClients=gimnas.carregaClients()
    return render_template('UT3_tasca_usuaris.html',
                            llistaClients=llistaClients,
                            editaClient=editaClient,
                            idclientEditable=idclientEditable)


@app.route('/desaModificacioUsuari')
def desaModificacioUsuari():
    # Recuperam dades del formaulari
    idclient=request.args.get('idclient')
    nom=request.args.get('nom')
    llinatges=request.args.get('llinatges')
    telefon=request.args.get('telefon')
    # Executam l'actualització de les dades
    gimnas.modificaClient(idclient,nom,llinatges,telefon)
    # Obtenim llista de clients
    llistaClients=gimnas.carregaClients()
    return render_template('UT3_tasca_usuaris.html',
                            llistaClients=llistaClients)


if __name__ == '__main__':
    app.run(debug=True)