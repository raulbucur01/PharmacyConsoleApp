from typing import List

from Domain.Entity import Entity
from Domain.Operations.UndoRedo_operation import UndoRedoOperation
from Repository.Repository import Repository


class WaterfallDelOperation(UndoRedoOperation):
    def __init__(self,
                 repository1: Repository,
                 repository2: Repository,
                 deleted_base_entity: Entity,
                 deleted_entities: List[Entity]):
        self.repository1 = repository1
        self.repository2 = repository2
        self.deleted_base_entity = deleted_base_entity
        self.deleted_entities = deleted_entities

    def undo(self):
        for entity in self.deleted_entities:
            self.repository1.create(entity)

        self.repository2.create(self.deleted_base_entity)

    def redo(self):
        entities = self.repository1.read()
        for entity in entities:
            if entity in self.deleted_entities:
                self.repository1.delete(entity.id_entity)

        entities = self.repository2.read()
        for entity in entities:
            if entity == self.deleted_base_entity:
                self.repository2.delete(entity.id_entity)
