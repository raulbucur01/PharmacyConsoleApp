from dataclasses import dataclass

from Domain.Entity import Entity


@dataclass
class Transaction(Entity):
    id_medicine: str
    id_card: str
    nr_pieces: int
    date: str
    hour: str
