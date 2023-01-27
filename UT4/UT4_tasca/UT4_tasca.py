from myproject import app
from flask import render_template, request, session, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from myproject.forms import UsuariForm, ReservaForm
from myproject.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from myproject.models import gimnas


# ********************************************
# ********************************************
# ************   TASCA 4   *******************
# ********************************************
# ********************************************


@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/formlogin')
def formlogin():
    return render_template('UT4_login.html',
                           altaMissatge=request.args.get('altaMissatge'))

@app.route('/login', methods = ['GET','POST'])
def login():
    # Obtenim dades del formulari
    nomUsuari=request.form['usuari']
    password=request.form['password']
    #print(nomUsuari)
    #print(password)
    
    # Instaciam la CLASSE User
    user=User()
    #print(user)
    #print(user.nomUsuari)
    
    # Definim l'atribut nomUsuari de l'objecte user
    user.set_nomUsuari(nomUsuari)
    #print(user.nomUsuari)

    if user.comprovaPassword(password):
        # TRUE, password -> OK
        # Obtenim dades de l'usuari en funció del nom usuari
        user.obtenirDadesUsuariSegonsNomUsuari()
        # Carregam usuari en login_manager
        login_user(user)

        return redirect(url_for('dashboard'))

    else:
        # FALSE, password -> KO
        return render_template('UT4_login.html', 
                               loginMissatge="Les dades que has indicat per \
                                   iniciar sessió no són correctes. Torna a \
                                    intentar-ho.")

@app.route('/dashboard')
@login_required
def dashboard():
    user=User()
    # Cal comprovar si l'usuari actiu té alguna reserva
    # Si té alguna reserva, cal obtenir la data de la primera reserva
    primeraData=user.obtenirPrimeraDataReservaClient(current_user.id)
    #print(primeraData)
    #print(type(primeraData))
    if primeraData['primeraData']==None:
        # L'usuari no ha fet cap reserva
        # Mostram les reserves de la setmana actual
        # Obtenim extrems de la setmana actual
        extremsSetmana=user.tornaLimitsDiaris(datetime.datetime.now())
        # print('extremsSetmana')
        # print(extremsSetmana)
        
        # Obtenim els arrays amb els valors per pintar les taules
        valorsArraysTaules=user.tornaArrayTaules(extremsSetmana,current_user.id)
        #print(valorsArraysTaules)
        
    else:
        # L'usuari ha fet com a mínim una reserva
        # Obtenim extrems de la setmana en la que va fer la primera reserva
        extremsSetmana=user.tornaLimitsDiaris(primeraData['primeraData'])
                
        # Obtenim els arrays amb els valors per pintar les taules
        valorsArraysTaules=user.tornaArrayTaules(extremsSetmana,current_user.id)
        #print(*valorsArraysTaules,sep='\n')
        
    return render_template('UT4_dashboard.html', 
                               diaInici=extremsSetmana[0],
                               diaFinal=extremsSetmana[1],
                               reservesCoberta=valorsArraysTaules[0],
                               reservesExterior=valorsArraysTaules[1])
    
@app.route('/dashboardCanviSetmana')
@login_required
def dashboardCanviSetmana():
    user=User()
    darrerDilluns=request.args.get('dilluns')
    sentit=request.args.get('accio')
        
    # Passam data dilluns a datetime
    darrerDilluns=datetime.datetime.strptime(darrerDilluns, '%d/%m/%Y')
    
    # Sumam o restam 7 dies a darrerDilluns segons sentit
    if sentit=="mes":
        nouDilluns=darrerDilluns+datetime.timedelta(days=7)
    elif sentit=="menys":
        nouDilluns=darrerDilluns-datetime.timedelta(days=7)
    else:
        nouDilluns=darrerDilluns
    
    # Obtenim extrems de la nova setmana a retornar
    extremsSetmana=user.tornaLimitsDiaris(nouDilluns)
                
    # Obtenim els arrays amb els valors per pintar les taules
    valorsArraysTaules=user.tornaArrayTaules(extremsSetmana,current_user.id)
    
    return render_template('UT4_dashboard.html', 
                               diaInici=extremsSetmana[0],
                               diaFinal=extremsSetmana[1],
                               reservesCoberta=valorsArraysTaules[0],
                               reservesExterior=valorsArraysTaules[1])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/nouUsuariRegistre', methods=['GET','POST'])
def nou_usuari_registre():

    # Cream una instancia de la classe UsuariForm
    form = UsuariForm()

    # Si s'ha enviat i validat el formulari, rebem els valors per POST
    if form.validate_on_submit():

        # Capturam els valors del formulari
        username=form.username.data 
        nom=form.nom.data 
        llinatges=form.llinatges.data 
        password=form.password.data
        dataAlta=form.dataAlta.data
        email=form.email.data
        telefon=form.telefon.data 
        
        """print(username)
        print(nom)
        print(llinatges)
        print(password)
        print(dataAlta)
        print(email)
        print(telefon)"""
        
        # Instaciam la CLASSE User
        user=User()
        
        # Executam l'alta de l'usuari en la BBDD
        user.altaUsuari(username,nom,llinatges,password,dataAlta,email,telefon)
        
        # Redirigim a formulari login
        return redirect(url_for('formlogin',
                                altaMissatge="USUARI AFEGIT CORRECTAMENT"))
    

    # Si NO s'ha enviat el formulari,
    # o s'ha enviat però NO ha estat validat,
    # cal tornar carregar el formulari passant les dades necessaries
    # per construir-lo (instacia form)
    return render_template('UT4_nouUsuariForm.html', form=form) 

@app.route('/formreserva',methods=['GET','POST'])
@login_required
def formreserva():
    # Instaciam la CLASSE User
    user=User()
    # Cream una instancia de la classe UsuariForm
    form = ReservaForm()
    # Recuperam dades de les pistes per passar al formulari
    dadesPistes=user.retornaDadesPistes()
    # print(dadesPistes)
    
    # Carregam les opcions del SELECT pel tipus de pista des de BBDD
    form.tipusPista.choices=[(pista['idpista'],str(pista['tipo'])+" \
        - "+str(pista['preu'])+" €") for pista in dadesPistes]
    
    if form.validate_on_submit():

        # Capturam els valors del formulari
        dataReserva=form.dataReserva.data 
        horaReserva=int(form.horaReserva.data) 
        tipusPista=int(form.tipusPista.data )
          
        # print(type(dataReserva))
        # print(dataReserva)
        # print(type(horaReserva))
        # print(horaReserva)
        # print(type(tipusPista))
        # print(tipusPista)
        
        # Combinam dataReserva + horaReserva per poder comprovar la 
        # disponibilitat de la reserva
        dataHoraReserva=user.converteixEnDateTime(dataReserva,horaReserva)
        
        # print('dataHoraReserva:')
        # print(dataHoraReserva)
        # print(type(dataHoraReserva))        
        
        
        # Recuperam reserves existents en la BBDD
        llistaReserves=user.retornaTotesReserves()
        
        # Comprovam que la pista no estigui reservada previament
        resultatDisponibilitat=user.comprovaDisponibiltat(llistaReserves,
                                                     dataHoraReserva,tipusPista)
        # print('resultatDisponibilitat')
        # print(resultatDisponibilitat)
        
        if resultatDisponibilitat==0:
            # La pista està disponible, podem inserir la reserva en BBDD
            dataHoraReservaString=dataHoraReserva.strftime("%Y-%m-%d %X")
            user.insereixReserva(dataHoraReservaString,
                                 tipusPista,
                                 current_user.id)
            # Redirigim a vista reserves
            return redirect(url_for('dashboard'))
            
        
        else:
            # Pista OCUPADA
            return render_template('UT4_formReserva.html', form=form, 
                                   missatgeDisponibilitat=resultatDisponibilitat)

        
    
    # Si NO s'ha enviat el formulari,
    return render_template('UT4_formReserva.html', form=form)


# ********************************************
# ********************************************
# ************   TASCA 3   *******************
# ********************************************
# ********************************************





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


@app.route('/ut3Inici')
def ut3Inici():
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
    # diaAvui ens indica quin dia de la setmana és avui
    # 0 - Diumenge
    # 1 - Dilluns
    # ...
    # 6 - Dissabte
     
    diaAvui=int(tornaDiaSetmana(avuiDataHora))

     
    # Determinam el limit diaris inferior (dilluns) i superiors
    #   (divendres,dissabte) per consulta SQL i TAULA
    #   limitsDiaris[0] - Dilluns (SQL i TAULA)
    #   limitsDiaris[1] - Divendres (TAULA)
    #   limitsDiaris[2] - Dissabte (SQL)
     

    limitsDiaris=tornaLimitsDiaris(avuiDataHora,diaAvui)

    # print(limitsDiaris[0])
    # print(limitsDiaris[1])
    # print(limitsDiaris[2])
    # print(type(limitsDiaris[0]))
    # print(type(limitsDiaris[1]))
    # print(type(limitsDiaris[2])) 

    # Valors per insertar en HTML
    diaIniciSetmana=limitsDiaris[0].strftime("%d/%m/%Y")
    diaFinalSetmana=limitsDiaris[1].strftime("%d/%m/%Y")

    # Valors per fer consulta SQL
    diaIniciSQL=limitsDiaris[0].strftime("%Y-%m-%d")
    diaFinalSQL=limitsDiaris[2].strftime("%Y-%m-%d")

    # Obtenim llista de reserves de la setmana

    reservesSetmana=gimnas.carregaReservesSetmana(diaIniciSQL,diaFinalSQL)

    # for reserves in reservesSetmana:
    #         print(reserves['data'])
    #         print(type(reserves['data']))
    #         print(reserves['idpista'])
    #         print(reserves['tipo'])
    #         print(reserves['idclient'])
    #         print(reserves['nom'])
    #         print(reserves['llinatges']) 

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
    # Comprovam si el client te reserves realitzades
    numReserves=gimnas.tornaNumReservesClient(idclient)
    if (numReserves['COUNT(idclient)'])==0:
        # El client no te reserves, es pot eliminar
        usuariNoEliminable=False
        missatge=""
        gimnas.eliminaClient(idclient)
    else:
        # El client te reserves, NO es pot eliminar
        usuariNoEliminable=True
        missatge="USUARI AMB RESERVES ACTIVES, NO ÉS POSSIBLE ELIMINAR-LO"
    # Obtenim llista de clients
    llistaClients=gimnas.carregaClients()
    return render_template('UT3_tasca_usuaris.html',
                            llistaClients=llistaClients,
                            usuariNoEliminable=usuariNoEliminable,
                            missatge=missatge)

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