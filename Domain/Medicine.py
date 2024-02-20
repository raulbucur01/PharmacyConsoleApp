from dataclasses import dataclass

from Domain.Entity import Entity


@dataclass
class Medicine(Entity):
    name: str
    producer: str
    price: float
    needs_prescription: str
