# PyCardDeck

PyCardDeck is a python library for working with card decks, cards and hands in python.

## Create Cards

```python
from PyCarDeck import Card

ace_spades = Card(14, 'Ace', 'Spades')
print(ace_spades)
print(ace_spades.val)
print(ace_spades.name)
print(ace_spades.suit)
# Output: Ace of Spades
# 14
# Ace
# Spades
```

## Create a Deck

```python
from PyCardDeck import Deck

deck = Deck([]) # the deck is currently empty
print(deck) # output []
```

## Create a `Deck` with Cards

```python
from PyCardDeck import Deck, Card

ace_spades = Card(14, 'Ace', 'Spades')
king_spades = Card(13, 'King', 'Spades')
deck = Deck([ace_spades, king_spades])
# Output: [{'value': 13, 'name': 'King', 'suit': 'Spades'}, {'value': 14, 'name': 'Ace', 'suit': 'Spades'}]
```