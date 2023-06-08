from abc import abstractmethod
from random import choice
from engine.structures import Card, Suit, Deck
from utils.log import log


class Player:
    """
    Represents a player, either human or agent. Base class for all players.
    """

    def __init__(self, name, player_type):
        self.name = name
        self.hand = []
        self.pile = []
        self.type = player_type

    def get_hand(self):
        """
        Returns the player's hand
        """
        return self.hand

    def get_name(self):
        """
        Returns the player's name
        """
        return self.name

    def get_pile(self):
        """
        Returns the player's pile
        """
        return self.pile

    def add_to_hand(self, card):
        """
        Adds a card to the player's hand
        """
        self.hand.append(card)

    def add_to_pile(self, cards):
        """
        Adds a list of cards to the player's pile
        """
        self.pile.extend(cards)

    @abstractmethod
    def action(self, world) -> Card:
        """
        This function is meant to be the brains of the player, and should be implemented differently based on the player's nature/strategy.
        """

    def play(self, played_card: Card) -> Card:
        """
        Removes a card from the player's hand and returns it.
        """
        for card in self.hand:
            if card.rank == played_card.rank and card.suit == played_card.suit:
                self.hand.remove(card)
                return card
        return False

    def leading_card(self, hand: Card, suit: Suit, trump: Suit) -> Card:
        """
        Returns the highest card in a list of cards.
        A trump card wins over a card of the current suit.
        Used to find the leading card on the table.
        """
        high_card = hand[0]

        for card in hand:
            if self.compare_cards(high_card, card, suit, trump) == -1:
                high_card = card

        return high_card

    def compare_cards(self, c1: Card, c2: Card, current_suit: Suit, trump: Suit):
        """
        Compares two cards and returns 1 if the first card wins, -1 if the second card wins, and 0 if they are equal.
        """
        # In case these are same-suit cards, compare the rank
        if c1.suit == c2.suit:
            return 1 if c1.rank > c2.rank else -1

        # If one of the cards is a trump, it wins
        if c1.suit == trump or c2.suit == trump:
            return 1 if c1.suit == trump else -1

        # If one of the cards is of the current suit, it wins
        if c1.suit == current_suit or c2.suit == current_suit:
            return 1 if c1.suit == current_suit else -1

        # If none of the cards is of the current suit, compare the rank
        return 1 if c1.rank > c2.rank else -1 if c1.rank < c2.rank else 0

    ## returns all cards from highest rank
    def highest_rank_card(self, hand: Card) -> Card:
        """
        Returns the highest card in a list of cards.
        """
        # Getting the card with the highest rank
        high_card = hand[0]

        for card in hand:
            if card.rank > high_card.rank:
                high_card = card

        # Returning all cards with the highest rank
        return [card for card in hand if card.rank == high_card.rank]

    def playable_cards(self, world):
        """
        Out of all the cards in the player's hand, returns the ones that can be played in the current trick.
        """
        current_suit = world.current_trick.get_starting_suit()

        valid_hand = []

        # If the user has a card of the current suit, he must play it
        for card in self.hand:
            if card.suit == current_suit:
                valid_hand.append(card)

        # If the user has no cards of the current suit, he can play any card
        if len(valid_hand) == 0:
            valid_hand = self.hand

        return valid_hand

    def get_points(self):
        """
        Returns the total number of points in the player's pile
        """
        return sum([card.points for card in self.pile])

    def __str__(self):
        return self.name


class Human(Player):
    """
    Represents a human player
    """

    def __init__(self, name):
        super().__init__(name, "Human")
        self.input_handler = None

    def register_input_handler(self, input_handler):
        """
        Registers a function to handle user input
        """
        self.input_handler = input_handler

    def action(self, world) -> Card:
        """
        Retrieves the user's card-choice from the provided input handler
        """
        card_choice = self.input_handler()

        # Collect user's card-choice
        card = self.hand[card_choice]

        return card


# AGENTS


class RandomAgent(Player):
    """
    An agent which randomly picks a card from its deck at any given play
    """

    def __init__(self, name):
        super().__init__(name, "RandomAgent")

    def action(self, world) -> Card:
        play_cards = self.playable_cards(world)
        return choice(play_cards)


class SimpleGreedyAgent(Player):
    """
    An agent which always plays the highest card in its hand.
    Ties are broken at random.
    """

    def __init__(self, name):
        super().__init__(name, "SimpleGreedyAgent")

    def action(self, world) -> Card:
        return choice(self.highest_rank_card(self.hand))


class MinimizePointLossGreedyAgent(Player):
    """
    An agent which always plays the card that will win the round, or its most valuable card otherwise.
    This agent will always play a trump card if it can.
    When in first place to play, it will play the highest card.
    """

    def __init__(self, name):
        super().__init__(name, "MinimizePointLossGreedyAgent")

    def action(self, world) -> Card:
        table = world.current_trick.get_cards()
        suit = world.current_trick.get_starting_suit()

        lead_card = None

        # If first player
        if len(table) == 0:
            # Return the highest card in the hand
            play_cards = self.highest_rank_card(self.hand)

        # Otherwise, if middle or last player
        else:
            # Find the leading card on the table
            lead_card = self.leading_card(table, suit, world.trump_suit)
            # Decide which card to play
            play_cards = [self.decide(world, lead_card)]

        return choice(play_cards)

    def decide(self, world, lead_card: Card) -> Card:
        """
        Computes the value of each card in the hand and returns best card to play.
        Returns a list of cards in case of a tie.
        """

        trump_weight = 5

        # Defining a floor value to find the highest card
        high_value = -1000
        high_card = None

        # Keeping track of the value of each card
        value_cards = []

        # Getting the current suit and trump suit
        suit = world.current_trick.get_starting_suit()

        # For each card in the hand
        for card in self.hand:
            # Check if current card would beat the leading card
            is_new_lead = self.compare_cards(card, lead_card, suit, world.trump_suit)

            # If it would beat the leading card
            trump_bonus = (card.suit == world.trump_suit) * trump_weight

            if is_new_lead == 1:
                value = 10 + card.points * 2 + trump_bonus
            else:
                value = -10 - (card.points * 2 + trump_bonus)

            if value > high_value:
                high_value = value
                high_card = card
            value_cards.append([card, value])

        log.debug(
            f"{self} current hand evaluation {value_cards}, trying to beat {lead_card}"
        )

        return high_card


class MPLGreedyTrumpSaveAgent(Player):
    """
    An agent which always plays the card that wont lose him points.
    This agent will always attempt to make points, though it is very conservative regarding using trump cards.
    When in first place to play, it will play the highest card.
    """

    def __init__(self, name):
        super().__init__(name, "MPLGreedyTrumpSaveAgent")

    def action(self, world) -> Card:
        # Getting the current suit and trump suit
        table = world.current_trick.get_cards()
        suit = world.current_trick.get_starting_suit()

        lead_card = None

        # If we are the first player
        if len(table) == 0:
            play_cards = self.highest_rank_card(self.hand)

        # Otherwise, if middle or last player
        else:
            lead_card = self.leading_card(table, suit, world.trump_suit)
            play_cards = [self.decide(world, lead_card)]

        return choice(play_cards)

    def decide(self, world, lead_card: Card) -> Card:
        """
        Computes the perceived value of each card in the hand and returns best card to play.
        """
        trump_weight = 5

        # Defining a floor value to find the highest card
        high_value = -1000
        high_card = None

        # Keeping track of the value of each card
        value_cards = []

        suit = world.current_trick.get_starting_suit()

        # For each card in the hand
        for card in self.hand:
            # Check if current card would beat the leading card
            is_new_lead = self.compare_cards(card, lead_card, suit, world.trump_suit)
            is_trump = (card.suit == world.trump_suit) * trump_weight

            # If it would beat the leading card
            if is_new_lead == 1:
                value = 15 + card.points - (is_trump * 3)
            else:
                value = -10 - (card.points * 2 + is_trump)

            if value > high_value:
                high_value = value
                high_card = card
            value_cards.append([card, value])

        log.debug(
            f"{self} current hand evaluation {value_cards}, trying to beat {lead_card}"
        )

        return high_card


class MPLGreedyTrumpBasedAgent(Player):
    """
    An agent which always plays the card that wont lose him points, though it will force trump battles.
    When in first place to play, it will play the highest card.
    """

    def __init__(self, name):
        super().__init__(name, "MPLGreedyTrumpBasedAgent")

    def action(self, world) -> Card:
        table = world.current_trick.get_cards()
        suit = world.current_trick.get_starting_suit()

        lead_card = None

        # If we are the first player
        if len(table) == 0:
            play_cards = self.first_play(world)

        # Otherwise, if middle or last player
        else:
            lead_card = self.leading_card(table, suit, world.trump_suit)
            play_cards = [self.decide(world, lead_card)]

        return choice(play_cards)

    def first_play(self, world) -> Card:
        """
        Returns either the the highest trump card, or if there are no trump cards, the highest card in the hand.
        """
        # Obtaining all trumps in hand
        trumps = [card for card in self.hand if card.suit == world.trump_suit]

        # If there are trumps in hand, return the highest one
        if len(trumps) > 0:
            return self.highest_rank_card(trumps)
        else:
            # Otherwise, return the highest card in the hand
            return self.highest_rank_card(self.hand)

    def decide(self, world, lead_card: Card) -> Card:
        """
        Computes the perceived value of each card in the hand and returns best card to play.
        """
        trump_weight = 100

        # Defining a floor value to find the highest card
        high_value = -1000
        high_card = None

        # Keeping track of the perceived value of each card
        value_cards = []

        suit = world.current_trick.get_starting_suit()
        # For each card in the hand
        for card in self.hand:
            # Check if current card would beat the leading card
            is_new_lead = self.compare_cards(card, lead_card, suit, world.trump_suit)
            is_trump = (card.suit == world.trump_suit) * trump_weight

            if is_new_lead == 1:
                value = 15 + card.points + is_trump
            else:
                value = -10 - (card.points * 2 + is_trump)

            if value > high_value:
                high_value = value
                high_card = card

            value_cards.append([card, value])

        log.debug(
            f"{self} current hand evaluation {value_cards}, trying to beat {lead_card}"
        )

        return high_card


class GreedyCountingAgent(Player):
    """
    An agent which will always play the card that won't him points.
    This agent will force trump battles.
    When in first place to play, it will play the highest card.
    """

    def __init__(self, name):
        super().__init__(name, "GreedyCountingAgent")
        self.counting_deck = Deck()
        self.cards_removed = []

    def action(self, world) -> Card:
        table = world.current_trick.get_cards()
        suit = world.current_trick.get_starting_suit()

        lead_card = None

        cards_to_remove = []
        cards_to_remove += table
        cards_to_remove += self.hand

        for player in world.player_pool.get_players():
            cards_to_remove += player.pile

        for card in cards_to_remove:
            if card in self.counting_deck.cards:
                self.counting_deck.cards.remove(card)

        # if first player
        if len(table) == 0:
            play_cards = self.decide_first_play(world)

        elif len(table) > 0 and len(table) < len(world.player_pool):
            lead_card = self.leading_card(table, suit, world.trump_suit)
            play_cards = self.decide_mid_play(world, lead_card)

        # if inside player or last player
        else:
            lead_card = self.leading_card(table, suit, world.trump_suit)
            play_cards = self.last_play(world, lead_card)

        return play_cards

    def decide_first_play(self, world) -> Card:
        """
        TODO: Explain this function
        """
        high_value = -1000
        high_card = None

        value_cards = []

        cards_missing = len(self.counting_deck)
        nplayers = len(world.player_pool)
        cards_player_hands = (nplayers - 1) * len(self.hand)

        for card in self.hand:
            beats = self.count_beating_cards(
                card, self.counting_deck, world.trump_suit, card.suit
            )
            prob_not_being_beat = self.calculate_probability(
                cards_player_hands, cards_missing, beats
            )
            value = prob_not_being_beat * card.points
            if value > high_value:
                high_value = value
                high_card = card
            value_cards.append([card, value])

        log.debug(f"{self} current hand Evaluation {value_cards}")

        return high_card

    def decide_mid_play(self, world, lead_card: Card) -> Card:
        """
        TODO: Explain this function
        """
        trump_weight = 5

        # Defining a floor value to find the highest card
        high_value = -1000
        high_card = None

        # Keeping track of the perceived value of each card
        value_cards = []

        current_suit = world.current_trick.get_starting_suit()

        cards_missing = len(self.counting_deck)
        nplayers = len(world.player_pool)
        cards_player_hands = (nplayers - 1) * len(self.hand)

        # For each card in the hand
        for card in self.hand:
            # Calculate the number of cards in the deck that beat the current card
            beats = self.count_beating_cards(
                card, self.counting_deck, world.trump_suit, current_suit
            )

            # Calculate the probability of the current card not being beaten
            prob_not_being_beat = self.calculate_probability(
                cards_player_hands, cards_missing, beats
            )

            # Check if current card would beat the leading card
            is_new_lead = self.compare_cards(
                card, lead_card, current_suit, world.trump_suit
            )
            is_trump = (card.suit == world.trump_suit) * trump_weight

            if is_new_lead == 1:
                value = prob_not_being_beat * card.points
            else:
                value = -10 - (card.points * 2 + is_trump)
            if value > high_value:
                high_value = value
                high_card = card
            value_cards.append([card, value])

        log.debug(
            f"{self} current hand evaluation {value_cards}, trying to beat {lead_card}"
        )

        return high_card

    def last_play(self, world, lead_card: Card) -> Card:
        """
        TODO: Explain this function
        """
        trump_weight = 5

        # Defining a floor value to find the highest card
        high_value = -1000
        high_card = None

        value_cards = []

        suit = world.current_trick.get_starting_suit()

        for card in self.hand:
            is_new_lead = self.compare_cards(card, lead_card, suit, world.trump_suit)
            is_trump = (card.suit == world.trump_suit) * trump_weight

            if is_new_lead == 1:
                value = 10 + card.points * 2 + is_trump
            else:
                value = -10 - (card.points * 2 + is_trump)

            if value > high_value:
                high_value = value
                high_card = card
            value_cards.append([card, value])

        log.debug(
            f"{self} current hand evaluation {value_cards}, trying to beat {lead_card}"
        )

        return high_card

    def count_beating_cards(self, card: Card, deck: Deck, trump: Suit, suit=None):
        """
        Returns the number of cards in the deck that beat the given card.
        """
        counter = 0

        if suit is None:
            suit = card.suit

        for deck_card in deck.cards:
            if self.compare_cards(deck_card, card, suit, trump) == 1:
                counter += 1

        return counter

    def calculate_probability(self, cards_in_hand, deck_size, cards_that_beat):
        """
        Calculates the probability of a card not being beaten by a card in the deck.
        """
        probability = 1.0

        for i in range(cards_that_beat):
            probability *= (deck_size - cards_in_hand - i) / (deck_size - i)

        return probability
