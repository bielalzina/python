from flask import Flask, request
from flask_restful import Resource, Api
import database

server = Flask(__name__)
api = Api(server)
mt = database.whatspau()

class users(Resource):
    def get(self):
        mt.conecta()
        resultat = mt.tornaUsername()
        mt.desconecta()
        return resultat


####    
class user(Resource):
    def get(self):
        mt.conecta()
        resultat = mt.autenticaUsuari(request.json)
        mt.desconecta()
        #return resultat

api.add_resource(user, '/user')


####







# GET (tots els usuaris excepte l’usuari que fa la consulta)
api.add_resource(users, '/users')


if __name__ == '__main__':
    server.run(debug=True)
