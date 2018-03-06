import model as model
import canonico as canonic


class UsuarioAssembler:

    def to_entity(self, resource):
        entity = model.Usuario()
        entity.email = resource.email
        entity.password = resource.password
        entity.nome = resource.nome
        entity.data_criacao = resource.data_criacao
        entity.data_alteracao = resource.data_alteracao
        return entity

    def to_resource(self, entity):
        resource = canonic.Usuario()
        resource.nome = entity.nome
        resource.data_alteracao = entity.data_alteracao
        resource.email = entity.email
        resource.data_criacao = entity.data_criacao
        resource.data_alteracao = entity.data_alteracao
        return resource

    def cursor_to_entity(self, cursor):
        if cursor is not None:
            entity = model.Usuario()
            entity._id = cursor['_id']
            entity.data_alteracao = cursor['data_alteracao']
            entity.password = cursor['password']
            entity.data_criacao = cursor['data_criacao']
            entity.nome = cursor['nome']
            entity.email = cursor['email']
            return entity


    def cursor_to_resource(self, cursor):
        return self.to_resource(self.cursor_to_entity(cursor))

    def request_to_resource(self, request):
        resource = canonic.Usuario()
        resource.nome = request.json['nome']
        if 'password' in request.json:
            resource.password = request.json['password']
        resource.email = request.json['email']
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
