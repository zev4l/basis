# Import the abstact card class
from pygame_cards.abstract import AbstractCard

from dataclasses import dataclass
from enum import Enum

class CardSuit(Enum):
    HEARTS = 'hearts'
    SPADES = 'spades'
    CLUBS = 'clubs'
    DIAMONDS = 'diamonds'

class CardRank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

@dataclass
class Card(AbstractCard):
    rank: CardRank
    suit: CardSuit

