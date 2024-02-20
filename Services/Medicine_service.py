import random
from typing import List

from Domain.Operations.Add_operation import AddOperation
from Domain.Operations.Delete_operation import DeleteOperation
from Domain.Medicine import Medicine
from Domain.Medicine_validator import MedicineValidator
from Domain.Operations.PriceIncrease_operation import PriceIncreaseOperation
from Domain.Operations.Update_operation import UpdateOperation

from Repository.Repository import Repository
from Services.UndoRedo_service import UndoRedoService


class MedicineService:
    def __init__(self,
                 medicine_repository: Repository,
                 medicine_validator: MedicineValidator,
                 undo_redo_service: UndoRedoService):

        self.medicine_repository = medicine_repository
        self.medicine_validator = medicine_validator
        self.undo_redo_service = undo_redo_service

    def add_medicine(self,
                     id_medicine: str,
                     name: str,
                     producer: str,
                     price: float,
                     needs_prescription: str):
        """
        Adauga un medicament in fisier
        :param: parametrii medicamentului de adaugat
        """
        medicine = Medicine(id_medicine, name, producer, price,
                            needs_prescription)
        self.medicine_validator.validate(medicine)
        self.medicine_repository.create(medicine)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.medicine_repository, medicine)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_medicine(self,
                        id_medicine: str,
                        name: str,
                        producer: str,
                        price: float,
                        needs_prescription: str):
        """
        Modifica un medicament din fisier
        :param : parametrii medicamentului cu care se va inlocui unul
                 existent din fisier
        """
        old_medicine = self.medicine_repository.read(id_medicine)
        new_medicine = Medicine(id_medicine, name, producer, price,
                                needs_prescription)
        self.medicine_validator.validate(new_medicine)
        self.medicine_repository.update(new_medicine)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.medicine_repository,
                                           old_medicine,
                                           new_medicine)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_medicine(self, id_medicine: str):
        """
        Sterge un medicament din fisier
        :param id_medicine: ID-ul medicamentului pe care vrem sa il stergem.
        """
        medicine = self.medicine_repository.read(id_medicine)
        self.medicine_repository.delete(id_medicine)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.medicine_repository, medicine)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self) -> List[Medicine]:
        """
        Ia toate medicamentele din fisier si le pune intr-o lista
        :return: Lista cu toate medicamentele din fisier
        """
        return self.medicine_repository.read()

    def increase_price(self, percentage: float, value: float) -> None:
        """
        Mareste pretul tuturor medicamentelor din fisier cu procentajul
        percentage daca au pretul mai mic decat valoarea value
        :param percentage: Procentajul cu care se mareste
        :param value: Valoarea maxima la care se aplica marirea
        """
        modified_before = []
        modified_after = []
        meds = self.get_all()
        for med in meds:
            if med.price < value:
                # utilizat la undo redo
                modified_before.append(
                    self.medicine_repository.read(med.id_entity))

                self.update_medicine(med.id_entity, med.name, med.producer,
                                     round(med.price +
                                           (percentage / 100 * med.price), 2),
                                     med.needs_prescription)

                # utilizat la undo redo
                modified_after.append(
                    self.medicine_repository.read(med.id_entity))

        self.undo_redo_service.clear_redo()
        priceincrease_operation = PriceIncreaseOperation(
            self.medicine_repository,
            modified_before,
            modified_after)
        self.undo_redo_service.add_to_undo(priceincrease_operation)

    def generate_medicine_id(self) -> str:
        return str(random.randint(1, 150))

    def generate_name(self) -> str:
        names = ['Propolis', 'Glivenol', 'Brufen', 'Triferment',
                 'Aspacardin']
        return random.choice(names)

    def generate_producer(self) -> str:
        producers = ['Bayer', 'Dacia Plant', 'Arctic', 'OperaMeds',
                     'MendyMeds']
        return random.choice(producers)

    def generate_price(self) -> float:
        return round(random.uniform(5.0, 50.0), 2)

    def generate_needs_prescription(self) -> str:
        valid = ['da', 'nu']
        return random.choice(valid)
