class Usuario():
    
    def __init__(self, _id = None, idade = None, dataAlteracao = None, password = None):
        self._id = _id
        self.idade = idade
        self.dataAlteracao = dataAlteracao
        self.password = password

class OAuth2AccessToken():

    def __init__(self, accessToken = None, usuario = None, dataExpiracao = None):
        self._id = accessToken
        self.usuario = usuario
        self.dataExpiracao = dataExpiracao