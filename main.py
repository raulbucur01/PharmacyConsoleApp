"""
Farmacie Online                                                          79max!
~1.1. CRUD medicament: id, nume, producător, preț, necesită rețetă. Prețul să
fie strict pozitiv.

~1.2. CRUD card client: id, nume, prenume,CNP,data nașterii
 (dd.mm.yyyy),
 data înregistrării (dd.mm.yyyy).
 CNP-ul trebuie să fie unic.

~1.3. CRUD tranzacție: id, id_medicament, id_card_client (poate fi nul),
 nr_bucăți, data și ora.
Dacă există un card client, atunci aplicați o reducere de 10%
 dacă medicamentul nu necesită
 rețetă și de 15% dacă necesită.
Se tipărește prețul plătit și reducerile acordate.

~1.4. Căutare medicamente și clienți. Căutare full text.
~1.5. Afișarea tuturor tranzacțiilor dintr-un interval de zile dat.
~1.6. Afișarea medicamentelor ordonate descrescător după numărul de vânzări.
~1.7. Afișarea cardurilor client ordonate descrescător după valoarea
     reducerilor obținute.
~1.8. Ștergerea tuturor tranzacțiilor dintr-un anumit interval de zile.
~1.9. Scumpirea cu un procentaj dat a tuturor medicamentelor cu prețul mai
     mic decât o valoare dată..
"""

from Domain.ClientCard_validator import ClientCardValidator
from Domain.Medicine_validator import MedicineValidator
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
from Tests.DomainTests import test_domain
from Tests.RepositoryTests import test_repository
from Tests.RestTests import test_rest
from Tests.ServiceTests import test_service
from UserInterface.Console import Console


def main():

    undo_redo_service = UndoRedoService()

    medicine_repository = RepositoryJson('medicines.json')
    medicine_validator = MedicineValidator()
    medicine_service = MedicineService(medicine_repository,
                                       medicine_validator,
                                       undo_redo_service)

    card_repository = RepositoryJson('cards.json')
    card_validator = ClientCardValidator()
    card_service = CardService(card_repository, card_validator,
                               undo_redo_service)

    tran_repository = RepositoryJson('transactions.json')
    tran_validator = TransactionValidator()
    tran_service = TransactionService(tran_repository, tran_validator,
                                      medicine_repository, card_repository,
                                      undo_redo_service)

    sort_desc_after_pieces_service = SortMedDescAfterPiecesBoughtService(
        medicine_repository, tran_repository,
        medicine_service, tran_service)

    sort_card_desc_after_total_discounts_service =\
        SortCardDescAfterTotalDiscountsService(medicine_repository,
                                               tran_repository,
                                               card_repository,
                                               medicine_service,
                                               tran_service,
                                               card_service)

    full_text_search_service = FullTextSearchService(medicine_repository,
                                                     card_repository,
                                                     medicine_service,
                                                     card_service)

    waterfall_service = WaterfallDelService(tran_repository,
                                            tran_service,
                                            medicine_repository,
                                            undo_redo_service)

    console = Console(medicine_service, card_service, tran_service,
                      sort_desc_after_pieces_service,
                      sort_card_desc_after_total_discounts_service,
                      full_text_search_service, waterfall_service,
                      undo_redo_service)
    console.run_console()


if __name__ == '__main__':
    test_repository()
    test_rest()
    test_domain()
    test_service()
    main()
