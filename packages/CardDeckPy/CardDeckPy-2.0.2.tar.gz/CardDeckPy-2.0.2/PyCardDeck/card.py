class Card:
    def __init__(self, value: int, name: str, suit: str):
        self.val = value
        self.name = name.title()
        self.suit = suit.title()
        self.__create_card()

    def __create_card(self):
        self.card = {"value": self.val, "name": self.name, "suit": self.suit}
        return self.card

    def __repr__(self) -> str:
        return f"{self.card}"

    def __str__(self) -> str:
        return f"{self.name.title()} of {self.suit.title()}"

    def __int__(self) -> int:
        return self.val

    def __gt__(self, otherCard) -> bool:
        return self.val > otherCard.val

    def __lt__(self, otherCard) -> bool:
        return self.val < otherCard.val

    def __eq__(self, otherCard) -> bool:
        return self.val == otherCard.val
