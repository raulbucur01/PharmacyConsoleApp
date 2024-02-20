from Domain.Entity import Entity
from Domain.Operations.UndoRedo_operation import UndoRedoOperation
from Repository.Repository import Repository


class AddOperation(UndoRedoOperation):
    def __init__(self,
                 repository: Repository,
                 added_entity: Entity):
        self.repository = repository
        self.added_entity = added_entity

    def undo(self):
        self.repository.delete(self.added_entity.id_entity)

    def redo(self):
        self.repository.create(self.added_entity)
