import pymongo
import config
client = pymongo.MongoClient(host=config.MONGO_HOST, port=config.MONGO_PORT)
db = client[config.MONGO_DATABASE]

class CrudRepository():
    def __init__(self, collection_name):
        self.collection_name = collection_name
    
    def save(self, obj):
        db[self.collection_name].insert_one(obj.__dict__)
    
    def findById(self, id):
        return db[self.collection_name].find_one({"_id": id})

    def findByFilter(self, filter):
        return db[self.collection_name].find(filter)

    def delete(self, id):
        db[self.collection_name].delete_one({"_id": id})

class UsuarioRepository(CrudRepository):
    
    def __init__(self, _collection_name):
        super().__init__(collection_name = _collection_name)

class OAuth2AcessTokenRepository(CrudRepository):

    def __init__(self, _collection_name):
        super().__init__(collection_name = _collection_name)
