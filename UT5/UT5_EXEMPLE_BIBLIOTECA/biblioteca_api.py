from flask import Flask, request
from flask_restful import Resource, Api
import database
import configparser
import datetime

server = Flask(__name__)
api = Api(server)
mt = database.biblioteca()

class llibres(Resource):
    def get(self,id_llibre):
        mt.conecta()
        resultat=mt.tornaLlibrePerID(id_llibre)
        mt.desconecta()
        return resultat

class llibres_autor(Resource):
    def get(self, id_autor):
        mt.conecta()
        resultat=mt.tornaLlibresPerIDautor(id_autor)
        mt.desconecta()
        return resultat

class editors(Resource):
    def get(self):
        mt.conecta()
        resultat=mt.tornaEditors()
        mt.desconecta()
        return resultat
    
    def post(self):
        mt.conecta()
        resultat=mt.nouEditor(request.json)
        mt.desconecta()
        return resultat

class editor(Resource):
    def get(self, id_editor):
        mt.conecta()
        resultat=mt.tornaEditorPerID(id_editor)
        mt.desconecta()
        return resultat

    def put(self,id_editor):
        mt.conecta()
        resultat=mt.modificaEditor(id_editor,request.json)
        mt.desconecta()
        return resultat
    
    def delete(self,id_editor):
        mt.conecta()
        resultat=mt.eliminaEditor(id_editor)
        mt.desconecta()
        


#GET
api.add_resource(llibres,'/llibres/<int:id_llibre>')

#GET
api.add_resource(llibres_autor,'/llibres/autor/<int:id_autor>')

#GET (tots els editors)
api.add_resource(editors,'/editors')

#GET (retorna 1 editor) POST (afegeix 1 editor) DELETE (elimina 1 editor)
api.add_resource(editor,'/editors/<int:id_editor>')






if __name__ == '__main__':
    server.run(debug=True)
