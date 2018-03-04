import datetime
from flask import Flask, request, Response
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from error_handling import ResourceBussinessException, ResourceNotFoundException, ResourceConflictException, UsernameNotFoundException
from service import UsuarioService, OAuth2Service
from repository import UsuarioRepository, OAuth2AcessTokenRepository
from assembler import UsuarioAssembler, OAuth2AccessTokenAssembler
from functools import wraps
from model import Usuario
from canonico import OAuth2AccessToken

usuarioRepository = UsuarioRepository(_collection_name = 'usuario')
usuarioAssembler = UsuarioAssembler()
usuarioService = UsuarioService(repository= usuarioRepository, assembler = usuarioAssembler)

oauth2Repository = OAuth2AcessTokenRepository(_collection_name='oAuth2AccessToken')
oauth2Assembler = OAuth2AccessTokenAssembler()
oauth2Service = OAuth2Service(repository=oauth2Repository, usuarioService=usuarioService, oAuth2Assembler=oauth2Assembler)

app = Flask(__name__)
api = Api(app)

def logado(func):
    @wraps(func)
    def inner( *args, **kwargs):
        authorization = request.headers.get('Authorization')
        if  authorization is None:
            return Response(status=401)
        else:
            try:
                token = oauth2Service.findAccessToken(authorization)
                if token is None or datetime.datetime.now() >= token.dataExpiracao:
                    return Response(status=401)
            except ResourceNotFoundException:
                return Response(status=401)
            return func(*args,**kwargs)
    return inner

def tratarResourceBussinessException(exception):
    response = jsonify(exception.to_dict())
    response.status_code = exception.status_code
    return response

@app.route('/usuarios', methods=['POST'])
def salvarUsuario():
    try:
        entity = usuarioAssembler.requestToEntity(request)
        entity.dataAlteracao = datetime.datetime.now()
        usuarioService.save(entity)
        return Response(status=201, content_type="application/json")
    except ResourceBussinessException as exception:
        return tratarResourceBussinessException(exception)
    except ResourceConflictException:
        return Response(status=409)

@app.route('/usuarios/<id>', methods=['GET'])
def buscarUsuario(id):
    try:
        entity = usuarioService.findById(id)
        resource = usuarioAssembler.toResource(entity)
        jsonString = dumps(resource.__dict__)
        return Response(response=str(jsonString), content_type="application/json")
    except ResourceNotFoundException:
        return Response(status=404)

@app.route('/usuarios/self', methods=['GET'])
@logado
def buscarUsuarioSelf():
    authorization = request.headers.get('Authorization')
    usuario = oauth2Service.findAccessToken(authorization).usuario
    return buscarUsuario(usuario._id)


@app.route('/usuarios/<id>', methods=['PUT'])
def alterarUsuario(id):
    return Response()

@app.route('/usuarios/<id>', methods=['DELETE'])
def deletarUsuario(id):
    usuarioService.delete(id)
    return Response()

@app.route('/oauth/token', methods=['POST'])
def getAccessToken():
    try:
        username = request.args.get("username")
        password = request.args.get("password")
        usuario = Usuario(_id=username, password = password)
        accessToken = oauth2Service.getAccessToken(usuario)
        retorno = OAuth2AccessToken(accessToken=accessToken)
        jsonString = dumps(retorno.__dict__)
        return Response(status=200, response=str(jsonString), content_type="application/json")
    except UsernameNotFoundException:
        return Response(status=400)
    except ResourceNotFoundException:
        return Response(status=400)

app.run(port=5002)

