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

    def highest_card(self, hand: Card) -> Card:
        high_card = hand[0]

        top_cards = []

        for card in hand:
            if card.rank > high_card.rank:
                high_card = card

        for card in hand:
            if card.rank == high_card.rank:
                top_cards.append(card)

        return top_cards

    def action(self, world) -> Card:
        play_cards = self.playable_cards(world)

        print(self)
        print(play_cards)

        return choice(self.highest_card(play_cards))


class MinimizePointLossGreedyAgent(Player):
    """
    this Agent will always play the card that wont lose him points
    will also jump at the bit to make points
    when in first place to play will play highest card

    """

    def __init__(self, name):
        super().__init__(name, "MinimizePointLossGreedyAgent")

    def action(self, world) -> Card:
        play_cards = self.playable_cards(world)
        print(self)
        print(play_cards)

        return self.card_choice(self, play_cards, world)

    def highest_card(self, hand: Card) -> Card:
        high_card = hand[0]

        top_cards = []

        for card in hand:
            if card.rank > high_card.rank:
                high_card = card

        for card in hand:
            if card.rank == high_card.rank:
                top_cards.append(card)

        return top_cards
    
    def compare_cards( c1 :Card, c2:Card, current_suit :Suit, trump :Suit  ) :
        
        if (c1.suit  == c2.suit ):
            if (c1.rank  > c2.rank ):
                return 1
            elif (c2.rank > c1.rank ):
                return -1
            else : 
                return 0
        elif (c1.suit  == trump ): 
            return 1 
        elif (c2.suit ==  trump ): 
            return -1
        elif (c1.suit ==  current_suit ):
            return 1
        elif  (c2.suit  ==  current_suit ) : 
            return -1
                
        else : 
            if (c1.rank > c2.rank ):
                return 1 
            elif (c1.rank < c2.rank ):
                return -1
            else :
                return 0
    
    def card_choice(self, hand: Card , world ) -> Card:
        # check what is the card
        # 1st play  :  play highest card
        # check all cards in table and decide winner and if trump

        # compare winner to our hand (NOT TRUMP)
        # if no card beats it choose lowest weight card non trump
        # if card beats(same suit higher rank,  or trump) it choose highest card

        # compare winner to our hand (TRUMP)
        # if no card beats it choose lowest card non trump
        # if card beats it choose highest beating card

        table =  world.current_trick.get_cards()

        suit = world.current_trick.get_starting_suit()
        trump =  world.trump_suit
        
        high_card =  Card() 


        if (table ==  None ): 
            return choice(self.highest_card(hand))

        else :
            high_card =  table[0]

            for c in table : 
                if (self.compare_cards(high_card, c ,  suit,trump ) == -1 ):
                    high_card =  c

        good_play = False
        play =  high_card

        for card in hand : 
            if (self.compare_cards(play, card , suit,trump ) ==-1 ):         
                good_play =  True
                play = card
        

        if (good_play ==False ):

            lowest  = hand[0]
            for c in hand : 
                if (self.compare_cards(lowest, card ,suit, trump ) == 1):
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

    def card_choice(self, hand:  Card , world ) -> Card:
    
        table =  world.current_trick.get_cards()

        suit = world.current_trick.get_starting_suit()
        trump =  world.trump_suit
        
        high_card =  Card() 


        if (table ==  None ): 
            return choice(self.highest_card(hand))

        else :
            high_card =  table[0]

            for c in table : 
                if (self.compare_cards(high_card, c ,  suit,trump ) == -1 ):
                    high_card =  c

        good_play = False
        play =  high_card

        for card in hand : 
            if (self.compare_cards(play, card , suit,trump ) ==-1 ):         
                #Will check if there is a higher card that isnt trump will choose over trumps 
                #effectively saving them for when needed 
                if (good_play) : 
                    if ( play.suit != trump and card.suit == trump ) : 
                        play  = play 
                    else : 
                        play =  card 
                else : 
                    good_play =  True
                    play = card

        if (good_play == False ):
            play  = hand[0]
            for c in hand : 
                if (self.compare_cards(play, card ,suit, trump ) == 1):
                    play = card 

        return play