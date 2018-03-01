from validator import NotNull
import json

@NotNull(attr_name="nome")
@NotNull(attr_name="idade")
class Usuario():
    def __init__(self, nome, idade = 0):
        self.nome = nome
        self.idade = idade
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)