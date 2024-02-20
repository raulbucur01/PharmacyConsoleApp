from Domain.ClientCard import Card
from Domain.Medicine import Medicine
from Domain.Transaction import Transaction


def test_medicine_domain():
    """
    Functie test domain medicament
    """
    med = Medicine('1', 'Aspirina', 'Bayer', 21.99, 'da')

    assert med.id_entity == '1'
    assert med.name == 'Aspirina'
    assert med.producer == 'Bayer'
    assert med.price == 21.99
    assert med.needs_prescription == 'da'


def test_card_domain():
    """
    Functie test domain card client
    """

    card = Card('2', 'Raul', 'Bucur', 1234567891023, '2021', '2021')

    assert card.id_entity == '2'
    assert card.first_name == 'Raul'
    assert card.last_name == 'Bucur'
    assert card.CNP == 1234567891023
    assert card.birth_date == '2021'
    assert card.register_date == '2021'


def test_transaction_domain():
    """
    Functie test domain tranzactie
    """

    tranzactie = Transaction('1', '2', '1', 12, '2021', '12')

    assert tranzactie.id_entity == '1'
    assert tranzactie.id_medicine == '2'
    assert tranzactie.id_card == '1'
    assert tranzactie.nr_pieces == 12
    assert tranzactie.date == '2021'
    assert tranzactie.hour == '12'


def test_domain():
    """
    Inglobeaza functiile test pt domain
    """

    test_medicine_domain()
    test_card_domain()
    test_transaction_domain()
