import datetime
import threading
from flask import Flask, request, Response
from flask_restful import Api
from json import dumps
from flask_jsonpify import jsonify
from error_handling import ResourceBussinessException, ResourceNotFoundException, ResourceConflictException,\
    UsernameNotFoundException
from service import UsuarioService, OAuth2Service, GoogleMapsService
from repository import UsuarioRepository, OAuth2AcessTokenRepository
from assembler import UsuarioAssembler, OAuth2AccessTokenAssembler, EnderecoAssembler
from functools import wraps
from model import Usuario
from canonico import OAuth2AccessToken

endereco_assembler = EnderecoAssembler()

usuario_repository = UsuarioRepository(_collection_name='usuario')
usuario_assembler = UsuarioAssembler(endereco_assembler=endereco_assembler)
usuario_service = UsuarioService(repository=usuario_repository, assembler=usuario_assembler)

oauth2_repository = OAuth2AcessTokenRepository(_collection_name='oAuth2AccessToken')
oauth2_assembler = OAuth2AccessTokenAssembler(usuario_assembler = usuario_assembler)
oauth2_service = OAuth2Service(repository=oauth2_repository,
                               usuario_service=usuario_service,
                               oauth2_assembler=oauth2_assembler)

google_maps_service = GoogleMapsService()

app = Flask(__name__)
api = Api(app)


def logado(func):
    @wraps(func)
    def inner(*args, **kwargs):
        authorization = request.headers.get('Authorization')
        if authorization is None:
            json_string = dumps({'message': 'Você deve estar logado para acessar este recurso'}, ensure_ascii=False)
            return Response(status=401, response=json_string, content_type="application/json")
        else:
            try:
                token = oauth2_service.find_access_token(authorization)
                if token is None or datetime.datetime.now() >= token.dataExpiracao:
                    json_string = dumps({'message': 'Sessão expirada'}, ensure_ascii=False)
                    return Response(status=401, response=json_string, content_type="application/json")
            except ResourceNotFoundException:
                json_string = dumps({'message': 'Token não encontrado'}, ensure_ascii=False)
                return Response(status=401, response=json_string, content_type="application/json")
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
        address = entity.endereco.endereco + " , " + entity.endereco.cep + " , " + entity.endereco.estado
        lat, lng = google_maps_service.get_lat_lng_from_address(address)
        entity.endereco.latitude = lat
        entity.endereco.longitude = lng
        usuario_service.save(entity)
        return Response(status=201, content_type="application/json")
    except ResourceBussinessException as exception:
        return tratar_resource_bussiness_exception(exception)
    except ResourceConflictException as e:
        json_string = dumps(e.__dict__, ensure_ascii=False)
        return Response(status=409, response=str(json_string), content_type='application/json')


@app.route('/usuarios/self', methods=['GET'])
@logado
def buscar_usuario_self():
    usuario = get_usuario_autenticado()
    return buscar_usuario(usuario._id)


@app.route('/usuarios/self', methods=['PUT'])
@logado
def alterar_usuario_self():
    try:
        usuario = get_usuario_autenticado()
        entity_enviada = usuario_assembler.request_to_entity(request)
        entity_enviada._id = usuario._id
        usuario_service.update(entity_enviada)
        return Response(status=204, content_type="application/json")
    except ResourceNotFoundException as e:
        json_string = dumps(e.__dict__, ensure_ascii=False)
        return Response(status=404, response=json_string, content_type="application/json")
    except ResourceConflictException as e:
        json_string = dumps(e.__dict__, ensure_ascii=False)
        return Response(status=409, response=json_string, content_type="application/json")


@app.route('/usuarios/self', methods=['DELETE'])
@logado
def deletar_usuario_self():
    usuario = get_usuario_autenticado()
    return deletar_usuario(usuario._id)


@app.route('/matches', methods=['POST'])
@logado
def salvar_match():
    usuario = get_usuario_autenticado()
    destin = usuario_service.find_by_id(request.json['id'])
    clasificacao = request.json['classificacao']
    threading.Thread(target=salvar_match_async, args=(usuario, destin, clasificacao)).start()
    return Response(status=202)

def salvar_match_async(usuario, destin, classficacao):
    raise ResourceNotFoundException()


@app.route('/oauth/token', methods=['POST'])
def get_access_token():
    try:
        username = request.args.get("username")
        password = request.args.get("password")
        access_token, data_expiracao = oauth2_service.get_access_token(Usuario(email=username, password=password))
        retorno = OAuth2AccessToken(access_token=access_token, data_expiracao=data_expiracao.isoformat()[:-3])
        return Response(status=200, response=str(dumps(retorno.__dict__)), content_type="application/json")
    except UsernameNotFoundException:
        return Response(status=400, content_type="application/json")
    except ResourceNotFoundException:
        return Response(status=400, content_type="application/json")


def buscar_usuario(usuario_id):
    try:
        entity = usuario_service.find_by_id(usuario_id)
        resource = usuario_assembler.to_resource(entity)
        resource.password = None
        resposta = resource.__dict__
        resposta['endereco'] = resposta['endereco'].__dict__
        json_string = dumps(resposta)
        return Response(response=str(json_string), content_type="application/json")
    except ResourceNotFoundException:
        return Response(status=404)


def deletar_usuario(usuario_id):
    usuario_service.delete(usuario_id)
    return Response()


def get_usuario_autenticado():
    authorization = request.headers.get('Authorization')
    return oauth2_service.find_access_token(authorization).usuario

app.run(port=5002)
