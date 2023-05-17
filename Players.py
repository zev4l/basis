import DeckOfCards


class Player:   
    
    def __init__(self, name, agent):
        self.name = name
        self.hand = []
        self.agent = agent 
        self.pile  = []
        
    def __str__(self):
        return  self.name
        
    def add_to_hand(self, card):
        self.hand.append(card)

    def Action ( self , world,isFirst)->DeckOfCards.Card:
        card = self.agent.Action(self,world,isFirst)
        return self.play(card.rank,  card.suit)
        

    def play(self,rank, suit)->DeckOfCards.Card:
        for card in self.hand:
            if card.rank == rank and card.suit == suit:
                self.hand.remove(card)
                return card
        return False

    def print_hand(self):
        print(f"{self.name}'s hand:")
        for card in self.hand:
            print(f"{self.hand.index(card)}---{card}")
            
    def simple_hand(self):
        print(f"{self.name}'s hand:")
        hand = '||'
        for card in self.hand: 
            hand =  f'{hand} {card.simple_print()} |'
        print( f'{hand}|')
    
class Players:
    def __init__(self):
        self.players = []
        self.current_player_index = 0

    def add_player(self, player):
        self.players.append(player)

    def get_current_player(self)->Player:
        if self.players:
            return self.players[self.current_player_index]
        return None

    def set_current_player(self,player):
        self.current_player_index= self.players.index(player)
        
        
    
    def next_player(self):
        if self.players:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def print_players(self):
        if self.players:
            print("Players:")
            for player in self.players:
                print(player.name)
                
    def print_players (self, firstPlayer):
        c_player_index = self.current_player_index
        
        index  = self.players.index(firstPlayer)
        
        output =  '|| 1st  '
        for i in range(len(self.players)):
            output =  f'{output}{self.players[(index+i)%len(self.players)]} '
            if (c_player_index == (index+i)%len(self.players)):
                output = f'{output}< current'
            output =f'{output}|X|X| '
            
        print (output)
        
        
        
        
        
    def size (self)->int:
        return len(self.players)