from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from error_handling import ResourceBussinessException
from model import Usuario

app = Flask(__name__)
api = Api(app)

@app.errorhandler(ResourceBussinessException)
def resourceBussinessExceptionHandler(error):
    response = jsonify(erro.to_dict())
    response.status_code = erro.status_code
    return response

class HelloWorld(Resource):
    def get(self):
        return jsonify({"data":"ok"})
    
    def post(self):
        nome = request.json['nome']
        usuario = Usuario('')
        usuario.nome = 'erick'
        print(usuario.idade)
        print(usuario.nome)

api.add_resource(HelloWorld, '/hello')

usuario = Usuario(nome='')

if __name__ == '__main__':
     app.run(port=5002)