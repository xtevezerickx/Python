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
        return db[self.collection_name].find_one({'_id': obj_id})

    def find_by_filter(self, obj_fiter):
        return db[self.collection_name].find(filter = obj_fiter)

    def delete(self, obj_id):
        db[self.collection_name].delete_one({'_id': obj_id})


class UsuarioRepository(CrudRepository):

    def __init__(self, _collection_name):
        super().__init__(collection_name=_collection_name)
        db[self.collection_name].create_index([('email',pymongo.ASCENDING)], unique = True)

    def update(self, usuario):
        update = {
            '$currentDate': {
                'data_alteracao': {
                    '$type': 'date'
                }
            },
            '$set': {
                'nome': usuario.nome,
                'email' : usuario.email
            }
        }
        db[self.collection_name].update_one(filter={'_id': usuario._id}, update=update)

    def find_one_by_email(self, email):
        return db[self.collection_name].find_one({'email': email})


class OAuth2AcessTokenRepository(CrudRepository):

    def __init__(self, _collection_name):
        super().__init__(collection_name=_collection_name)
