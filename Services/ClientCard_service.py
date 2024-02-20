from typing import List

from Domain.Operations.Add_operation import AddOperation
from Domain.ClientCard import Card
from Domain.ClientCard_validator import ClientCardValidator
from Domain.Operations.Delete_operation import DeleteOperation
from Domain.Operations.Update_operation import UpdateOperation
from Repository.Exceptions import DuplicateCNPError
from Repository.Repository import Repository
from Services.UndoRedo_service import UndoRedoService


class CardService:
    def __init__(self,
                 card_repository: Repository,
                 card_validator: ClientCardValidator,
                 undo_redo_service: UndoRedoService):

        self.card_repository = card_repository
        self.card_validator = card_validator
        self.undo_redo_service = undo_redo_service

    def add_card(self,
                 id_card: str,
                 first_name: str,
                 last_name: str,
                 CNP: int,
                 birth_date: str,
                 register_date: str):
        """
        Adauga un card in fisier
        :param: parametrii cardului de adaugat
        """
        if self.cnp_unique(CNP) is False:
            raise DuplicateCNPError(f'Exista deja un card client cu CNP-ul'
                                    f' {CNP}')

        card = Card(id_card, first_name, last_name, CNP, birth_date,
                    register_date)
        self.card_validator.validate(card)
        self.card_repository.create(card)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.card_repository, card)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_card(self,
                    id_card: str,
                    first_name: str,
                    last_name: str,
                    CNP: int,
                    birth_date: str,
                    register_date: str):
        """
        Modifica un card din fisier
        :param : parametrii cardului cu care se va inlocui unul existent
                 din fisier
        """
        if self.cnp_unique(CNP) is False:
            raise DuplicateCNPError(f'Exista deja un card client cu CNP-ul'
                                    f' {CNP}')

        old_card = self.card_repository.read(id_card)
        new_card = Card(id_card, first_name, last_name, CNP, birth_date,
                        register_date)
        self.card_validator.validate(new_card)
        self.card_repository.update(new_card)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.card_repository,
                                           old_card,
                                           new_card)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_card(self, id_card: str):
        """
        Sterge un card din fisier
        :param id_card: ID-ul cardului pe care vrem sa il stergem.
        """
        card = self.card_repository.read(id_card)
        self.card_repository.delete(id_card)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.card_repository, card)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self) -> List[Card]:
        """
        Ia toate cardurile din fisier si le pune intr-o lista
        :return: Lista cu toate cardurile din fisier
        """
        return self.card_repository.read()

    def cnp_unique(self, cnp=None) -> True or False:
        """
        Verifica daca CNP-ul este unic
        :param cnp: CNP-ul cardului
        :return: - true daca CNP unic
                 - false daca CNP nu este unic
        """
        cards = self.card_repository.read()

        for elem in cards:
            if elem.CNP == cnp:
                return False
        return True
