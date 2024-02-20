from Domain.ClientCard_validator import ClientCardValidationError
from Domain.Medicine import Medicine
from Domain.Medicine_validator import MedicineValidationError
from Domain.Transaction_validator import TransactionValidationError
from Repository.Exceptions import DuplicateIDError, NoSuchIDError, \
    WrongRangeError, DuplicateCNPError
from Services.FullTextSearch_service import FullTextSearchService
from Services.ClientCard_service import CardService
from Services.Medicine_service import MedicineService
from Services.RestFunctionalities_service import \
    SortMedDescAfterPiecesBoughtService, \
    SortCardDescAfterTotalDiscountsService, WaterfallDelService
from Services.Transaction_service import TransactionService
from Services.UndoRedo_service import UndoRedoService


class Console:
    def __init__(self, medicine_service: MedicineService,
                 card_service: CardService,
                 transaction_service: TransactionService,
                 sort_desc_after_pieces_service:
                 SortMedDescAfterPiecesBoughtService,
                 sort_card_after_total_discounts_service:
                 SortCardDescAfterTotalDiscountsService,
                 full_text_search_service: FullTextSearchService,
                 waterfall_del_service: WaterfallDelService,
                 undo_redo_service: UndoRedoService):

        self.medicine_service = medicine_service
        self.card_service = card_service
        self.transaction_service = transaction_service
        self.sort_desc_after_pieces_service = sort_desc_after_pieces_service
        self.sort_card_after_total_discounts_service =\
            sort_card_after_total_discounts_service
        self.full_text_search_service = full_text_search_service
        self.waterfall_del_service = waterfall_del_service
        self.undo_redo_service = undo_redo_service

    def show_menu(self):
        print(' ')
        print('add + med/card/tran -> Add medicament/card client/'
              'tranzactie')
        print('upd + med/card/tran -> Update medicament/card client/'
              'tranzactie')
        print('del + med/card/tran -> Delete medicament/card client/'
              'tranzactie')
        print('sho + med/card/tran -> Show all medicament/card client/'
              'tranzactie')
        print('1. Cautare full text.')
        print('2. Afișeaza totate tranzacțiile dintr-un '
              'interval de zile dat.')
        print('3. Afiseaza medicamentele ordonate descrescător după numărul'
              ' de vânzări. ')
        print('4. Afișeaza cardurile client ordonate descrescător după'
              ' valoarea reducerilor obținute.')
        print('5. Șterge toate tranzacțiile dintr-un anumit'
              ' interval de zile.')
        print('6. Scumpeste cu un procentaj dat toate medicamentele cu prețul'
              ' mai mic decât o valoare dată.')
        print('randmed -> Genereaza n medicamente random.')
        print('--Undo--')
        print('--Redo--')
        print('x -> Iesire')

    def run_console(self):
        while True:
            print(' ')
            self.show_menu()
            opt = str(input('Alege o optiune: '))

            # med
            if opt == 'addmed':
                self.handle_add_medicine()

            elif opt == 'shomed':
                self.handle_show_all_medicines(
                    self.medicine_service.get_all())

            elif opt == 'updmed':
                self.handle_update_medicine()

            elif opt == 'delmed':
                self.handle_delete_medicine()

            # card
            elif opt == 'addcard':
                self.handle_add_card()

            elif opt == 'shocard':
                self.handle_show_all_cards(
                    self.card_service.get_all())

            elif opt == 'updcard':
                self.handle_update_card()

            elif opt == 'delcard':
                self.handle_delete_card()

            # tran
            elif opt == 'addtran':
                self.handle_add_transaction()

            elif opt == 'shotran':
                self.handle_show_all_transactions(
                    self.transaction_service.get_all())

            elif opt == 'updtran':
                self.handle_update_transaction()

            elif opt == 'deltran':
                self.handle_delete_transaction()

            # rest
            elif opt == '1':
                self.handle_full_text_search()

            elif opt == '2':
                self.handle_show_tran_from_range()

            elif opt == '3':
                self.handle_sort_med_after_pieces()

            elif opt == '4':
                self.handle_sort_card_after_total_discounts()

            elif opt == '5':
                self.handle_delete_from_range()

            elif opt == '6':
                self.handle_price_increase()

            elif opt == 'randmed':
                self.handle_generate_random_medicines()

            elif opt == 'undo':
                self.undo_redo_service.do_undo()

            elif opt == 'redo':
                self.undo_redo_service.do_redo()

            elif opt == 'x':
                break

            else:
                print('Optiune invalida, reincearca.')

    # med
    def handle_add_medicine(self):
        try:
            print(' ')
            id_medicine = str(input('Introduceti un ID: '))
            name = str(input('Introduceti numele medicamentului: '))
            producer = str(input('Introduceti numele producatorului: '))
            price = float(input('Introduceti pretul medicamentului: '))
            needs_prescription = str(input('Necesita reteta? '))

            self.medicine_service.add_medicine(id_medicine, name, producer,
                                               price, needs_prescription)
        except MedicineValidationError as ve:
            print('Eroare de validare:', ve)
        except DuplicateIDError as de:
            print('ID duplicat:', de)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_show_all_medicines(self, objects):
        for obj in objects:
            print(obj)

    def handle_update_medicine(self):
        try:
            print(' ')
            id_medicine = str(input('Introduceti ID-ul medicamentului pe care'
                                    ' vreti sa il modificati: '))
            name = str(input('Introduceti noul nume al medicamentului: '))
            producer = str(input('Introduceti noul nume al producatorului: '))
            price = float(input('Introduceti noul pret al medicamentului: '))
            needs_prescription = str(input('Necesita reteta? '))

            self.medicine_service.update_medicine(id_medicine, name, producer,
                                                  price, needs_prescription)
        except MedicineValidationError as ve:
            print('Eroare de validare:', ve)
        except NoSuchIDError as ne:
            print('ID inexistent:', ne)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_medicine(self):
        try:
            print(' ')
            id_medicine = str(input('Introduceti ID-ul medicamentului pe care'
                                    ' vreti sa il stergeti: '))

            deleted_med = None
            meds = self.medicine_service.get_all()
            for med in meds:
                if med.id_entity == id_medicine:
                    deleted_med = med

            self.medicine_service.delete_medicine(id_medicine)
            self.handle_delete_corresponding_transactions(id_medicine,
                                                          deleted_med)
        except MedicineValidationError as ve:
            print('Eroare de validare:', ve)
        except NoSuchIDError as ne:
            print('ID inexistent:', ne)
        except Exception as ex:
            print('Eroare:', ex)

    # card
    def handle_add_card(self):
        try:
            print(' ')
            id_card = str(input('Introduceti un ID: '))
            last_name = str(input('Introduceti numele de familie: '))
            first_name = str(input('Introduceti prenumele: '))
            cnp = int(input('Introduceti CNP-ul: '))
            bd = str(input('Introduceti data nasterii: '))
            rd = str(input('Introduceti data inregistrarii: '))

            self.card_service.add_card(id_card, first_name, last_name, cnp,
                                       bd, rd)
        except ClientCardValidationError as ve:
            print('Eroare de validare:', ve)
        except DuplicateIDError as de:
            print('ID duplicat:', de)
        except DuplicateCNPError as ce:
            print('CNP duplicat:', ce)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_show_all_cards(self, objects):
        for obj in objects:
            print(obj)

    def handle_update_card(self):
        try:
            print(' ')
            id_card = str(input('Introduceti ID-ul cardului pe care vreti'
                                ' sa il modificati: '))
            first_name = str(input('Introduceti noul nume de familie: '))
            last_name = str(input('Introduceti noul prenume: '))
            cnp = int(input('Introduceti noul CNP: '))
            bd = str(input('Introduceti noua data a nasterii: '))
            rd = str(input('Introduceti noua data a inregistrarii: '))

            self.card_service.update_card(id_card, first_name, last_name, cnp,
                                          bd, rd)
        except ClientCardValidationError as ve:
            print('Eroare de validare:', ve)
        except NoSuchIDError as ne:
            print('ID inexistent:', ne)
        except DuplicateCNPError as ce:
            print('CNP duplicat:', ce)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_card(self):
        try:
            print(' ')
            id_card = str(input('Introduceti ID-ul cardului pe care vreti sa'
                                ' il stergeti: '))
            self.card_service.delete_card(id_card)
        except ClientCardValidationError as ve:
            print('Eroare de validare:', ve)
        except NoSuchIDError as ne:
            print('ID inexistent:', ne)
        except Exception as ex:
            print('Eroare:', ex)

    # tran
    def handle_add_transaction(self):
        try:
            print(' ')
            id_tran = str(input('Introduceti ID-ul tranzactiei: '))
            id_med = str(input('Introduceti ID-ul medicamentului: '))
            id_card = str(input('Introduceti ID-ul cardului (0 daca nu se'
                                ' foloseste card): '))
            nr_pieces = int(input('Introduceti nr de bucati cumparate: '))
            date = str(input('Introduceti data tranzactiei: '))
            hour = str(input('Introduceti  ora tranzactiei: '))

            self.transaction_service.add_transaction(id_tran, id_med, id_card,
                                                     nr_pieces, date, hour)
            price, discount = self.transaction_service.apply_discount(
                id_med, id_card, nr_pieces)

            print(' ')
            print('Tranzactie adaugata cu succes!')
            if discount is None:
                print(f'Pretul platit este {price} lei! Nu s-a aplicat nicio'
                      f' reducere.')
            else:
                print(f'Pretul platit este {price} lei! S-a aplicat o'
                      f' reducere de {discount}%')

        except TransactionValidationError as ve:
            print('Eroare de validare:', ve)
        except DuplicateIDError as de:
            print('ID duplicat:', de)
        except NoSuchIDError as ne:
            print('ID inexistent:', ne)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_show_all_transactions(self, objects):
        for obj in objects:
            print(obj)

    def handle_update_transaction(self):
        try:
            print(' ')
            id_tran = str(input('Introduceti ID-ul tranzactiei pe care vreti'
                                ' sa o modificati: '))
            id_med = str(input('Introduceti noul ID al medicamentului: '))
            id_card = str(input('Introduceti noul ID al cardului: '))
            nr_pieces = int(input('Introduceti noul nr de bucati cumparate:'
                                  ' '))
            date = str(input('Introduceti noua data a tranzactiei: '))
            hour = str(input('Introduceti noua ora a tranzactiei: '))

            self.transaction_service.update_transaction(id_tran,
                                                        id_med, id_card,
                                                        nr_pieces, date, hour)

            price, discount = self.transaction_service.apply_discount(
                id_med, id_card, nr_pieces)

            print(' ')
            print('Tranzactie modificata cu succes!')
            if discount is None:
                print(f'Pretul platit este {round(price, 2)} lei! '
                      f'Nu s-a aplicat nicio '
                      f'reducere.')
            else:
                print(f'Pretul platit este {round(price, 2)} lei! '
                      f'S-a aplicat o '
                      f'reducere de {discount}%')

        except TransactionValidationError as ve:
            print('Eroare de validare:', ve)
        except NoSuchIDError as ne:
            print('ID inexistent:', ne)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_transaction(self):
        try:
            print(' ')
            id_tran = str(input('Introduceti ID-ul tranzactiei pe care vreti'
                                ' sa o stergeti: '))
            self.transaction_service.delete_transaction(id_tran)
        except TransactionValidationError as ve:
            print('Eroare de validare:', ve)
        except NoSuchIDError as ne:
            print('ID inexistent:', ne)
        except Exception as ex:
            print('Eroare:', ex)

    # rest
    def handle_sort_med_after_pieces(self):
        try:
            print(' ')
            result_list = self.sort_desc_after_pieces_service.sort_desc()
            for elem in result_list:
                print(f'Nume medicament: {elem[0]}, numar de bucati '
                      f'cumparate: {elem[1]}')
        except Exception as ex:
            print('Eroare:', ex)

    def handle_generate_random_medicines(self):
        try:
            print(' ')
            n = int(input('Cate medicamente vrei sa generezi?: '))
            while n > 0:
                exception = False
                try:
                    id_medicine = self.medicine_service.generate_medicine_id()
                    name = self.medicine_service.generate_name()
                    producer = self.medicine_service.generate_producer()
                    price = self.medicine_service.generate_price()
                    needs_prescription = self.medicine_service.\
                        generate_needs_prescription()

                    self.medicine_service.add_medicine(id_medicine, name,
                                                       producer, price,
                                                       needs_prescription)
                except Exception:
                    exception = True
                finally:
                    if exception is True:
                        pass
                    else:
                        n -= 1

        except Exception as ex:
            print('Eroare:', ex)

    def handle_sort_card_after_total_discounts(self):
        try:
            print(' ')
            result_list = self.\
                sort_card_after_total_discounts_service.sort_desc()
            for elem in result_list:
                print(f'ID card: {elem[0]}, numele de pe card: {elem[1]},'
                      f' valoare reduceri: {round(elem[2], 2)} lei')
        except Exception as ex:
            print('Eroare:', ex)

    def handle_price_increase(self):
        try:
            print(' ')
            percentage = float(input('Alege un procentaj: '))
            value = float(input('Alege o valoare: '))

            self.medicine_service.increase_price(percentage, value)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_from_range(self):
        try:
            print(' ')
            day1 = int(input('Alege capatul stanga al intervalului: '))
            day2 = int(input('Alege capatul dreapta al intervalului: '))

            self.transaction_service.delete_from_range(day1, day2)
        except WrongRangeError as re:
            print('Interval gresit:', re)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_show_tran_from_range(self):
        try:
            print(' ')
            day1 = int(input('Alege capatul stanga al intervalului: '))
            day2 = int(input('Alege capatul dreapta al intervalului: '))

            tran_list = self.transaction_service.get_tran_from_range(
                day1, day2)
            print(' ')
            if not tran_list:
                print(f'Nu exista tranzactii intre zilele {day1} si {day2}.')
            else:
                print(f'Transactiile dintre zilele {day1} si {day2} sunt:')
                for elem in tran_list:
                    print(elem)
        except WrongRangeError as re:
            print('Interval gresit:', re)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_full_text_search(self):
        try:
            print(' ')
            text = str(input('Introduceti textul pt cautarea full text: '))

            meds, cards = self.full_text_search_service.full_text_search(text)
            if (meds == []) and (cards == []):
                print('Nu au fost gasite rezultate pt aceasta cautare.')
            else:
                print('Rezultatele cautarii sunt:')
                for med in meds:
                    print(med)
                for card in cards:
                    print(card)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_corresponding_transactions(self, id_medicine: str,
                                                 deleted_med: Medicine):
        try:
            self.waterfall_del_service.waterfalldel(id_medicine, deleted_med)
        except Exception as ex:
            print('Eroare:', ex)
