# Import the abstact card class
from pygame_cards.abstract import AbstractCard

from dataclasses import dataclass
from enum import Enum

import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from engine.structures import Card

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
class UICard(AbstractCard):
    rank: CardRank
    suit: CardSuit
    filename: str

