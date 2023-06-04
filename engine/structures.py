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
        self.current_player_index = self.players.index(player)

    def advance_player(self):
        if self.players:
            self.current_player_index = (self.current_player_index + 1) % len(
                self.players
            )

    def __str__(self):
        return ", ".join([player.name for player in self.players])

    def __len__(self) -> int:
        return len(self.players)


class Rank(IntEnum):
    """
    A helper enum for card ranks.
    Structure: (rank, points)
    Allows comparing ranks between the real rank, and obtaining points via the points property (e.g. Rank.Ace.points -> 11)
    """

    ACE = (10, 11)
    SEVEN = (9, 10)
    KING = (8, 4)
    JACK = (7, 3)
    QUEEN = (6, 2)
    SIX = (5, 0)
    FIVE = (4, 0)
    FOUR = (3, 0)
    THREE = (2, 0)
    TWO = (1, 0)

    def __new__(cls, value, points):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.points = points
        return obj

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

    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit
        self.points = rank.points

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __repr__(self):
        return f"({self.suit.value}) {self.rank.name}"
    
    def get_filename(self):
        filename = ""
        
        if self.suit == Suit.CLUBS: filename += "clubs"
        elif self.suit == Suit.DIAMONDS: filename += "diamonds"
        elif self.suit == Suit.HEARTS: filename += "hearts"
        elif self.suit == Suit.SPADES: filename += "spades"

        filename += "-"

        if self.rank == Rank.TWO: filename += "2"
        elif self.rank == Rank.THREE: filename += "3"
        elif self.rank == Rank.FOUR: filename += "4"
        elif self.rank == Rank.FIVE: filename += "5"
        elif self.rank == Rank.SIX: filename += "6"
        elif self.rank == Rank.SEVEN: filename += "7"
        elif self.rank == Rank.QUEEN: filename += "Q"
        elif self.rank == Rank.JACK: filename += "J"
        elif self.rank == Rank.KING: filename += "K"
        elif self.rank == Rank.ACE: filename += "A"

        filename += ".png"
        return filename

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


class State(Enum):
    RUNNING = 1
    EXPECTING_INPUT = 2
    OVER = 3
    DRAW = 4
    INIT = 5
