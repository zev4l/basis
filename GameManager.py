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
    
    def Action (self,player, world,isFirst)->DeckOfCards.Card: 
        
        world.print()
        
        player.print_hand()
        cardIndex = int(input("choose your card"))
        
        print(cardIndex)
        card  = player.hand[cardIndex]
        print (f'>> played : {card}')
        return card
        


class Table:
    def __init__(self):
       
        self.deck =  DeckOfCards.DeckOfCards()
        self.player_pool =  Players.Players()
        self.first_player = None
        self.table_cards = []
        self.current_suit = ''
        self.trump_card = None
        self.trump= ''

    def print(self):
        print('=====================================================')
        print(f'|| trump_card  {self.trump_card.simple_print() } ')
        print(f'|| deck {self.deck.size()}')
        print(f'||')
        x = '|| table  >'
        for card in self.table_cards: 
            x =  f'{x} {card.simple_print()} | '
        print( x)

        print(f'||')
        print(f'|| rounds suit  => {self.current_suit}')
        
        self.player_pool.print_players(self.first_player)
        print(f'||')
        print('=====================================================')

    def set_first_player(self, player):
        self.first_player = player

    def deal_cards(self, num_cards):
        for _ in range(num_cards):
            for player in self.player_pool.players:
                
                card = self.deck.draw_card()
                if card:
                    player.add_to_hand(card)
                elif self.trump_card:
                    player.add_to_hand(self.trump_card)
                    self.trump_card =None

      



    def start_match(self): 
        self.deck.reset()
        self.deck.shuffle()
        self.deal_cards(3)
        playerList =  self.player_pool.players
        self.set_first_player( playerList[0])
        for player in playerList:
            player.simple_hand()
            print ("___________")
        
        self.trump_card  = self.deck.draw_card()
        self.trump = self.trump_card.suit
        
        self.print()
        self.player_pool.next_player()
        self.print()
        
        
            

    def turn (self,isFirst = False)->DeckOfCards.Card:
        
        card_played = self.player_pool.get_current_player().Action(self,isFirst)
        self.table_cards.append(card_played)
        return card_played

    def round (self):
        self.table_cards =[]
        
        self.player_pool.set_current_player(self.first_player) 
        
        firstCard= self.turn(True)
        self.current_suit=  firstCard.suit
        
        self.player_pool.next_player()                
        for i in range(self.player_pool.size()-1):
            self.turn()
            self.player_pool.next_player()
        
    
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
game.round()

game.print()

    