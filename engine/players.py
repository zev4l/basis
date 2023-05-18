from engine.structures import Card
from abc import abstractmethod
from random import choice


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.pile = []
        
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
        Player.__init__(self, name)
    
    def action(self, state) -> Card: 
        # Show the user the current game-state
        state.print()

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
        Player.__init__(self, name)

    def action(self, world) -> Card:
        return choice(self.hand)