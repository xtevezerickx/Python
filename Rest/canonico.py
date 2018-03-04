class Usuario():
    def __init__(self, nome = None, idade = None, dataAlteracao = None, password = None):
        self.nome = nome
        self.idade = idade
        self.dataAlteracao = dataAlteracao
        self.password = password

class OAuth2AccessToken():
    def __init__(self, accessToken = None):
        self.accessToken = accessToken