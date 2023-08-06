from typing import List
from . import Card
from .errors import DrawFromEmptyHand


class Hand:
    def __init__(self, cards: List[Card]):
        self.hand = cards

    def draw(self) -> Card:
        try:
            return self.hand.pop(0)
        except IndexError:
            pass
        raise DrawFromEmptyHand(f"Cannot draw card from empty hand {self}")

    def add_to_hand(self, cards: List[Card]):
        for card in cards:
            self.hand.append(card)

    def pop(self, idx: int) -> Card:
        return self.hand.pop(idx)

    def __len__(self) -> int:
        return len(self.hand)

    def __repr__(self) -> str:
        return f"{self.hand}"
