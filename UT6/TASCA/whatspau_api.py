from flask import Flask, request
from flask_restful import Resource, Api
import database
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
app.config['SECRET_KEY'] = "keysupersecreta"
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
        resultat = mt.tornaUsername(current_identity.id)
        mt.desconecta()
        return resultat
    
class missatges(Resource):
    @jwt_required()
    def get(self):
        mt.conecta()
        resultat = mt.tornaTotsMissatges()
        mt.desconecta()
        return resultat

class check(Resource):
    @jwt_required()
    def get(self):
        mt.conecta()
        resultat = mt.tornaNumMissatges(current_identity.id)
        mt.desconecta()
        return resultat

class conversa(Resource):
    @jwt_required()
    def get(self, id_interlocutor):        
        mt.conecta()
        resultat = mt.tornaMissatgesConversa(id_interlocutor,current_identity.id)
        mt.desconecta()
        return resultat
    
    @jwt_required()
    def post(self, id_interlocutor):
        mt.conecta()
        resultat = mt.nouMissatge(id_interlocutor,current_identity.id,request.json)
        mt.desconecta()
        return resultat

class missatgesrebuts(Resource):
    @jwt_required()
    def put(self):
        mt.conecta()
        resultat = mt.canviaStatusRebut(current_identity.id)
        mt.desconecta()
        return resultat
    
class missatgesllegits(Resource):
    @jwt_required()
    def put(self):
        mt.conecta()
        resultat = mt.canviaStatusLlegit(current_identity.id)
        mt.desconecta()
        return resultat

# GET (tots els usuaris excepte l’usuari que fa la consulta)
api.add_resource(users, '/users')

# GET (tots els missatges amb status "Enviat")
api.add_resource(missatges, '/missatges')

# GET (numero de missatges de l'usuari amb status "Enviat")
# El numero de missatges inclou tant els missatges en que l'usuari
# és id_sender com els missatges en que és id_receiver
# Si només volem recuperar el num de missatges quan usuari és id_sender,
# la consulta sql es simplifica (igual per id_receiver)
api.add_resource(check, '/check')

# GET (retorna tots els missatges d'una conversa entre l'usuari autenticat
#      i un altre usuari especificat)
# POST (envia un missatge a la conversa entre l'usuari autenticat 
#      i un usuari en concret)
api.add_resource(conversa, '/conversa/<int:id_interlocutor>')

# PUT (canvia l'status dels missatges enviats a l'usuari autenticat,
#      de 'send' a 'received')
api.add_resource(missatgesrebuts, '/missatgesrebuts')

# PUT (canvia l'status dels missatges rebuts per l'usuari autenticat,
#      de 'received' a 'read')
api.add_resource(missatgesllegits, '/missatgesllegits')


#
# TASCA AVANÇADA
#

class grups(Resource):
    @jwt_required()
    def get(self):
        mt.conecta()
        resultat = mt.tornaGrups(current_identity.id)
        mt.desconecta()
        return resultat

class membresgrups(Resource):
    @jwt_required()
    def get(self):
        mt.conecta()
        resultat = mt.tornaMembresGrups(current_identity.id)
        mt.desconecta()
        return resultat

class mgcheck(Resource):
    @jwt_required()
    def get(self):
        mt.conecta()
        resultat = mt.tornaNumMissatgesGrup(current_identity.id)
        mt.desconecta()
        return resultat

class conversagrup(Resource):
    @jwt_required()
    def get(self,id_grup):        
        mt.conecta()
        resultat = mt.tornaMissatgesConversaGrup(id_grup,current_identity.id)
        mt.desconecta()
        return resultat
    
    @jwt_required()
    def post(self, id_grup):
        mt.conecta()
        resultat = mt.nouMissatgeGrup(id_grup,current_identity.id,request.json)
        mt.desconecta()
        return resultat


class mgrebuts(Resource):
    @jwt_required()
    def put(self, id_grup):
        mt.conecta()
        resultat = mt.canviaGrupStatusRebut(id_grup,current_identity.id)
        mt.desconecta()
        return resultat
    
class mgllegits(Resource):
    @jwt_required()
    def put(self, id_grup):
        mt.conecta()
        resultat = mt.canviaGrupStatusLlegit(id_grup,current_identity.id)
        mt.desconecta()
        return resultat


# GET (retorna els grups al qual pertany l'usuari autenticat)
api.add_resource(grups, '/grups')

# GET (retorna els membres dels grups al qual pertany l'usuari autenticat)
api.add_resource(membresgrups, '/membresgrups')

# GET (retorna el numero de missatges amb status 'send' que té l'usuari 
#      autenticat per cada grup al que pertany)
api.add_resource(mgcheck, '/mgcheck')

# GET (retorna tots els missatges del grup)
# POST (envia un missatge a un grup de conversa)
api.add_resource(conversagrup, '/conversagrup/<int:id_grup>')

# PUT (canvia l'status dels missatges enviats a l'usuari autenticat,
#      de 'send' a 'received' en el grup de conversa indicat)
api.add_resource(mgrebuts, '/mgrebuts/<int:id_grup>')

# PUT (canvia l'status dels missatges rebuts per l'usuari autenticat,
#      de 'received' a 'read' en el grup de conversa indicat)
api.add_resource(mgllegits, '/mgllegits/<int:id_grup>')


if __name__ == '__main__':
    app.run(debug=True)
