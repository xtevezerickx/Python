from error_handling import ResourceNotFoundException, ResourceConflictException, UsernameNotFoundException
from passlib.hash import pbkdf2_sha256
from model import OAuth2AccessToken
from datetime import datetime, timedelta
import config
import uuid

class UsuarioService:

    def __init__(self, repository, assembler):
        self.repository = repository
        self.assembler = assembler

    def save(self, usuario):
        data = datetime.now()
        usuario._id = str(uuid.uuid4())
        usuario.data_alteracao = data
        usuario.data_criacao = data
        usuario.password = pbkdf2_sha256.hash(usuario.password)
        cursor = self.repository.find_by_filter({'email': usuario.email})
        documents = []
        for i in cursor:
            documents.append(i)
        if len(documents) > 0:
            raise ResourceConflictException('Já existe um usuario com este email.')
        self.repository.save(usuario)

    def find_by_id(self, obj_id):
        cursor = self.repository.find_by_id(obj_id)
        if cursor is None:
            raise ResourceNotFoundException('Usuário não encontrado.')
        entity = self.assembler.cursor_to_entity(cursor)
        entity.data_alteracao = entity.data_alteracao.isoformat()[:-3]
        entity.data_criacao = entity.data_criacao.isoformat()[:-3]
        return entity

    def delete(self, obj_id):
        cursor = self.repository.find_by_id(obj_id)
        if cursor is None:
            raise ResourceNotFoundException('Usuario não encontrado')
        self.repository.delete(obj_id)

    def update(self, usuario):
        cursor = self.repository.find_one_by_email({'email': usuario.email})
        if cursor is not None and cursor['_id'] is not usuario._id:
            raise ResourceConflictException('Já existe um usuário com este email.')
        self.repository.update(usuario)

    def find_one_by_email(self, email):
        cursor = self.repository.find_one_by_email(email)
        entity = self.assembler.cursor_to_entity(cursor)
        return entity


class OAuth2Service:

    def __init__(self, repository, usuario_service, oauth2_assembler):
        self.repository = repository
        self.usuario_service = usuario_service
        self.oauth2_assembler = oauth2_assembler

    def get_access_token(self, usuario):
        usuario_banco = self.usuario_service.find_one_by_email(usuario.email)
        if usuario_banco is None:
            raise UsernameNotFoundException()
        if not pbkdf2_sha256.verify(usuario.password, usuario_banco.password):
            raise UsernameNotFoundException()
        access_token = str(uuid.uuid4())
        data_expiracao = datetime.now() + timedelta(minutes=config.TOKEN_VALIDATE_MINUTES)
        oauth2_acces_token = OAuth2AccessToken(access_token=access_token, usuario=usuario_banco.__dict__,
                                               data_expiracao=data_expiracao)
        self.repository.save(oauth2_acces_token)
        return access_token, data_expiracao

    def find_access_token(self, obj_id):
        cursor = self.repository.find_by_id(obj_id)
        if cursor is None:
            raise ResourceNotFoundException()
        return self.oauth2_assembler.cursor_to_entity(cursor)
