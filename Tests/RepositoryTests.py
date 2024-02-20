from Domain.ClientCard import Card
from Domain.Medicine import Medicine
from Domain.Transaction import Transaction
from Repository.RepositoryJson import RepositoryJson
from utils import clear_file


def test_clientcard_repository():
    filename = 'test_clientcard.json'
    clear_file(filename)
    card_repository = RepositoryJson(filename)

    added = Card('1', 'Dan', 'Nume', 1234567890123, 'data', 'data')
    card_repository.create(added)

    assert card_repository.read(added.id_entity) == added

    cards = card_repository.read()

    assert len(cards) == 1

    updated = Card('1', 'Cosmin', 'nume2', 9934567890123, 'data2', 'data3')
    card_repository.update(updated)

    assert card_repository.read(updated.id_entity) == updated

    card_repository.delete(updated.id_entity)

    assert card_repository.read(updated.id_entity) is None
    assert card_repository.read() == []
    assert len(card_repository.read()) == 0


def test_medicine_repository():
    filename = 'test_medicine.json'
    clear_file(filename)
    medicine_repository = RepositoryJson(filename)
    added = Medicine('1', 'ceva', 'altceva', 23.0, 'da')
    medicine_repository.create(added)

    assert medicine_repository.read(added.id_entity) == added

    meds = medicine_repository.read()

    assert len(meds) == 1

    updated = Medicine('1', 'ceva2', 'altecva2', 23.9, 'da')
    medicine_repository.update(updated)

    assert medicine_repository.read(updated.id_entity) == updated

    medicine_repository.delete(updated.id_entity)

    assert medicine_repository.read(updated.id_entity) is None
    assert medicine_repository.read() == []
    assert len(medicine_repository.read()) == 0


def test_transaction_repository():
    filename = 'test_transaction.json'
    clear_file(filename)
    transaction_repository = RepositoryJson(filename)
    added = Transaction('1', '1', '1', 23, 'dara', '12:00')
    transaction_repository.create(added)

    assert transaction_repository.read(added.id_entity) == added

    trans = transaction_repository.read()

    assert len(trans) == 1

    updated = Transaction('1', '2', '2', 2, 'data2', '19:00')
    transaction_repository.update(updated)

    assert transaction_repository.read(updated.id_entity) == updated

    transaction_repository.delete(updated.id_entity)

    assert transaction_repository.read(updated.id_entity) is None
    assert transaction_repository.read() == []
    assert len(transaction_repository.read()) == 0


def test_repository():
    test_medicine_repository()
    test_clientcard_repository()
    test_transaction_repository()
