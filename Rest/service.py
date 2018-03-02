from repository import UsuarioRepository
from assembler import UsuarioAssembler

class UsuarioService():
    
    def __init__(self, repository, assembler):
        self.repository = repository
        self.assembler = assembler
    
    def save(self, usuario):
        self.repository.save()
    
    def findById(self, id):
        cursor = self.repository.findById(id)
        print(cursor)
        entity = self.assembler.cursorToEntity(cursor)
        entity.dataAlteracao = entity.dataAlteracao.isoformat()
        return entity
