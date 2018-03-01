
from validator import NotNull
from error_handling import ResourceBussinessException
@NotNull(attr_name="nome")
@NotNull(attr_name="idade")
class Usuario():
    def __init__(self, nome, idade = 0):
        self.nome = nome
        self.idade = idade