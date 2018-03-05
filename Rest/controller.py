import datetime
from flask import Flask, request, Response
from flask_restful import Api
from json import dumps
from flask_jsonpify import jsonify
from error_handling import ResourceBussinessException, ResourceNotFoundException, ResourceConflictException, \
    UsernameNotFoundException
from service import UsuarioService, OAuth2Service
from repository import UsuarioRepository, OAuth2AcessTokenRepository
from assembler import UsuarioAssembler, OAuth2AccessTokenAssembler
from functools import wraps
from model import Usuario
from canonico import OAuth2AccessToken

usuario_repository = UsuarioRepository(_collection_name='usuario')
usuario_assembler = UsuarioAssembler()
usuario_service = UsuarioService(repository=usuario_repository, assembler=usuario_assembler)

oauth2_repository = OAuth2AcessTokenRepository(_collection_name='oAuth2AccessToken')
oauth2_assembler = OAuth2AccessTokenAssembler()
oauth2_service = OAuth2Service(repository=oauth2_repository,
                               usuario_service=usuario_service,
                               oauth2_assembler=oauth2_assembler)

app = Flask(__name__)
api = Api(app)


def logado(func):
    @wraps(func)
    def inner(*args, **kwargs):
        authorization = request.headers.get('Authorization')
        if authorization is None:
            return Response(status=401)
        else:
            try:
                token = oauth2_service.find_access_token(authorization)
                if token is None or datetime.datetime.now() >= token.dataExpiracao:
                    return Response(status=401)
            except ResourceNotFoundException:
                return Response(status=401)
            return func(*args, **kwargs)

    return inner


def tratar_resource_bussiness_exception(exception):
    response = jsonify(exception.to_dict())
    response.status_code = exception.status_code
    return response


@app.route('/usuarios', methods=['POST'])
def salvar_usuario():
    try:
        entity = usuario_assembler.request_to_entity(request)
        entity.dataAlteracao = datetime.datetime.now()
        usuario_service.save(entity)
        return Response(status=201, content_type="application/json")
    except ResourceBussinessException as exception:
        return tratar_resource_bussiness_exception(exception)
    except ResourceConflictException:
        return Response(status=409)


@app.route('/usuarios/<usuario_id>', methods=['GET'])
def buscar_usuario(usuario_id):
    try:
        entity = usuario_service.find_by_id(usuario_id)
        resource = usuario_assembler.to_resource(entity)
        json_string = dumps(resource.__dict__)
        return Response(response=str(json_string), content_type="application/json")
    except ResourceNotFoundException:
        return Response(status=404)


@app.route('/usuarios/self', methods=['GET'])
@logado
def buscar_usuario_self():
    authorization = request.headers.get('Authorization')
    usuario = oauth2_service.find_access_token(authorization).usuario
    return buscar_usuario(usuario._id)


@app.route('/usuarios/<usuario_id>', methods=['PUT'])
def alterar_usuario(usuario_id):
    return Response()


@app.route('/usuarios/<usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    usuario_service.delete(usuario_id)
    return Response()


@app.route('/oauth/token', methods=['POST'])
def get_access_token():
    try:
        username = request.args.get("username")
        password = request.args.get("password")
        access_token = oauth2_service.get_access_token(Usuario(_id=username, password=password))
        retorno = OAuth2AccessToken(access_token=access_token)
        return Response(status=200, response=str(dumps(retorno.__dict__)), content_type="application/json")
    except UsernameNotFoundException:
        return Response(status=400)
    except ResourceNotFoundException:
        return Response(status=400)


app.run(port=5002)
