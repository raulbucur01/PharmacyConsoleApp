from Domain.Entity import Entity
from Domain.Operations.UndoRedo_operation import UndoRedoOperation
from Repository.Repository import Repository


class UpdateOperation(UndoRedoOperation):
    def __init__(self,
                 repository: Repository,
                 old_entity: Entity,
                 new_entity: Entity):
        self.repository = repository
        self.old_entity = old_entity
        self.new_entity = new_entity

    def undo(self):
        self.repository.update(self.old_entity)

    def redo(self):
        self.repository.update(self.new_entity)
