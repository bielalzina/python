from flask import Flask, request
from flask_restful import Resource, Api
import database
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
app.config['SECRET_KEY'] = "clausecreta"
api = Api(app)

mt = database.whatspau()

jwt = JWT(app, authenticate, identity)

#
# SERVEIS PROTEGITS PER @jwt_required
#


class users(Resource):
    @jwt_required()
    def get(self):
        mt.conecta()
        resultat = mt.tornaUsernames(current_identity.id)
        mt.desconecta()
        return resultat


# GET retorna els usernames excepte el de l'usuari autenticat
api.add_resource(users, '/users')


class missatges(Resource):
    @jwt_required()
    def get(self):
        mt.conecta()
        resultat = mt.tornaTotsMissatgesSend()
        mt.desconecta()
        return resultat


# GET retorna tots els missatges amb status SEND
api.add_resource(missatges, '/missatges')


class check(Resource):
    @jwt_required()
    def get(self):
        mt.conecta()
        resultat = mt.tornaNumMissatges(current_identity.id)
        mt.desconecta()
        return resultat


# GET retorna el num. de missatges qe l'usuari amb status SEND
api.add_resource(check, '/check')


class conversa(Resource):
    @jwt_required()
    def get(self, id_interlocutor):
        mt.conecta()
        resultat = mt.tornaConversa(id_interlocutor, current_identity.id)
        mt.desconecta()
        return resultat

    @jwt_required()
    def post(self, id_interlocutor):
        mt.conecta()
        resultat = mt.nouMissatge(
            id_interlocutor, current_identity.id, request.json)
        mt.desconecta()
        return resultat


# GET retorna la conversa entre usuari autenticat i usuari especificat
# POST envia un missatge a la conversa entre usuari autenticat i usuari especificat
api.add_resource(conversa, '/missatges/<int:id_interlocutor>')


class missatgesRebuts(Resource):
    @jwt_required()
    def put(self):
        mt.conecta()
        resultat = mt.canviaStatusRebut(current_identity.id)
        mt.desconecta()
        return resultat


# PUT canvia status missatge de send a received
api.add_resource(missatgesRebuts, '/missatgesRebuts')


class missatgesLlegits(Resource):
    @jwt_required()
    def put(self):
        mt.conecta()
        resultat = mt.canviaStatusLlegit(current_identity.id)
        mt.desconecta()
        return resultat


# PUT canvia status missatge de send a received
api.add_resource(missatgesLlegits, '/missatgesLlegits')


if __name__ == '__main__':
    app.run(debug=True)
