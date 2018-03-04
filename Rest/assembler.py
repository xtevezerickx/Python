import model as model
import canonico as canonic


class UsuarioAssembler():
    
    def toEntity(self, resource):
        entity = model.Usuario()
        entity._id = resource.nome
        entity.idade = resource.idade
        entity.password = resource.password
        return entity
    
    def toResource(self, entity):
        resource = canonic.Usuario()
        resource.nome = entity._id
        resource.idade = entity.idade
        resource.dataAlteracao = entity.dataAlteracao
        return resource

    def cursorToEntity(self, cursor):
        entity = model.Usuario()
        entity._id = cursor['_id']
        entity.idade = cursor['idade']
        entity.dataAlteracao = cursor['dataAlteracao']
        entity.password = cursor['password']
        return entity
    
    def cursorToResource(self, cursor):
        return self.toResource(self.cursorToEntity(cursor))

    def requestToResource(self, request):
        resource = canonic.Usuario()
        resource.nome =  request.json['nome']
        resource.idade = request.json['idade']
        resource.password = request.json['password']
        return resource

    def requestToEntity(self, request):
        return self.toEntity(self.requestToResource(request))


class OAuth2AccessTokenAssembler():

    def cursorToEntity(self, cursor):
        entity = model.OAuth2AccessToken()
        entity._id = cursor['_id']
        entity.usuario = UsuarioAssembler().cursorToEntity(cursor['usuario'])
        entity.dataExpiracao = cursor['dataExpiracao']
        return entity
