from typing import List
from . import Card


class Hand:
    def __init__(self, cards: List[Card]):
        self.hand = cards

    def draw(self) -> Card:
        return self.hand[0]

    def add_to_hand(self, cards: List[Card]):
        for card in cards:
            self.hand.append(card)

    def pop(self, idx: int) -> Card:
        return self.hand.pop(idx)

    def __len__(self) -> int:
        return len(self.hand)

    def __repr__(self) -> str:
        return f"{self.hand}"
