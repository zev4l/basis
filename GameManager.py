import DeckOfCards
import Players

# initiate DeckOfCards & game manager
# set up Player Number  default  2,3 ,4
# Set up each player  
#     PLAYER Type
#     if agent 
#         what are player rules 
#     add player pool 
# set player pool

class humanAgent: 
    def __init__(self):
        pass
    
    def Action (self,player, world): 
        player.print_hand()
        cardIndex = input("choose your card")
        
        print(cardIndex)
        return cardIndex
        


class Table:
    def __init__(self):
       
        self.deck =  DeckOfCards.DeckOfCards()
        self.player_pool =  Players.Players()
        self.first_player = None
        self.table_cards = []



    def set_first_player(self, player):
        self.first_player = player

    def deal_cards(self, num_cards):
        for _ in range(num_cards):
            for player in self.player_pool.players:
                
                card = self.deck.draw_card()
                if card:
                    player.add_to_hand(card)

      



    def start_match(self): 
        self.deck.reset()
        self.deck.shuffle()
        self.deal_cards(3)
        playerList =  self.player_pool.players
        for player in playerList:
            player.print_hand()
            print ("___________")
        
        
    
    def setup(self):
        nPlayers = input("How many Players: 2,3 or 4  " )
        try:
                nPlayers = int(nPlayers)
        except ValueError:
            print("Invalid input. Enter a number.")        
        for i in range(nPlayers): 
            type =input("What is the player type 0- human 1-bot") 
            
            type =  'human'
            
            if (type == 'human'):
                self.player_pool.add_player(Players.Player(f'player{i}', humanAgent()))
        
                
            


game =  Table()
game.setup()
game.start_match()
    