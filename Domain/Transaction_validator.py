from Domain.Transaction import Transaction


class TransactionValidationError(Exception):
    pass


class TransactionValidator:
    def validate(self, transaction: Transaction):
        if transaction.nr_pieces <= 0:
            raise TransactionValidationError('Numarul de bucati cumparate'
                                             ' nu poate fi <= 0')

        if self.valid_date(transaction.date) is False:
            raise TransactionValidationError(f'Data introdusa'
                                             f' ({transaction.date}) '
                                             f'nu este de forma DD.MM.YYYY '
                                             f'sau'
                                             f' nu are sens.')
        if self.valid_hour(transaction.hour) is False:
            raise TransactionValidationError(f'Ora introdusa'
                                             f' ({transaction.hour}) nu este'
                                             f' de forma h:min '
                                             'sau nu are sens.')

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

    def contains_letters(self, string: str) -> True or False:
        string_lowercase = string.lower()
        return string_lowercase.islower()

    def valid_hour(self, hour: str) -> True or False:
        if ':' not in hour:
            return False

        if self.contains_letters(hour):
            return False

        hour_split = hour.split(':')
        h = hour_split[0]
        m = hour_split[1]

        if int(h) not in range(0, 25):
            return False

        if int(m) not in range(0, 61):
            return False

        return True
