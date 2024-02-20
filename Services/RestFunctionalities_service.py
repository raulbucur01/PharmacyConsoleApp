from typing import Tuple, List

from Domain.Medicine import Medicine
from Domain.Operations.WaterfallDel_operation import WaterfallDelOperation
from Repository.Repository import Repository
from Services.ClientCard_service import CardService
from Services.Medicine_service import MedicineService
from Services.Transaction_service import TransactionService
from Services.UndoRedo_service import UndoRedoService
from utils import my_sorted


class SortMedDescAfterPiecesBoughtService:
    """
    Se lucreaza cu: Medicine rep/service si Transaction rep/service
    """
    def __init__(self,
                 med_rep: Repository,
                 tran_rep: Repository,
                 med_service: MedicineService,
                 tran_service: TransactionService):

        self.med_rep = med_rep
        self.tran_rep = tran_rep
        self.med_service = med_service
        self.tran_service = tran_service

    def sort_desc(self) -> List[Tuple]:
        """
        Sorteaza descrescator o lista de tupluri de forma (x,y) cu:
        x -> numele medicamentului
        y -> numarul de bucati cumparate

        :return: Lista de tupluri sortata descrescator
        """
        # ~!Recursive!~
        def inner(meds):
            if not meds:
                return []

            med = meds[0]
            nr_pieces_list = [tran.nr_pieces for tran in trans
                              if med.id_entity == tran.id_medicine]
            total_pieces_bought = sum(nr_pieces_list)
            return [(med.name, total_pieces_bought)] + inner(meds[1:])

        meds = self.med_service.get_all()
        trans = self.tran_service.get_all()
        meds_and_pieces = inner(meds)
        """
        lst = []
        for med in meds:
            nr_pieces = 0
            for tran in trans:
                if med.id_entity == tran.id_medicine:
                    nr_pieces += tran.nr_pieces
            lst.append((med.name, nr_pieces))
        """
        """
        lst = []
        for med in meds:
            nr_pieces_list = [tran.nr_pieces for tran in trans
                              if med.id_entity == tran.id_medicine]
            total_pieces_bought = sum(nr_pieces_list)
            lst.append((med.name, total_pieces_bought))
        """

        return my_sorted(meds_and_pieces, key=lambda x: x[1], reverse=True)


class SortCardDescAfterTotalDiscountsService:
    """
    Se lucreaza cu: Medicine, Card, Transaction cu service/rep
    """
    def __init__(self,
                 med_rep: Repository,
                 tran_rep: Repository,
                 card_rep: Repository,
                 med_service: MedicineService,
                 tran_service: TransactionService,
                 card_service: CardService):

        self.med_rep = med_rep
        self.tran_rep = tran_rep
        self.card_rep = card_rep
        self.med_service = med_service
        self.tran_service = tran_service
        self.card_service = card_service

    def sort_desc(self) -> List[Tuple]:
        """
        Sorteaza descrescator o lista de tupluri de forma (x,y,z)
        Dupa variabila z unde:
        x -> ID-ul cardului
        y -> Numele de pe card
        z -> Totalul reducerilor obtinute

        :return: Lista de tupluri sortata descrescator dupa variabila z
        """

        meds = self.med_service.get_all()
        trans = self.tran_service.get_all()
        cards = self.card_service.get_all()

        lst = []
        for card in cards:
            total_discounts = 0
            for tran in trans:
                if card.id_entity == tran.id_card:
                    nr_pieces = tran.nr_pieces
                    for med in meds:
                        if med.id_entity == tran.id_medicine:
                            price = med.price
                            discount = 0
                            if med.needs_prescription == 'nu':
                                discount = 10
                            elif med.needs_prescription == 'da':
                                discount = 15
                            total = price * nr_pieces
                            total_discounts += (discount/100) * total
            lst.append((card.id_entity, card.first_name + ' ' +
                        card.last_name, total_discounts))

        return my_sorted(lst, key=lambda x: x[2], reverse=True)


class WaterfallDelService:
    def __init__(self,
                 tran_rep: Repository,
                 tran_serv: TransactionService,
                 med_rep: Repository,
                 undo_redo_service: UndoRedoService):

        self.tran_rep = tran_rep
        self.tran_serv = tran_serv
        self.med_rep = med_rep
        self.undo_redo_service = undo_redo_service

    def waterfalldel(self, idmed: str, deleted_med: Medicine):
        trans = self.tran_serv.get_all()

        deleted_transactions = []
        for tran in trans:
            if tran.id_medicine == idmed:
                deleted_transactions.append(self.tran_rep.read(
                    tran.id_entity))
                self.tran_serv.delete_transaction(tran.id_entity)

        self.undo_redo_service.clear_redo()
        waterfalldel_operation = WaterfallDelOperation(self.tran_rep,
                                                       self.med_rep,
                                                       deleted_med,
                                                       deleted_transactions)
        self.undo_redo_service.add_to_undo(waterfalldel_operation)
