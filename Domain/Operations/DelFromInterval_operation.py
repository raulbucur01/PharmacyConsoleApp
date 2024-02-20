from typing import List

from Domain.Entity import Entity
from Domain.Operations.UndoRedo_operation import UndoRedoOperation
from Repository.Repository import Repository


class DelFromIntervalOperation(UndoRedoOperation):
    def __init__(self,
                 repository: Repository,
                 deleted_entities: List[Entity]):
        self.repository = repository
        self.deleted_entities = deleted_entities

    def undo(self):
        for entity in self.deleted_entities:
            self.repository.create(entity)

    def redo(self):
        entities = self.repository.read()
        for entity in entities:
            if entity in self.deleted_entities:
                self.repository.delete(entity.id_entity)
