import random
from uuid import uuid4
from dataclasses import dataclass


@dataclass()
class Player:
    id: str
    name: str
    wins: int = 0


    @classmethod
    def create(cls, name: str = None):
        return cls(
            id=str(uuid4()),
            name=name or f'Игрок-{random.randint(1,999)}'
        )
