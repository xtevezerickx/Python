from error_handling import ResourceNotFoundException, ResourceConflictException, UsernameNotFoundException
from passlib.hash import pbkdf2_sha256
from model import OAuth2AccessToken
import uuid
from datetime import datetime, timedelta


class UsuarioService():

    def __init__(self, repository, assembler):
        self.repository = repository
        self.assembler = assembler

    def save(self, usuario):
        usuario.password = pbkdf2_sha256.hash(usuario.password)
        if self.repository.findById(usuario._id) is not None:
            raise ResourceConflictException()
        self.repository.save(usuario)

    def findById(self, id):
        cursor = self.repository.findById(id)
        if cursor is None:
            raise ResourceNotFoundException()
        entity = self.assembler.cursorToEntity(cursor)
        entity.dataAlteracao = entity.dataAlteracao.isoformat()
        return entity

    def delete(self, id):
        cursor = self.repository.findById(id)
        if cursor is None:
            raise ResourceNotFoundException()
        self.repository.delete(id)


class OAuth2Service():

    def __init__(self, repository, usuarioService, oAuth2Assembler):
        self.repository = repository
        self.usuarioService = usuarioService
        self.oAuth2Assembler = oAuth2Assembler

    def getAccessToken(self, usuario):
        usuarioBanco = self.usuarioService.findById(usuario._id)
        if usuarioBanco is None:
            raise UsernameNotFoundException()
        if not pbkdf2_sha256.verify(usuario.password, usuarioBanco.password):
            raise UsernameNotFoundException()
        accessToken = str(uuid.uuid4())
        dataExpiracao = datetime.now() + timedelta(minutes=15)
        oauth2AccesToken = OAuth2AccessToken(accessToken = accessToken, usuario=usuarioBanco.__dict__, dataExpiracao= dataExpiracao)
        self.repository.save(oauth2AccesToken)
        return accessToken

    def findAccessToken(self, id):
        cursor = self.repository.findById(id)
        if cursor is None:
            raise ResourceNotFoundException()
        return self.oAuth2Assembler.cursorToEntity(cursor)






