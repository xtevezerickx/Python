class ResourceBussinessException(Exception):
    status_code = 422
    def __init__(self, message = "Unprocessable Entity", payload = None):
        super(ResourceBussinessException, self).__init__(message)
        self.message = message
        self.payload = payload
        
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class ResourceConflictException(Exception):
    def __init__(self, message = "Conflict"):
        super(ResourceConflictException, self).__init__(message)

class ResourceNotFoundException(Exception):
    def __init__(self, message = "Conflict"):
        super(ResourceNotFoundException, self).__init__(message)
