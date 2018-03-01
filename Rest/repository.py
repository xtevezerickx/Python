import pymongo
import model
from flask_jsonpify import jsonify

client = pymongo.MongoClient(host="localhost", port=27017)
db = client.python
class UsuarioRepository():
    
    def save(self, novoUsuario):
        db.usuario.insert_one(novoUsuario.toJson())