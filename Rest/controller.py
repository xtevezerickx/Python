from flask import Flask, request, Response
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from error_handling import ResourceBussinessException
from model import Usuario
from service import UsuarioService
from repository import UsuarioRepository
from assembler import UsuarioAssembler


usuarioRepository = UsuarioRepository(_collection_name = 'usuario')
usuarioAssembler = UsuarioAssembler()
usuarioService = UsuarioService(repository= usuarioRepository, assembler = usuarioAssembler)

app = Flask(__name__)
api = Api(app)


class GetUsuarioById(Resource):
    def get(self, id):
        entity = usuarioService.findById(id)
        resource = usuarioAssembler.toResource(entity)
        jsonString = dumps(resource.__dict__)
        return Response(response=str(jsonString), content_type="application/json")

class HelloWorld(Resource):

    def tratarResourceBussinessException(self, exception):
        response = jsonify(exception.to_dict())
        response.status_code = exception.status_code
        return response

    def get(self):
        resposta = usuarioRepository.find('Id')
        json_string = dumps([ob.__dict__ for ob in resposta])
        return Response(response=str(json_string), content_type="application/json")

    def post(self):
        nome = request.json['nome']
        idade = request.json['idade']
        try:
            usuario = Usuario(nome=nome)
            usuario.idade = idade
            usuarioRepository.save(usuario)
        except ResourceBussinessException as exception:
            return self.tratarResourceBussinessException(exception)

api.add_resource(HelloWorld, '/hello')
api.add_resource(GetUsuarioById, '/hello/<id>')

if __name__ == '__main__':
    app.run(port=5002)

