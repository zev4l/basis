import DeckOfCards


class Player:   
    
    def __init__(self, name, agent):
        self.name = name
        self.hand = []
        self.agent = agent 
        
    def add_to_hand(self, card):
        self.hand.append(card)


    def Action ( self , world):
        card = self.agent.Action(self,world)
        return self.play(card.rank,  card.suit)
        

    def play(self,rank, suit):
        for card in self.hand:
            if card.rank == rank and card.suit == suit:
                self.hand.remove(card)
                return card
        return False

    def print_hand(self):
        print(f"{self.name}'s hand:")
        for card in self.hand:
            print(f"{self.hand.index(card)}---{card}")

class Players:
    def __init__(self):
        self.players = []
        self.current_player_index = 0

    def add_player(self, player):
        self.players.append(player)

    def get_current_player(self):
        if self.players:
            return self.players[self.current_player_index]
        return None

    def next_player(self):
        if self.players:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def print_players(self):
        if self.players:
            print("Players:")
            for player in self.players:
                print(player.name)
    def size (self):
        return len(self.players)