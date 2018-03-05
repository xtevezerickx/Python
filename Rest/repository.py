import pymongo
import config

client = pymongo.MongoClient(host=config.MONGO_HOST, port=config.MONGO_PORT)
db = client[config.MONGO_DATABASE]

class CrudRepository:
    def __init__(self, collection_name):
        self.collection_name = collection_name

    def save(self, obj):
        db[self.collection_name].insert_one(obj.__dict__)

    def find_by_id(self, obj_id):
        return db[self.collection_name].find_one({"_id": obj_id})

    def find_by_filter(self, obj_fiter):
        return db[self.collection_name].find(obj_fiter)

    def delete(self, obj_id):
        db[self.collection_name].delete_one({"_id": obj_id})


class UsuarioRepository(CrudRepository):

    def __init__(self, _collection_name):
        super().__init__(collection_name=_collection_name)


class OAuth2AcessTokenRepository(CrudRepository):

    def __init__(self, _collection_name):
        super().__init__(collection_name=_collection_name)
