import random
from enum import Enum, IntEnum


class Pool:
    """
    Structure to be used by Game, which represents an aggregation of players.
    The implementation of this class allows a third party to register on-player-change callbacks.
    """

    def __init__(self):
        self.players = []
        self.current_player_index = 0
        self.callbacks = []

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
        self._notify_observers()

    def advance_player(self):
        self.set_current_player(
            self.players[(self.current_player_index + 1) % len(self.players)]
        )

    def _notify_observers(self):
        for callback in self.callbacks:
            callback(self.get_current_player())

    def register_callback(self, callback):
        self.callbacks.append(callback)

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
        return f"{self.rank.name} ({self.suit.value})"

    def get_filename(self):
        suit_names = {
            Suit.CLUBS: "clubs",
            Suit.DIAMONDS: "diamonds",
            Suit.HEARTS: "hearts",
            Suit.SPADES: "spades"
        }

        rank_names = {
            Rank.TWO: "2",
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.QUEEN: "Q",
            Rank.JACK: "J",
            Rank.KING: "K",
            Rank.ACE: "A"
        }

        filename = suit_names[self.suit] + "-" + rank_names[self.rank] + ".png"
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

    def rectify(self):
        """
        This method will adapt the deck to a situation of 3-player or 6-player game.
        According to Bisca rules, in a 3-player game, the 2s are removed from the deck.
        """
        self.cards = [card for card in self.cards if card.rank != Rank.TWO]

    def __len__(self):
        return len(self.cards)


class State(Enum):
    RUNNING = 1
    EXPECTING_INPUT = 2
    OVER = 3
    DRAW = 4
    INIT = 5
