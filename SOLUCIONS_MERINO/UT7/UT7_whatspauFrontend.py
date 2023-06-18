from flask import Flask, render_template, request, session, make_response
import numpy as np
import datetime
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
API_url="http://87.235.201.250:8080/whatspau_php"

@app.route('/')
def index():
	return render_template('UT7_whatspau_login.html')

@app.route('/signin')
def signin():
	return render_template('UT7_whatspau_login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    usuari= request.form['usuari']
    pwd=request.form['password']
    #preparam la consulta a la API
    payload={"username":usuari,"password":pwd}
    #enviam la consulta AUTH a la API
    response=requests.post(API_url+"/login",data=payload)
    #print("response.status_code: ") 
    #print(response.status_code) 
    #print("response.json(): ")
    #print(response.json())
    #Hem de comprovar si l'usuari està ben autenticat
    
    

    if (response.json()!='Acces denegat'):
        
        #DEMANAM DADES API ENDPOINT /USERS
        urlUsers="http://87.235.201.250:8080/whatspau_php/users"
        headers={'Authorization': response.json()}
        usuaris=requests.request("GET",urlUsers,headers=headers,data=payload)
        #print(usuaris.status_code)
        #print(usuaris.json())
        #print(type(usuaris.json()))
        #print("************************")
        llistaUsers=usuaris.json()
        
        # DEMANAN DADES API ENDPOPINT /MISSATGES
        # OBTENIMS ELS MISSATGES ENVIATS A L'USUARI AUTENTICAT
        
        urlUsers="http://87.235.201.250:8080/whatspau_php/missatges"
        headers={'Authorization': response.json()}
        missatges=requests.request("GET",urlUsers,headers=headers,data=payload)
        #print(missatges.status_code)
        #print(missatges.json())
        #print(type(missatges.json()))
        #print("************************")
        llistaMissatges=missatges.json()
        
        # CREAM UN ARRAY QUE NOMÉS CONTENGUI EL id_sender DE llistaMissatges
        
        arrayIdSender=[]
        for llista in llistaMissatges:
            arrayIdSender.append(llista['id_sender'])
        #print(arrayIdSender)
        #print(type(arrayIdSender))
        #print("************************")
        
        # CREAM UNA LLISTA NOVA QUE PER A CADA ID_SENDER TINGUEM EL NUM. DE
        # MISSTAGES ENVIATS
        # [
        #  {'id_user': 1, 'numMissatges': n1},
        #  {'id_user': 2, 'numMissatges': n2},
        #
        #  {'id_user': n, 'numMissatges': nn},
        # ]
        
        numMissatgesNous=[]
        
        for i in set(arrayIdSender):
            numMissatgesNous.append({
                'id_user': i,
                'numMissatges': arrayIdSender.count(i)
            })
        #print(numMissatgesNous)
        #print(type(numMissatgesNous))
        #print("************************")
        
        # EN LA LLISTA llistaUsers 
        # AFEGFIM ELEMENT numMissatges A CADA DICCIONARI AMB VALOR = 0
        
        novaLlistaUsers=[]
        for usuari in llistaUsers:
            usuari.update({'numMissatges': 0})
        #print(llistaUsers)
        #print(type(llistaUsers))
        #print("************************")
        
        
        # ARA CAL MODIFICAR PER CADA USUARI numMissatges EN FUNCIÓ DE LA
        # INFORMACIÓ QUE TENIM EN numMisstagesNous
        for i in numMissatgesNous:
            for j in llistaUsers:
                if i['id_user']==j['id_user']:
                    j['numMissatges']=i['numMissatges']
            
        print(llistaUsers)
        print(type(llistaUsers))
        print("************************")
        
        #PREPARAM RENDER_TEMPLATE
        resp=make_response(render_template('UT7_whatspau_cabecera.html',
                                           amics=llistaUsers))
        
        # CREAM COOKIE AMB TOKEN
        resp.set_cookie('JWT',response.json())
        
        # RETORNAM RESPOSTA
        return resp
        
        #usuari ben autenticat
        #deixam el token a una cookie
        #demanam a la API les dades que hem de passar a la pàgina (que no ha de fer el javascript)
        #retornam UT7_whatspau_cabecera.html, on està indicat que carregui el main.js

    else:
    	return render_template('UT7_whatspau_login.html',loginmsg="Usuari incorrecte")



if __name__ == '__main__':
	app.run(debug=True,port="5000")
