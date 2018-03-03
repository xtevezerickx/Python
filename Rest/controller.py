import datetime
from flask import Flask, request, Response
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from error_handling import ResourceBussinessException, ResourceNotFoundException, ResourceConflictException
from service import UsuarioService
from repository import UsuarioRepository
from assembler import UsuarioAssembler
from functools import wraps

usuarioRepository = UsuarioRepository(_collection_name = 'usuario')
usuarioAssembler = UsuarioAssembler()
usuarioService = UsuarioService(repository= usuarioRepository, assembler = usuarioAssembler)

app = Flask(__name__)
api = Api(app)

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

@app.route('/usuarios/<id>', methods=['PUT'])
def alterarUsuario(id):
    return Response()

@app.route('/usuarios/<id>', methods=['DELETE'])
def deletarUsuario(id):
    usuarioService.delete(id)
    return Response()

app.run(port=5002)

