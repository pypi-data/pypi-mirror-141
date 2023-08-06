class Card:
    def __init__(self, value, name, suit):
        self.val = value
        self.name = name.title()
        self.suit = suit.title()
        self.__create_card()

    def __create_card(self):
        self.card = {"value": self.val, "name": self.name, "suit": self.suit}
        return self.card

    def __repr__(self):
        return f"{self.card}"

    def __str__(self):
        return f"{self.name.title()} of {self.suit.title()}"

    def __int__(self):
        return self.val

    def __gt__(self, otherCard):
        return self.val > otherCard.val

    def __lt__(self, otherCard):
        return self.val < otherCard.val

    def __eq__(self, otherCard):
        return self.val == otherCard.val
