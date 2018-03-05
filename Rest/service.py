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
        usuario.password = pbkdf2_sha256.hash(usuario.password)
        if self.repository.find_by_id(usuario._id) is not None:
            raise ResourceConflictException()
        self.repository.save(usuario)

    def find_by_id(self, obj_id):
        cursor = self.repository.find_by_id(obj_id)
        if cursor is None:
            raise ResourceNotFoundException()
        entity = self.assembler.cursor_to_entity(cursor)
        entity.dataAlteracao = entity.dataAlteracao.isoformat()
        return entity

    def delete(self, obj_id):
        cursor = self.repository.find_by_id(obj_id)
        if cursor is None:
            raise ResourceNotFoundException()
        self.repository.delete(obj_id)


class OAuth2Service:

    def __init__(self, repository, usuario_service, oauth2_assembler):
        self.repository = repository
        self.usuario_service = usuario_service
        self.oauth2_assembler = oauth2_assembler

    def get_access_token(self, usuario):
        usuario_banco = self.usuario_service.find_by_id(usuario._id)
        if usuario_banco is None:
            raise UsernameNotFoundException()
        if not pbkdf2_sha256.verify(usuario.password, usuario_banco.password):
            raise UsernameNotFoundException()
        access_token = str(uuid.uuid4())
        data_expiracao = datetime.now() + timedelta(minutes=config.TOKEN_VALIDATE_MINUTES)
        oauth2_acces_token = OAuth2AccessToken(access_token=access_token, usuario=usuario_banco.__dict__,
                                               data_expiracao=data_expiracao)
        self.repository.save(oauth2_acces_token)
        return access_token

    def find_access_token(self, obj_id):
        cursor = self.repository.find_by_id(obj_id)
        if cursor is None:
            raise ResourceNotFoundException()
        return self.oauth2_assembler.cursor_to_tntity(cursor)
