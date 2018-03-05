import model as model
import canonico as canonic


class UsuarioAssembler:

    def to_entity(self, resource):
        entity = model.Usuario()
        entity._id = resource.nome
        entity.password = resource.password
        return entity

    def to_resource(self, entity):
        resource = canonic.Usuario()
        resource.nome = entity._id
        resource.data_alteracao = entity.data_alteracao
        return resource

    def cursor_to_entity(self, cursor):
        entity = model.Usuario()
        entity._id = cursor['_id']
        entity.data_alteracao = cursor['data_alteracao']
        entity.password = cursor['password']
        return entity

    def cursor_to_resource(self, cursor):
        return self.to_resource(self.cursor_to_entity(cursor))

    def request_to_resource(self, request):
        resource = canonic.Usuario()
        resource.nome = request.json['nome']
        resource.password = request.json['password']
        return resource

    def request_to_entity(self, request):
        return self.to_entity(self.request_to_resource(request))


class OAuth2AccessTokenAssembler:

    def cursor_to_entity(self, cursor):
        entity = model.OAuth2AccessToken()
        entity._id = cursor['_id']
        entity.usuario = UsuarioAssembler().cursor_to_entity(cursor['usuario'])
        entity.dataExpiracao = cursor['data_expiracao']
        return entity
