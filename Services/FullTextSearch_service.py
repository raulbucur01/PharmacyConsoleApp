from typing import List

from Domain.ClientCard import Card
from Domain.Medicine import Medicine
from Repository.Repository import Repository
from Services.ClientCard_service import CardService
from Services.Medicine_service import MedicineService


class FullTextSearchService:
    """
    Cautare full text
    """

    def __init__(self,
                 medicine_repository: Repository,
                 card_repository: Repository,
                 medicine_service: MedicineService,
                 card_service: CardService):
        self.medicine_repository = medicine_repository
        self.card_repository = card_repository
        self.medicine_service = medicine_service
        self.card_service = card_service

    def full_text_search(self, text: str) -> List[Medicine] and List[Card]:
        """
        Cautare full text
        :param text: textul cautat
        :return: 2 liste continand medicamentele si cardurile care se
                 potrivesc cu textul cautat
        """
        """
        searched_meds = [med for med in meds if (text in med.name) or
                         (text in med.producer) or
                         (text in str(med.price)) or
                         (text in med.needs_prescription)]
        """
        meds = self.medicine_service.get_all()
        searched_meds = list(filter(
            lambda med: (text in med.name) or
                        (text in med.producer) or
                        (text in str(med.price)) or
                        (text in med.needs_prescription), meds))
        """
                for med in meds:
            if (text in med.name) \
                    or (text in med.producer) \
                    or (text in str(med.price)) \
                    or (text in med.needs_prescription):
                searched_meds.append(med)
        """
        """
        searched_cards = [card for card in cards if (text in card.first_name)
                          or (text in card.last_name)
                          or (text in str(card.CNP))
                          or (text in card.birth_date)
                          or (text in card.register_date)]
        """
        cards = self.card_service.get_all()
        searched_cards = list(filter(
            lambda card: (text in card.first_name) or
                         (text in card.last_name) or
                         (text in str(card.CNP)) or
                         (text in card.birth_date) or
                         (text in card.register_date), cards))
        """
                for card in cards:
            if (text in card.first_name) \
                    or (text in card.last_name) \
                    or (text in str(card.CNP)) \
                    or (text in card.birth_date) \
                    or (text in card.register_date):
                searched_cards.append(card)
        """
        return searched_meds, searched_cards
