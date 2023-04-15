from flask import Flask, render_template, request, session, make_response
import numpy as np
import datetime
import requests
import json


app = Flask(__name__)
app.config['SECRET_KEY']="mysecretkey"
API_url="http://87.235.201.250:8080/whatspau_php"

@app.route('/')
def index():
    return render_template('UT7_whatspau_login.html')

@app.route('/signin')
def signin():
    return render_template('UT7_whatspau_login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    
    usuari=request.form['usuari']
    pwd=request.form['password']
    
    #PREPARAM CONSULTA A L'API
    payload={"username":usuari, "password":pwd}
    
    
    # ENVIAM CONSULTA AUTH A API
    response=requests.post(API_url+"/login",data=payload)
    #print("response.status_code: ")
    #print(response.status_code)
    #print("response.json: ")
    #print(response.json())
    

    # COMPROVEM QUE L'USUARI ESTÀ BEN AUTENTICAT

    if (response.json()!="Acces denegat"):

        # DEMANAM DADES API ENDPOINT /USERS
        urlUsers=API_url+"/users"
        headers = {'Authorization': response.json()}
        usuaris=requests.request("GET",urlUsers, headers=headers, data=payload)
        #print(usuaris.status_code)
        #print(usuaris.json())
        #print(type(usuaris.json()))
        llistaUsers=usuaris.json()
        

        # DEMANAM DADES API ENDPOINT /MISSATGES
        urlMissatges=API_url+"/missatges"
        missatgesNous=requests.request("GET",urlMissatges, headers=headers, data=payload)
        #print(missatgesNous.json())

        # OBTENIM NUMERO MISSATGES NOUS PER CADA ID_SENDER

        arrayIdSender=[]
        for llista in missatgesNous.json():
            arrayIdSender.append(llista['id_sender'])
        #print(arrayIdSender)

        numMissatgesNous = []

        # CREAM UNA LLISTA NOVA AMB L'ESTRUCTURA SEGÜENT:
        # [
        #   {'id_user': 1, 'nousMissatges': n1}, 
        #   {'id_user': 2, 'nousMissatges': n2},
        #   .....
        #   {'id_user': n, 'nousMissatges': nn}
        # ]

        for i in set(arrayIdSender):
            numMissatgesNous.append({
                'id_user': i,
                'nousMissatges': arrayIdSender.count(i)
            })
        #print(numMissatgesNous)

        # CREAM UNA NOVA LLISTA D'USUARIS
        # AFEGIM L'ELEMENT nousMissatges A CADA DICCIONARI amb el valor 0
        
        novaLlistaUsers = []
        for usuari in llistaUsers:
            usuari.update({"nousMissatges":0})
            novaLlistaUsers.append(usuari)
        #print(novaLlistaUsers)
        
        # ACTUALITZAM novaLlistaUsers AMB VALORS numMissatgesNous
        
        for element2 in numMissatgesNous:
            for element1 in novaLlistaUsers:
                if (element1['id_user']==element2['id_user']):
                     element1['nousMissatges']=element2['nousMissatges']
        #print(novaLlistaUsers)
        
        # DEMANAM DADES API ENDPOINT /GRUPS
        urlGrups=API_url+"/grups"
        headers = {'Authorization': response.json()}
        llistaGrups=requests.request("GET",urlGrups, headers=headers, data=payload)
        #print(llistaGrups.json())
        #print(type(llistaGrups.json()))
        
        # CREAM UN NOU ARRAY COMBINANT USUARIS "AMICS" I GRUPS
        llistaUsersGrups = []
        
        # Iteram novaLlistaUsers per crear els elements tipus "amic"
        for user in novaLlistaUsers:
            llistaUsersGrups.append({"tipus": "amic", 
                                     "id": user["id_user"], 
                                     "name": user["username"], 
                                     "nousMissatges": user["nousMissatges"]})

        # Iteram llistaGrups per crear els elements tipus "grup"
        for grup in llistaGrups.json():
            llistaUsersGrups.append({"tipus": "grup", 
                                     "id": grup["id_grup"],
                                     "name": grup["grupname"],
                                     "nousMissatges": "No disponible"})

        # Ordenam array per id
        llistaUsersGrupsOrd = sorted(llistaUsersGrups, key=lambda x: x['id'])
        #print(llistaUsersGrupsOrd)

        #PREPARAM RENDER_TEMPLATE
        resp=make_response(render_template('UT7_whatspau_cabecera.html'
                                           , usersGrups=llistaUsersGrupsOrd))
        
        # CREAM COOKIE AMB AUTORITZACIÓ
        resp.set_cookie('JWT',response.json())
        
        
             
        return resp
    
    else:
        return render_template('UT7_whatspau_login.html', loginmsg=response.json())

if __name__=='__main__':
    app.run(debug=True, port="5000")
