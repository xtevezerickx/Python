import pymongo
from model import Usuario
from flask_jsonpify import jsonify

client = pymongo.MongoClient(host="localhost", port=27017)
db = client.python

class CrudRepository():
    def __init__(self, collection_name):
        self.collection_name = collection_name
    
    def save(self, obj):
        db[self.collection_name].insert_one(obj.__dict__)
    
    def findById(self, id):
        return db[self.collection_name].find_one({"_id": id})

    def findByFilter(self, filter):
        return db[self.collection_name].find(filter)

class UsuarioRepository(CrudRepository):
    
    def __init__(self, _collection_name):
        super().__init__(collection_name = _collection_name)
    
    #def save(self, novoUsuario):
    #    db.usuario.insert_one(novoUsuario.__dict__)

    def find(self, id):
        response = []
        for cursor in db.usuario.find({"nome":"Erick"}):
            usuario = Usuario(_id = cursor['_id'])
            usuario.idade = cursor['idade']
            usuario.dataAlteracao = cursor['dataAlteracao']
            response.append(usuario)
        return response
    
    def findById(self, id):
        return db.usuario.find_one({"_id": id})