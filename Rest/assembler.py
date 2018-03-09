import model as model
import canonico as canonic


class UsuarioAssembler:

    def __init__(self, endereco_assembler):
        self.endereco_assembler = endereco_assembler

    def to_entity(self, resource):
        entity = model.Usuario()
        ignore = ['id', 'endereco']
        for name in resource.__dict__:
            if name in ignore:
                continue
            entity.__setattr__(name, resource.__getattribute__(name))
        entity.endereco = self.endereco_assembler.to_entity(resource.endereco)

        return entity

    def to_resource(self, entity):
        resource = canonic.Usuario()
        ignore = ['id', 'endereco']
        for name in entity.__dict__:
            if name in ignore:
                continue
            resource.__setattr__(name, entity.__getattribute__(name))
        resource.endereco = self.endereco_assembler.to_resource(entity.endereco)

        return resource

    def cursor_to_entity(self, cursor):
        if cursor is not None:
            entity = model.Usuario()
            entity._id = cursor['_id']
            entity.nome = cursor['nome']
            entity.email = cursor['email']
            entity.rg = cursor['rg']
            entity.cpf = cursor['cpf']
            entity.endereco = self.endereco_assembler.cursor_to_entity(cursor['endereco'])
            entity.password = cursor['password']
            entity.data_alteracao = cursor['data_alteracao']
            entity.data_criacao = cursor['data_criacao']
            entity.facebook = cursor['facebook']
            entity.twitter = cursor['twitter']
            entity.whatsapp = cursor['whatsapp']
            entity.telefone = cursor['telefone']

            return entity


    def cursor_to_resource(self, cursor):
        return self.to_resource(self.cursor_to_entity(cursor))


    def request_to_resource(self, request):
        resource = canonic.Usuario()
        resource.nome = request.json['nome']
        resource.email = request.json['email']
        if 'password' in request.json:
            resource.password = request.json['password']
        resource.rg = request.json['rg']
        resource.cpf = request.json['cpf']
        resource.endereco = self.endereco_assembler.request_to_resource(request)
        resource.facebook = request.json['facebook']
        resource.twitter = request.json['twitter']
        resource.whatsapp = request.json['whatsapp']
        resource.telefone = request.json['telefone']
        return resource

    def request_to_entity(self, request):
        return self.to_entity(self.request_to_resource(request))


class OAuth2AccessTokenAssembler:

    def __init__(self, usuario_assembler):
        self.usuario_assembler = usuario_assembler

    def cursor_to_entity(self, cursor):
        entity = model.OAuth2AccessToken()
        entity._id = cursor['_id']
        entity.usuario = self.usuario_assembler.cursor_to_entity(cursor['usuario'])
        entity.dataExpiracao = cursor['data_expiracao']
        return entity

class EnderecoAssembler:

    def to_entity(self, resource):
        entity = model.Endereco()
        for name in resource.__dict__:
            entity.__setattr__(name, resource.__getattribute__(name))
        return entity

    def to_resource(self, entity):
        resource = canonic.Endereco()
        for name in entity.__dict__:
            resource.__setattr__(name, entity.__getattribute__(name))
        return resource

    def cursor_to_entity(self, cursor):
        entity = model.Endereco()
        entity.endereco = cursor['endereco']
        entity.numero = cursor['numero']
        entity.estado = cursor['estado']
        entity.cidade = cursor['cidade']
        entity.cep = cursor['cep']
        entity.latitude = cursor['latitude']
        entity.longitude = cursor['longitude']
        return entity

    def request_to_resource(self, request):
        resource = canonic.Endereco()
        endereco = request.json['endereco']
        resource.endereco = endereco['endereco']
        resource.numero = endereco['numero']
        resource.estado = endereco['estado']
        resource.cidade = endereco['cidade']
        resource.cep = endereco['cep']
        return resource

