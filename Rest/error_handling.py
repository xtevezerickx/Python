
# coding: utf-8
from flask import jsonify
class ResourceBussinessException(Exception):
    status_code = 422
    def __init__(self, message = "Unprocessable Entity", payload = None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
        
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv