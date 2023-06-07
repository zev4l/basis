from engine.structures import Card, Suit

from abc import abstractmethod
from random import choice


class Player:
    def __init__(self, name, player_type):
        self.name = name
        self.hand = []
        self.pile = []
        self.type = player_type

    def get_hand(self):
        return self.hand

    def get_name(self):
        return self.name

    def get_pile(self):
        return self.pile

    def add_to_hand(self, card):
        self.hand.append(card)

    def add_to_pile(self, cards):
        self.pile.extend(cards)

    @abstractmethod
    def action(self, world) -> Card:
        """
        This function is meant to be the brains of the player, and should be implemented differently based on the player's nature/strategy
        """
        pass
        # card = self.agent.Action(self,world,isFirst)
        # return self.play(card.rank,  card.suit)

    def play(self, played_card: Card) -> Card:
        for card in self.hand:
            if card.rank == played_card.rank and card.suit == played_card.suit:
                self.hand.remove(card)
                return card
        return False
    
    
    
    ##checks what is the highest card in a list 
    ## trump wins over current suit 
    ## used to find leading card on the table 
    def leading_Card (self , hand : Card,  suit : Suit, trump : Suit  ) -> Card:
        
        high_card =  hand[0]
        
        for c in hand : 
            if (self.compare_cards (high_card , c, suit, trump) == -1):
                high_card = c
        
        return high_card

    ## compares two cards trump wins over current suit 
    ## 1 wins 1st card  -1 wins 2nd card 0  they are equal 
    def compare_cards(self,c1: Card, c2: Card, current_suit: Suit, trump: Suit):
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
        high_card = hand[0]

        top_cards = []

        for card in hand:
            if card.rank > high_card.rank:
                high_card = card

        for card in hand:
            if card.rank == high_card.rank:
                top_cards.append(card)

        return top_cards

    def playable_cards(self, world):
        current_suit = world.current_trick.get_starting_suit()

        world.trump_suit

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
        return sum([card.points for card in self.pile])

    def display_hand(self):
        print(f"{self.name}'s hand:")
        hand = "||"
        for card in self.hand:
            hand = f"{hand} {card.simple_print()} |"
        print(f"{hand}|")

    def __str__(self):
        return self.name


class Human(Player):
    """
    Represents a human player
    """

    def __init__(self, name):
        super().__init__(name, "Human")
        self.input = None

    def register_input_handler(self, input_handler):
        self.input_handler = input_handler

    def action(self, world) -> Card:
        self.input = self.input_handler()

        # Collect user's card-choice
        card = self.hand[self.input]

        # Reset input
        self.input = None

        return card

    def set_input(self, input):
        self.input = input


# AGENTS


class RandomAgent(Player):
    """
    An agent which randomly picks a card from its deck at any given play
    """

    def __init__(self, name):
        super().__init__(name, "RandomAgent")

    def action(self, world) -> Card:
        play_cards = self.playable_cards(world)

        print(self)
        print(play_cards)

        return choice(play_cards)


class SimpleGreedyAgent(Player):
    """
    this Agent will always play the highest valued card possible
    if more than one card have the same rank  it will randomly pick
    """

    def __init__(self, name):
        super().__init__(name, "SimpleGreedyAgent")



    def action(self, world) -> Card:

        print(self)
        print(self.hand)
        
        return choice(self.highest_rank_card(self.hand))


class MinimizePointLossGreedyAgent(Player):
    """
    this Agent will always play the card that wont lose him points
    will also jump at the bit to make points
    Trump over current Suit 
    when in first place to play will play highest card

    """

    def __init__(self, name):
        super().__init__(name, "MinimizePointLossGreedyAgent")

    def action(self, world) -> Card:

        print(self)
        print(self.hand)
        
        table  = world.current_trick.get_cards()
        
        #if first player 
        if (len(table) == 0 ) :
        
            play_cards = self.highest_rank_card(self.hand)            
             
        #if inside player 
        else :
            lead_card = self.leading_Card(table)
            play_cards = self.cards_value_and_play(world,lead_card)


        return self.card_choice(self, play_cards, world)


    def cards_value_and_play (self,  world , lead_card :Card )-> Card : 
        
        high_value =  -1000
        high_card =None
        
        suit = world.current_trick.get_starting_suit()
        trump = world.trump_suit
        
        for c in self.hand :
            is_new_lead = self.compare_cards(c ,  lead_card , suit, trump)
            is_trump =  (c.suit == trump) *100
            
            value =  is_new_lead*( c.points + is_trump)
            if (value  > high_value  ):
                high_value =value
                high_card =c 
        
        return high_card





    def card_choice(self, hand: Card, world) -> Card:
        # check what is the card
        # 1st play  :  play highest card
        # check all cards in table and decide winner and if trump

        # compare winner to our hand (NOT TRUMP)
        # if no card beats it choose lowest weight card non trump
        # if card beats(same suit higher rank,  or trump) it choose highest card

        # compare winner to our hand (TRUMP)
        # if no card beats it choose lowest card non trump
        # if card beats it choose highest beating card

        table = world.current_trick.get_cards()

        suit = world.current_trick.get_starting_suit()
        trump = world.trump_suit

        high_card = Card()

        if table == None:
            return choice(self.highest_card(hand))

        else:
            high_card = table[0]

            for c in table:
                if self.compare_cards(high_card, c, suit, trump) == -1:
                    high_card = c

        good_play = False
        play = high_card

        for card in hand:
            if self.compare_cards(play, card, suit, trump) == -1:
                good_play = True
                play = card

        if good_play == False:
            lowest = hand[0]
            for c in hand:
                if self.compare_cards(lowest, card, suit, trump) == 1:
                    lowest = card
            play = lowest

        return play


class MPLGreedyTrumpSaveAgent(MinimizePointLossGreedyAgent):
    """
    this Agent will always play the card that wont lose him points
    will also jump at the bit to make points , however will only use trumps when necessary
    when in first place to play will play highest card

    """

    def __init__(self, name):
        super().__init__(name, "MPLGreedyTrumpSaveAgent")

    def action(self, world) -> Card:
        play_cards = self.playable_cards(world)
        print(self)
        print(play_cards)

        return self.card_choice(self, play_cards, world)

    def card_choice(self, hand: Card, world) -> Card:
        table = world.current_trick.get_cards()

        suit = world.current_trick.get_starting_suit()
        trump = world.trump_suit

        high_card = Card()

        if table == None:
            return choice(self.highest_card(hand))

        else:
            high_card = table[0]

            for c in table:
                if self.compare_cards(high_card, c, suit, trump) == -1:
                    high_card = c

        good_play = False
        play = high_card

        for card in hand:
            if self.compare_cards(play, card, suit, trump) == -1:
                # Will check if there is a higher card that isnt trump will choose over trumps
                # effectively saving them for when needed
                if good_play:
                    if play.suit != trump and card.suit == trump:
                        play = play
                    else:
                        play = card
                else:
                    good_play = True
                    play = card

        if good_play == False:
            play = hand[0]
            for c in hand:
                if self.compare_cards(play, card, suit, trump) == 1:
                    play = card

        return play
