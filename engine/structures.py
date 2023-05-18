import random
from enum import Enum, IntEnum

class Pool:
    """
    Structure to be used by Game, which represents an aggregation of players
    """    
    def __init__(self):
        self.players = []
        self.current_player_index = 0

    def add_player(self, player):
        self.players.append(player)

    def get_players(self):
        return self.players

    def get_current_player(self):
        if self.players:
            return self.players[self.current_player_index]
        return None

    def set_current_player(self, player):
        self.current_player_index= self.players.index(player)    

    def advance_player(self):
        if self.players:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def __str__(self):
        return ", ".join([player.name for player in self.players])

    def __len__(self) -> int:
        return len(self.players)

class Rank(IntEnum):
    """
    A helper enum for card ranks
    """
    Two = 0
    Three = 0
    Four = 0
    Five = 0
    Six = 0
    Seven = 0
    Queen = 2
    Jack = 3
    King = 4
    Ace = 11

class Suit(Enum):
    """
    A helper enum for card suits
    """
    SPADES = "Spades"
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"

class Card:
    """
    A representation of a card
    """
    def __init__(self, rank : Rank, suit : Suit):
        self.rank = rank
        self.suit = suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    
    def __repr__(self):
        return f'({self.suit.value}) {self.rank.name}'
        
class Deck:
    """
    A representation of a deck
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.cards = []
        
        for suit in Suit:
            for rank in Rank:
                card = Card(rank, suit)
                self.cards.append(card)

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def remove_card(self, rank, suit) -> bool:
        for card in self.cards:
            if card.rank == rank and card.suit == suit:
                self.cards.remove(card)
                return True
        return False

    def draw_card(self) -> Card:
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

    def print_deck(self):
        print("Deck:")
        for card in self.cards:
            print(card)
            
    def __len__(self):
        return len(self.cards)