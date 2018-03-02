from validator import NotNull
import json
import datetime
class Usuario():
    
    collection_name = 'usuario'

    def __init__(self, _id = None, idade = None, dataAlteracao = None):
        self._id = _id
        self.idade = idade
        self.dataAlteracao = dataAlteracao
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)