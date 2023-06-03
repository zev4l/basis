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
        
    def play(self, played_card : Card) -> Card:
        for card in self.hand:
            if card.rank == played_card.rank and card.suit == played_card.suit:
                self.hand.remove(card)
                return card
        return False
    
    def playable_cards(self, world):
        current_suit  =  world.current_trick.get_starting_suit()

        if (current_suit):
            trump = world.trump_suit
        
            valid_hand = []

            for card in self.hand:
                if card.suit == current_suit or card.suit == trump:
                    valid_hand.append(card)
        
            if len(valid_hand) > 0:
                return valid_hand

        return self.hand

    def display_hand(self):
        print(f"{self.name}'s hand:")
        hand = '||'
        for card in self.hand: 
            hand =  f'{hand} {card.simple_print()} |'
        print( f'{hand}|')

    def __str__(self):
        return self.name

class Human(Player): 
    """
    Represents a human player
    """
    def __init__(self, name):
        name = input("What's your name?")
        super.__init__(self, name, "Human")

    
    def action(self, world) -> Card: 
        # Show the user the current game-state
        world.print()

        # Show the user his hand
        self.print_hand()

        # Collect user's card-choice, accounting for print_hand's 0-index change
        card_idx = int(input("Choose your card: ")) - 1
        card = self.hand[card_idx]

        print(f'Card played: {card}')

        return card
    
    def print_hand(self):
        output = "\n".join([f"{n + 1} {card}" for n, card in enumerate(self.hand)])
        print(output)

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
        print (play_cards)


        return choice(play_cards)
    
    
class SimpleGreedyAgent(Player):
    """
    this Agent will always play the highest valued card possible
    if more than one card have the same rank  it will randomly pick
    """
    def __init__(self, name):
        super().__init__(name, "SimpleGreedyAgent")
        
    def highest_card(self, hand : Card)->Card:
        
        high_card =  hand[0]

        top_cards = []

        for card in hand : 
            if (card.rank > high_card.rank):
                high_card =card
        
        for card in hand : 
            if (card.rank ==  high_card.rank):
                top_cards.append(card)
        
        return top_cards

    def action(self, world) -> Card:
        
        play_cards = self.playable_cards(world)

        print(self)
        print (play_cards)
        
        return choice(self.highest_card(play_cards) )
    
class MinimizePointLossGreedyAgent(Player):
    """
    this Agent will always play the card that wont lose him points 
    will also jump at the bit to make points 
    when in first place to play will play highest card
    
    """
    def __init__(self, name):
        super().__init__(name, "MinimizePointLossGreedyAgent")
        
    def action(self, world)-> Card:
        
        play_cards = self.playable_cards(world)
        print(self)
        print (play_cards)
        
        
           
        return  choice(play_cards) 
    
    def card_choice(self, hand : Card ,table )-> Card:
        
        #check what is the card  
        #1st play  :  play highest card 
        # check all cards in table and decide winner and if trump 
        
        #compare winner to our hand (NOT TRUMP)
        # if no card beats it choose lowest weight card non trump 
        # if card beats(same suit higher rank,  or trump) it choose highest card 
        
        #compare winner to our hand (TRUMP)
        # if no card beats it choose lowest card non trump
        # if card beats it choose highest beating card 
        
        
        return hand