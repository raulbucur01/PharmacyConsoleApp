from typing import List

from Domain.Entity import Entity
from Domain.Operations.UndoRedo_operation import UndoRedoOperation
from Repository.Repository import Repository


class PriceIncreaseOperation(UndoRedoOperation):
    def __init__(self,
                 repository: Repository,
                 modified_entities_before: List[Entity],
                 modified_entities_after: List[Entity]):
        self.repository = repository
        self.modified_entities_before = modified_entities_before
        self.modified_entities_after = modified_entities_after

    def undo(self):
        for entity in self.modified_entities_before:
            self.repository.update(entity)

    def redo(self):
        for entity in self.modified_entities_after:
            self.repository.update(entity)
