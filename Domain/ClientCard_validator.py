from Domain.ClientCard import Card


class ClientCardValidationError(Exception):
    pass


class ClientCardValidator:
    def validate(self, card: Card):
        if len(str(card.CNP)) != 13:
            raise ClientCardValidationError('CNP-ul trebuie sa aiba '
                                            '13 cifre.')

        if self.valid_date(card.birth_date) is False:
            raise ClientCardValidationError(f'Data introdusa '
                                            f'({card.birth_date}) '
                                            f'nu este de forma DD.MM.YYYY sau'
                                            f' nu are sens.')

        if self.valid_date(card.register_date) is False:
            raise ClientCardValidationError(f'Data introdusa '
                                            f'({card.register_date}) '
                                            f'nu este de forma DD.MM.YYYY sau'
                                            f' nu are sens.')

    def valid_date(self, date: str) -> True or False:
        if '.' not in date:
            return False

        if self.contains_letters(date):
            return False

        date_split = date.split('.')
        day = date_split[0]
        month = date_split[1]
        year = date_split[2]

        if int(day) not in range(1, 32):
            return False

        if int(month) not in range(1, 13):
            return False

        if len(year) != 4:
            return False

        return True

    def contains_letters(self, string):
        string_lowercase = string.lower()
        return string_lowercase.islower()
