from validator import NotNull
import json
import datetime
class Usuario():
    
    collection_name = 'usuario'

    def __init__(self, _id = None, idade = None):
        self._id = _id
        self.idade = idade
        self.dataAlteracao = datetime.datetime.now()
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)