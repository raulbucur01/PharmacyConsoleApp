from typing import List, Tuple

from Domain.Operations.Add_operation import AddOperation
from Domain.Operations.DelFromInterval_operation import \
    DelFromIntervalOperation
from Domain.Operations.Delete_operation import DeleteOperation
from Domain.Transaction import Transaction
from Domain.Transaction_validator import TransactionValidator
from Domain.Operations.Update_operation import UpdateOperation
from Repository.Exceptions import NoSuchIDError, WrongRangeError
from Repository.Repository import Repository
from Services.UndoRedo_service import UndoRedoService


class TransactionService:
    def __init__(self,
                 transaction_repository: Repository,
                 transaction_validator: TransactionValidator,
                 medicine_repository: Repository,
                 card_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.transaction_repository = transaction_repository
        self.transaction_validator = transaction_validator
        self.medicine_repository = medicine_repository
        self.card_repository = card_repository
        self.undo_redo_service = undo_redo_service

    def add_transaction(self,
                        id_transaction: str,
                        id_medicine: str,
                        id_card: str,
                        nr_pieces: int,
                        date: str,
                        hour: str):

        """
        Adauga o tranzactie in fisier
        :param: parametrii tranzactiei de adaugat
        """
        if self.medicine_repository.read(id_medicine) is None:
            raise NoSuchIDError(f'Nu exista medicament cu ID-ul {id_medicine}'
                                f' Tranzactia nu se poate efectua.')

        if (self.card_repository.read(id_card) is None) and (id_card != '0'):
            raise NoSuchIDError(f'Nu exista card client cu ID-ul {id_card}. '
                                f'Tranzactia nu se poate efectua.')

        transaction = Transaction(id_transaction, id_medicine, id_card,
                                  nr_pieces, date, hour)
        self.transaction_validator.validate(transaction)
        self.transaction_repository.create(transaction)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.transaction_repository, transaction)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_transaction(self,
                           id_transaction: str,
                           id_medicine: str,
                           id_card: str,
                           nr_pieces: int,
                           date: str,
                           hour: str):
        """
        Modifica o tranzactie din fisier
        :param : parametrii tranzactiei cu care se va inlocui una
                 existenta din fisier
        """
        if self.medicine_repository.read(id_medicine) is None:
            raise NoSuchIDError(f'Nu exista medicament cu ID-ul'
                                f' {id_medicine}. '
                                f'Tranzactia nu se poate efectua.')

        if (self.card_repository.read(id_card) is None) and (id_card != '0'):
            raise NoSuchIDError(f'Nu exista card client cu ID-ul {id_card}. '
                                f'Tranzactia nu se poate efectua.')

        old_transaction = self.transaction_repository.read(id_transaction)
        new_transaction = Transaction(id_transaction, id_medicine, id_card,
                                      nr_pieces, date, hour)
        self.transaction_validator.validate(new_transaction)
        self.transaction_repository.update(new_transaction)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.transaction_repository,
                                           old_transaction,
                                           new_transaction)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_transaction(self, id_transaction: str):
        """
        Sterge o tranzactie din fisier
        :param id_transaction: ID-ul tranzactiei pe care vrem sa o stergem.
        """
        transaction = self.transaction_repository.read(id_transaction)
        self.transaction_repository.delete(id_transaction)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.transaction_repository,
                                           transaction)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self) -> List[Transaction]:
        """
        Ia toate tranzactiile din fisier si le pune intr-o lista
        :return: Lista cu toate medicamentele din fisier
        """
        return self.transaction_repository.read()

    def apply_discount(self, idMedicine: str, idCard: str, nr_pieces: int) \
            -> Tuple:
        """
        Dacă există un card client, atunci aplicați o reducere de 10%
        dacă medicamentul nu necesită
        rețetă și de 15% dacă necesită.
        :return: Tuplu: (pretul platit, reducerea acordata)
        """

        med = self.medicine_repository.read(idMedicine)

        discount = None
        if idCard == '0':
            total = med.price * nr_pieces
            return total, discount
        else:
            if med.needs_prescription == 'nu':
                discount = 10
            elif med.needs_prescription == 'da':
                discount = 15

        total = med.price * nr_pieces

        return round(total - ((discount / 100) * total), 2), discount

    def delete_from_range(self, day1: int, day2: int) -> None:
        """
        Șterge toate tranzacțiile dintr-un anumit interval de zile.
        :param day1: Ziua din capatul stanga al intervalului
        :param day2: Ziua din capatul dreapta al intervalului
        """
        if day1 > day2:
            raise WrongRangeError(f'Capatul stanga al intervalului ({day1})'
                                  f' este mai mare'
                                  f' decat capatul dreapta ({day2}).')
        if (day1 not in range(1, 32)) or (day2 not in range(1, 32)):
            raise WrongRangeError(f'Zilele trebuie sa fie intre 1 si 31.')

        deleted_transactions = []
        trans = self.get_all()
        if day1 == day2:
            for tran in trans:
                if int(self.get_day(tran.date)) == day1:
                    deleted_transactions.append(tran)
                    self.delete_transaction(tran.id_entity)
        else:
            for tran in trans:
                if int(self.get_day(tran.date)) in range(day1, day2 + 1):
                    deleted_transactions.append(tran)
                    self.delete_transaction(tran.id_entity)

        self.undo_redo_service.clear_redo()
        delfrominterval_operation = DelFromIntervalOperation(
            self.transaction_repository,
            deleted_transactions)
        self.undo_redo_service.add_to_undo(delfrominterval_operation)

    def get_day(self, date: str):
        """
        Ia ziua dintr-o data calendaristica
        :param date: Data calendaristica
        :return: Ziua din data calendaristica data
        """
        str_split = date.split('.')
        return str_split[0]

    def get_tran_from_range(self, day1: int, day2: int) -> List[Transaction]:
        """
        Ia tranzactiile din un interval de zile intr-o lista
        :param day1: Ziua din capatul stanga al intervalului
        :param day2: Ziua din capatul dreapta al intervalului
        :return: Lista de tranzactii din intervalul [day1, day2]
        """
        if day1 > day2:
            raise WrongRangeError(f'Capatul stanga al intervalului ({day1})'
                                  f' este mai mare'
                                  f' decat capatul dreapta ({day2}).')
        if (day1 not in range(1, 32)) or (day2 not in range(1, 32)):
            raise WrongRangeError(f'Zilele trebuie sa fie intre 1 si 31.')

        trans = self.get_all()
        if day1 == day2:
            result_list = [tran for tran in trans
                           if int(self.get_day(tran.date)) == day1]
            """
                for tran in trans:
                    if int(self.get_day(tran.date)) == day1:
                        result_list.append(tran)
            """
        else:
            result_list = [tran for tran in trans
                           if int(self.get_day(tran.date))
                           in range(day1, day2 + 1)]
            """
                for tran in trans:
                    if int(self.get_day(tran.date)) in range(day1, day2 + 1):
                        result_list.append(tran)
            """

        return result_list
