import random

class Card:
    def __init__(self, rank, suit, value, image=''):
        self.rank = rank
        self.suit = suit
        self.value = value
        self.image = image

    def __str__(self):
        return f'{self.rank} of {self.suit} with value {self.value}'

class DeckOfCards:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = []
        suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', 'Jack', 'Queen', 'King']
        values = [11,0,0,0,0,0,10,2,3,4]
        
        for suit in suits:
            for rank in ranks:
                value = values[ranks.index(rank)]
                card = Card(rank, suit, value)
                self.cards.append(card)


    def shuffle(self):
        random.shuffle(self.cards)

    def remove_card(self, rank, suit):
        for card in self.cards:
            if card.rank == rank and card.suit == suit:
                self.cards.remove(card)
                return True
        return False

    def draw_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

    def print_deck(self):
        print("Deck of Cards:")
        for card in self.cards:
            print(card)
            
    def size (self):
        return len(self.cards)



# # Create a deck of cards
# deck = DeckOfCards()
# print ("________________")
# # deck.print_deck()

# # card = deck.draw_card()
# # print ("__card draw is_____________________________ ")

# # deck.remove_card("King","Hearts")

# deck.print_deck()

# print(deck.size())




# # Shuffle the deck
# deck.shuffle()


# card = Card('4','Hearts',0)


# # Remove a specific card from the deck
# #card = '4 of Hearts'
# if deck.remove_card(card):
#     print(f'Removed {card} from the deck.')
# else:
#     print(f'{card} not found in the deck.')


# print ("________________without 4 of hearts")
# deck.print_deck()


# # Draw a card from the deck
# drawn_card = deck.draw_card()
# if drawn_card is not None:
#     print(f'Drawn card: {drawn_card}')
# else:
#     print('No cards left in the deck.')

# print ("________________before reset")
# deck.print_deck()
# # Reset the deck
# deck.reset()
# print ("________________reseted")
# deck.print_deck()