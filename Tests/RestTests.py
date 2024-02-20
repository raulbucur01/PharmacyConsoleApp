from Domain.ClientCard import Card
from Domain.ClientCard_validator import ClientCardValidator
from Domain.Medicine import Medicine
from Domain.Medicine_validator import MedicineValidator
from Domain.Transaction import Transaction
from Domain.Transaction_validator import TransactionValidator
from Repository.RepositoryJson import RepositoryJson
from Services.ClientCard_service import CardService
from Services.FullTextSearch_service import FullTextSearchService
from Services.Medicine_service import MedicineService
from Services.RestFunctionalities_service import \
    SortMedDescAfterPiecesBoughtService, \
    SortCardDescAfterTotalDiscountsService, WaterfallDelService
from Services.Transaction_service import TransactionService
from Services.UndoRedo_service import UndoRedoService
from utils import clear_file


def test_SortDescAfterPiecesBought():
    undo_redo_service = UndoRedoService()

    med_rep = RepositoryJson('test_m.json')
    tran_rep = RepositoryJson('test_t.json')

    medicine_validator = MedicineValidator()
    med_service = MedicineService(med_rep, medicine_validator,
                                  undo_redo_service)

    card_rep = RepositoryJson('cards.json')

    tran_validator = TransactionValidator()
    tran_service = TransactionService(tran_rep, tran_validator, med_rep,
                                      card_rep,
                                      undo_redo_service)

    sort_desc_service = SortMedDescAfterPiecesBoughtService(med_rep,
                                                            tran_rep,
                                                            med_service,
                                                            tran_service)

    s = sort_desc_service.sort_desc()
    assert s == [('Triferment', 18), ('Ibuprofen', 2),
                 ('Parasinus', 2), ('Fiobilin', 1), ('Mydocalm', 0)]


def test_SortDescAfterTotalDiscounts():
    undo_redo_service = UndoRedoService()

    med_rep = RepositoryJson('test_m.json')
    card_rep = RepositoryJson('test_c.json')
    tran_rep = RepositoryJson('test_t.json')

    medicine_validator = MedicineValidator()
    med_service = MedicineService(med_rep, medicine_validator,
                                  undo_redo_service)
    card_validator = ClientCardValidator()
    card_service = CardService(card_rep, card_validator,
                               undo_redo_service)
    tran_validator = TransactionValidator()
    tran_service = TransactionService(tran_rep, tran_validator, med_rep,
                                      card_rep,
                                      undo_redo_service)

    sort_desc_service = \
        SortCardDescAfterTotalDiscountsService(med_rep, tran_rep,
                                               card_rep,
                                               med_service, tran_service,
                                               card_service)

    s = sort_desc_service.sort_desc()
    assert s == [('2', 'Georgeta Popescu', 64.035),
                 ('1', 'Raul Bucur', 17.36),
                 ('3', 'Alexandrion Buhnnici', 0)]


def test_increase_price():
    undo_redo_service = UndoRedoService()

    med_rep_before = RepositoryJson('med_rep_before.json')

    med_validator = MedicineValidator()
    med_service_before = MedicineService(med_rep_before, med_validator,
                                         undo_redo_service)

    medsbefore = med_service_before.get_all()
    med_service_before.increase_price(10, 15)
    medsafter = med_service_before.get_all()
    realafter = [Medicine(id_entity='1', name='Ibuprofen', producer='Bayer',
                          price=23.5, needs_prescription='da'),
                 Medicine(id_entity='2', name='Fiobilin',
                          producer='SunPharma',
                          price=13.75, needs_prescription='da'),
                 Medicine(id_entity='3', name='Mydocalm',
                          producer='RichterPharma',
                          price=6.05, needs_prescription='nu'),
                 Medicine(id_entity='4', name='Triferment',
                          producer='BioPharm',
                          price=25.9, needs_prescription='da'),
                 Medicine(id_entity='5', name='Parasinus',
                          producer='DaciaPlant',
                          price=13.97, needs_prescription='nu')]

    clear_file('med_rep_before.json')
    with open('med_rep_backup.json', "r") as myfile:
        data = myfile.read()

    with open('med_rep_before.json', 'w') as myfile:
        myfile.write(data)

    assert medsafter == realafter
    assert medsafter != medsbefore
    assert medsbefore != realafter


def test_delete_from_range():
    undo_redo_service = UndoRedoService()

    tran_rep_before = RepositoryJson('tran_rep_before.json')
    med_rep = RepositoryJson('medicines.json')
    card_rep = RepositoryJson('cards.json')

    tran_validator = TransactionValidator()
    tran_service_before = TransactionService(tran_rep_before, tran_validator,
                                             med_rep, card_rep,
                                             undo_redo_service)

    transbefore = tran_service_before.get_all()
    tran_service_before.delete_from_range(1, 9)
    transafter = tran_service_before.get_all()
    realafter = [Transaction(id_entity='1', id_medicine='4', id_card='2',
                             nr_pieces=2, date='12.12.2021', hour='23:32')]

    clear_file('tran_rep_before.json')
    with open('tran_rep_backup.json', "r") as myfile:
        data = myfile.read()

    with open('tran_rep_before.json', 'w') as myfile:
        myfile.write(data)

    assert transafter == realafter
    assert transafter != transbefore
    assert transbefore != realafter


def test_get_tran_from_range():
    undo_redo_service = UndoRedoService()

    tran_rep = RepositoryJson('test_gettfr.json')
    med_rep = RepositoryJson('medicines.json')
    card_rep = RepositoryJson('cards.json')

    tran_validator = TransactionValidator()
    tran_service = TransactionService(tran_rep, tran_validator, med_rep,
                                      card_rep,
                                      undo_redo_service)
    lst = tran_service.get_tran_from_range(1, 9)
    result = [Transaction(id_entity='2', id_medicine='1', id_card='1',
                          nr_pieces=4, date='9.10.2021', hour='12:44'),
              Transaction(id_entity='3', id_medicine='3', id_card='3',
                          nr_pieces=2, date='1.1.2021', hour='23:59')]

    assert lst == result


def test_full_text_search():
    undo_redo_service = UndoRedoService()

    med_rep = RepositoryJson('test_full_text_med.json')
    card_rep = RepositoryJson('test_full_text_card.json')

    med_v = MedicineValidator()
    medicine_service = MedicineService(med_rep, med_v,
                                       undo_redo_service)
    card_v = ClientCardValidator()
    card_service = CardService(card_rep, card_v,
                               undo_redo_service)

    full_text_service = FullTextSearchService(med_rep,
                                              card_rep,
                                              medicine_service,
                                              card_service)

    text = 'Par'
    meds, cards = full_text_service.full_text_search(text)

    searched_m = [Medicine(id_entity='5', name='Parasinus',
                           producer='DaciaPlant', price=16.14,
                           needs_prescription='nu'),
                  Medicine(id_entity='6', name='Paracetamol',
                           producer='Bayer', price=10.2,
                           needs_prescription='nu')]
    searched_c = [Card(id_entity='4', first_name='Dariusel',
                       last_name='Paraschiv',
                       CNP=9876543210123, birth_date='12.10.2002',
                       register_date='12.12.2020')]

    text2 = 'xyz'
    meds2, cards2 = full_text_service.full_text_search(text2)

    assert meds == searched_m
    assert cards == searched_c
    assert meds2 == []
    assert cards2 == []


def test_delete_corresponding_transactions():
    undo_redo_service = UndoRedoService()

    tran_rep = RepositoryJson('test_waterfall_del.json')
    med_rep = RepositoryJson('medicines.json')
    card_rep = RepositoryJson('cards.json')
    tran_val = TransactionValidator()
    tran_serv = TransactionService(tran_rep, tran_val, med_rep, card_rep,
                                   undo_redo_service)

    waterfall_del_service = WaterfallDelService(tran_rep,
                                                tran_serv,
                                                med_rep,
                                                undo_redo_service)
    transbefore = tran_serv.get_all()
    waterfall_del_service.waterfalldel('2', Medicine('2', 'Da', 'DA',
                                                     12, 'da'))
    transafter = tran_serv.get_all()
    realafter = [Transaction(id_entity='5', id_medicine='5', id_card='5',
                             nr_pieces=2, date='13.01.2021', hour='23:23')]

    clear_file('test_waterfall_del.json')
    with open('waterfall_backup.json', "r") as myfile:
        data = myfile.read()

    with open('test_waterfall_del.json', 'w') as myfile:
        myfile.write(data)

    assert transafter == realafter
    assert transafter != transbefore
    assert transbefore != realafter


def test_undo_redo():
    clear_file('undoredo.json')
    med_rep = RepositoryJson('undoredo.json')
    med_val = MedicineValidator()
    undo_redo_service = UndoRedoService()
    med_service = MedicineService(med_rep, med_val, undo_redo_service)

    med_service.add_medicine('1', 'Parasinus', 'Bayer', 12.2, 'nu')
    assert len(undo_redo_service.undo_list) == 1
    assert len(undo_redo_service.redo_list) == 0
    undo_redo_service.do_undo()
    assert len(undo_redo_service.undo_list) == 0
    assert len(undo_redo_service.redo_list) == 1
    assert len(med_rep.read()) == 0
    undo_redo_service.do_redo()
    assert len(undo_redo_service.undo_list) == 1
    assert len(undo_redo_service.redo_list) == 0
    assert len(med_rep.read()) == 1

    med_service.add_medicine('2', 'da', 'da', 12.2, 'da')
    undo_redo_service.do_undo()
    assert len(med_rep.read()) == 1
    undo_redo_service.do_redo()
    assert len(med_rep.read()) == 2
    undo_redo_service.do_undo()
    undo_redo_service.do_undo()
    assert len(med_rep.read()) == 0
    undo_redo_service.do_redo()
    undo_redo_service.do_redo()
    assert len(med_rep.read()) == 2


def test_rest():
    test_SortDescAfterPiecesBought()
    test_SortDescAfterTotalDiscounts()
    test_increase_price()
    test_delete_from_range()
    test_get_tran_from_range()
    test_delete_corresponding_transactions()
    test_full_text_search()
    test_undo_redo()
