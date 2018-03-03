from error_handling import ResourceNotFoundException, ResourceConflictException

class UsuarioService():
    
    def __init__(self, repository, assembler):
        self.repository = repository
        self.assembler = assembler
    
    def save(self, usuario):
        if self.findById(usuario._id) is not None:
            raise ResourceConflictException()
        self.repository.save(usuario)

    def findById(self, id):
        cursor = self.repository.findById(id)
        if(cursor is None):
            raise ResourceNotFoundException()
        entity = self.assembler.cursorToEntity(cursor)
        entity.dataAlteracao = entity.dataAlteracao.isoformat()
        return entity