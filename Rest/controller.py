from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from error_handling import ResourceBussinessException
from model import Usuario
from repository import UsuarioRepository

app = Flask(__name__)
api = Api(app)

usuarioRepository = UsuarioRepository()

class HelloWorld(Resource):

    def tratarResourceBussinessException(self, exception):
        response = jsonify(exception.to_dict())
        response.status_code = exception.status_code
        return response

    def get(self):
        usuairo = Usuario(nome="erick", idade=21)
        usuarioRepository.save(usuario)
        return jsonify({"data":"ok"})

    def post(self):
        nome = request.json['nome']
        try:
            usuario = Usuario(nome=None)
        except ResourceBussinessException as exception:
            return self.tratarResourceBussinessException(exception)

api.add_resource(HelloWorld, '/hello')

if __name__ == '__main__':
    app.run(port=5002)

