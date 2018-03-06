class Usuario:
    def __init__(self, **kwargs):
        params = {}
        for i in kwargs:
            params[i.lower()] = kwargs[i]

        self.nome = params.get('nome', None)
        self.data_alteracao = params.get('data_alteracao', None)
        self.data_criacao = params.get('data_criacao', None)
        self.password = params.get('password', None)
        self.email = params.get('email', None)


class OAuth2AccessToken:
    def __init__(self, access_token=None, data_expiracao=None):
        self.access_token = access_token
        self.data_expiracao = data_expiracao
