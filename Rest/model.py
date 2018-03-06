from json import dumps
class Usuario:

    def __init__(self, **kwargs):
        params = {}
        for i in kwargs:
            params[i.lower()] = kwargs[i]

        self._id = params.get('_id', None)
        self.data_alteracao = params.get('data_alteracao', None)
        self.data_criacao = params.get('data_criacao', None)
        self.password = params.get('password', None)
        self.nome = params.get('nome', None)
        self.email = params.get('email', None)

    def __str__(self):
        aux = self.__dict__
        aux['data_alteracao'] = None
        aux['data_criacao'] = None
        return dumps(aux, ensure_ascii=False)


class OAuth2AccessToken:

    def __init__(self, access_token=None, usuario=None, data_expiracao=None):
        self._id = access_token
        self.usuario = usuario
        self.data_expiracao = data_expiracao
