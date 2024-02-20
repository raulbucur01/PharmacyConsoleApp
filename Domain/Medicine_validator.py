from Domain.Medicine import Medicine


class MedicineValidationError(Exception):
    pass


class MedicineValidator:
    def validate(self, medicine: Medicine):
        valid_pres_need = ['da', 'nu']
        if medicine.needs_prescription not in valid_pres_need:
            raise MedicineValidationError(f'Necesitatea retetei poate fi'
                                          f' exprimata doar'
                                          f' prin  {valid_pres_need}')

        if medicine.price < 0:
            raise MedicineValidationError('Pretul medicamentului nu poate'
                                          ' fi negativ')
