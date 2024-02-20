from dataclasses import dataclass

from Domain.Entity import Entity


@dataclass
class Card(Entity):
    first_name: str
    last_name: str
    CNP: int
    birth_date: str
    register_date: str
