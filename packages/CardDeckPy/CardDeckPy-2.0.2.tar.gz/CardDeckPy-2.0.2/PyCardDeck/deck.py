from random import shuffle as s
from typing import List
from .card import Card
from .hand import Hand


class Deck:
    def __init__(self, cards: List, shuffled: bool = True):
        self.deck = cards

        if shuffled:
            self.shuffle()
        self.get_deck()

    def deal(self) -> (Hand, Hand):
        player1_cards, player2_cards = Hand([]), Hand([])
        for idx, card in enumerate(self.deck):
            if idx % 2 == 0:
                player1_cards.add_to_hand([card])
            else:
                player2_cards.add_to_hand([card])
        return player1_cards, player2_cards

    def get_deck(self):
        return self.deck

    def shuffle(self):
        s(self.deck)

    def draw(self) -> Card:
        return self.deck.pop(0)

    def __len__(self) -> int:
        return len(self.deck)

    def draw_n_cards(self, amount: int) -> List[Card]:
        drawn_cards = []
        for _ in range(amount):
            drawn_cards.append(self.draw())
        return drawn_cards

    def fill(self):
        word_nums = [
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "jack",
            "queen",
            "king",
            "ace",
        ]
        self.deck.clear()
        for suit in ["Hearts", "Diamonds", "Spades", "Clubs"]:
            for num in range(2, 15):
                self.deck.append(Card(num, word_nums[num - 2], suit))

    def __repr__(self):
        return f"{self.deck}"
