from flask import Flask
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
api = Api(app)

jwt = JWT(app, authenticate, identity)

# Later on this will be a model call to our database!
# Right now its just a list of dictionaries
# puppies = [{'name':'Rufus'},{name:'Frankie'},......]
# Keep in mind, its in memory, it clears with every restart!

puppies = []

class PuppyNames(Resource):
    
    def get(self,name):
        print(puppies)
        
        # Cercam en variable puppies
        for pup in puppies:
            if pup['name'] == name:
                return pup
        
        # Si no existeix
        return {'name':None},404
    
    def post(self, name):
        # Afegim mascota a puppies
        pup = {'name':name}
        puppies.append(pup)
        # Responem
        print(puppies)
        return pup
    
    def delete(self,name):
        # Cercam en puppies
        for ind, pup in enumerate(puppies):
            if pup['name']==name:
                #esborram
                puppies.pop(ind)
                return {'note': 'Puppy eliminat'}

class AllNames(Resource):

    @jwt_required()
    def get(self):
        # return all the puppies :)
        print(puppies)
        return {'puppies': puppies}


api.add_resource(PuppyNames,'/puppy/<string:name>')
api.add_resource(AllNames,'/puppies')


if __name__ == '__main__':
    app.run(debug=True)