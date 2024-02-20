from Domain.ClientCard_validator import ClientCardValidator
from Domain.Medicine_validator import MedicineValidator
from Domain.Transaction_validator import TransactionValidator
from Repository.RepositoryJson import RepositoryJson
from Services.ClientCard_service import CardService
from Services.Medicine_service import MedicineService
from Services.Transaction_service import TransactionService
from Services.UndoRedo_service import UndoRedoService
from utils import clear_file


def test_medicine_service():
    """
    Functia de test pentru medicine service
    """
    undo_redo_service = UndoRedoService()
    clear_file('test_med_serv.json')
    medicine_validator = MedicineValidator()
    medicine_repository = RepositoryJson('test_med_serv.json')
    medicine_service = MedicineService(medicine_repository,
                                       medicine_validator,
                                       undo_redo_service)

    medicine_service.add_medicine('1', 'Extraveral', 'Bayer',
                                  12.3, 'da')
    assert len(medicine_service.get_all()) == 1

    medicine_service.update_medicine('1', 'Triferment', 'Bayer',
                                     12.3, 'da')
    assert len(medicine_service.get_all()) == 1
    el = medicine_service.get_all()
    assert el[0].name == 'Triferment'

    medicine_service.delete_medicine('1')
    assert len(medicine_service.get_all()) == 0


def test_card_client_service():
    """
    Functia de test pentru client card service
    """
    undo_redo_service = UndoRedoService()
    clear_file('test_card_serv.json')
    card_validator = ClientCardValidator()
    card_repository = RepositoryJson('test_card_serv.json')
    card_service = CardService(card_repository, card_validator,
                               undo_redo_service)

    card_service.add_card('1', 'Codrin', 'Codrin', 1234523451234,
                          '12.12.2021', '12.12.2021')
    assert len(card_service.get_all()) == 1

    card_service.update_card('1', 'Cocolino', 'Codrin', 1234523451034,
                             '12.12.2021', '12.12.2021')
    assert len(card_service.get_all()) == 1
    el = card_service.get_all()
    assert el[0].first_name == 'Cocolino'

    card_service.delete_card('1')
    assert len(card_service.get_all()) == 0


def test_transaction_service():
    """
    Functia de test pt transaction service
    """
    clear_file('test_tran_serv.json')

    undo_redo_service = UndoRedoService()
    medicine_repository = RepositoryJson('test_m.json')
    card_repository = RepositoryJson('test_c.json')

    transaction_validator = TransactionValidator()
    transaction_repository = RepositoryJson('test_tran_serv.json')
    transaction_service = TransactionService(transaction_repository,
                                             transaction_validator,
                                             medicine_repository,
                                             card_repository,
                                             undo_redo_service)

    transaction_service.add_transaction('1', '1', '1', 3,
                                        '12.12.2021', '23:00')
    assert len(transaction_service.get_all()) == 1

    transaction_service.update_transaction('1', '1', '1', 10,
                                           '12.12.2021', '23:00')
    assert len(transaction_service.get_all()) == 1
    el = transaction_service.get_all()
    assert el[0].nr_pieces == 10

    transaction_service.delete_transaction('1')
    assert len(transaction_service.get_all()) == 0


def test_service():
    test_medicine_service()
    test_card_client_service()
    test_transaction_service()
