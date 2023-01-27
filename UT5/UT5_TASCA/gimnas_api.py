from flask import Flask, request
from flask_restful import Resource, Api
import database
import configparser
import datetime

server = Flask(__name__)
api = Api(server)
mt = database.gimnas()

class usuaris(Resource):
    def get(self):
        mt.conecta()
        resultat = mt.tornaUsuaris()
        mt.desconecta()
        return resultat
    
    def post(self):
        mt.conecta()
        resultat=mt.nouUsuari(request.json)
        mt.desconecta()
        return resultat

class usuari(Resource):
    def get(self, id_usuari):
        mt.conecta()
        resultat = mt.tornaUsuariPerID(id_usuari)
        mt.desconecta()
        return resultat

    def put(self,id_usuari):
        mt.conecta()
        resultat=mt.modificaUsuari(id_usuari,request.json)
        mt.desconecta()
        return resultat
    
    def delete(self,id_usuari):
        mt.conecta()
        resultat=mt.eliminaUsuari(id_usuari)
        mt.desconecta()

class reservesSetmana(Resource):
    def get(self, data):
        mt.conecta()
        resultat=mt.tornaReservesSetmana(data)
        mt.desconecta()
        return resultat

class reservesSetmanaActual(Resource):
    def get(self):
        mt.conecta()
        resultat=mt.tornaReservesSetmanaActual()
        mt.desconecta()
        return resultat

class reservesUsuari(Resource):
    def get(self, id_usuari):
        mt.conecta()
        resultat = mt.tornaReservesUsuari(id_usuari)
        mt.desconecta()
        return resultat
    
    def post(self,id_usuari):
        mt.conecta()
        resultat=mt.novaReservaUsuari(id_usuari,request.json)
        mt.desconecta()
        return resultat
    
    def delete(self,id_usuari):
        mt.conecta()
        resultat=mt.eliminaReservaUsuari(id_usuari,request.json)
        mt.desconecta()

#GET (tots els usuaris) i POST (afegeix 1 usuari) 
api.add_resource(usuaris,'/gimnas/usuari')

#GET (retorna 1 usuari) PUT (modifica 1 usuari) DELETE (elimina 1 usuari)
api.add_resource(usuari,'/gimnas/usuari/<int:id_usuari>')

#GET retorna les reserves de la setmana segons la data indicada
api.add_resource(reservesSetmana,'/gimnas/reserves/setmana/<data>')

#GET retorna les reserves de la setmana actual
api.add_resource(reservesSetmanaActual,'/gimnas/reserves')

# GET (retorna reserves d'1 usuari) 
# POST (afegeix 1 reserva) 
# DELETE (elimina 1 reserva)
api.add_resource(reservesUsuari,'/gimnas/reserves/usuari/<int:id_usuari>')

if __name__ == '__main__':
    server.run(debug=True)









