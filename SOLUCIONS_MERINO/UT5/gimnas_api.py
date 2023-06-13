from flask import Flask, request
from flask_restful import Resource, Api
import database


server = Flask(__name__)
api = Api(server)
mt = database.gimnas()


class usuaris(Resource):
    def get(self):
        mt.connecta()
        resultat = mt.tornaUsuaris()
        mt.desconnecta()
        return resultat

    def post(self):
        mt.connecta()
        resultat = mt.desaNouUsuari(request.json)
        mt.desconnecta()
        return resultat


class usuari(Resource):
    def get(self, idusuari):
        mt.connecta()
        resultat = mt.tornaUsuariPerID(idusuari)
        mt.desconnecta()
        return resultat

    def put(self, idusuari):
        mt.connecta()
        resultat = mt.modificaUsuariPerID(idusuari, request.json)
        mt.desconnecta()
        return resultat

    def delete(self, idusuari):
        mt.connecta()
        resultat = mt.esborraUsuari(idusuari)
        mt.desconnecta()
        return resultat


class reservesSetmanaData(Resource):
    def get(self, data):
        mt.connecta()
        resultat = mt.tornaReservesSegonsData(data)
        mt.desconnecta()
        return resultat


class reservesSetmanaActual(Resource):
    def get(self):
        mt.connecta()
        resultat = mt.tornaReservesSetmanaActual()
        mt.desconnecta()
        return resultat


class reservesUsuari(Resource):
    def get(self, idusuari):
        mt.connecta()
        resultat = mt.tornaReservesUsuari(idusuari)
        mt.desconnecta()
        return resultat

    def post(self, idusuari):
        mt.connecta()
        resultat = mt.novaReservaUsuari(idusuari, request.json)
        mt.desconnecta()
        return resultat


# GET (tots els usuaris) i POST (afegeix 1 usuari)
api.add_resource(usuaris, '/gimnas/usuaris')

# GET (retorna 1 usuari), PUT (modifica 1 usuari), DELETE (esborra 1 usuari)
api.add_resource(usuari, '/gimnas/usuari/<int:idusuari>')

# GET retorna llista reserves de la setmana segons DATA indicada)
api.add_resource(reservesSetmanaData, '/gimnas/setmana/data/<data>')


# GET retorna llista reserves de la setmana actual)
api.add_resource(reservesSetmanaActual, '/gimnas/reserves')

# GET (retorna reserces usuari), POST (afegeix reserva usuari),
# DELETE (esborra reserva usuari)
api.add_resource(reservesUsuari, '/gimnas/reserves/usuari/<int:idusuari>')

if __name__ == '__main__':
    server.run(debug=True, port=5001)
