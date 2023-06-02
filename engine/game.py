from engine.players import Player
from engine.structures import Pool, Deck, Suit, Rank, Card
from utils.stats import StatsRecorder
from utils.log import Logger
from time import sleep

# Constants
MIN_PLAYERS = 2
CARDS_PER_PLAYER = 3
ROUND_DELAY_SECONDS = 1

log = Logger()

class Trick:
    def __init__(self):
        self.plays = [] # List of tuples (player, card)
        self.starting_suit = None
        self.winning_play = None

    def get_cards(self) -> list:
        return [card for _, card in self.plays]
    


    def get_starting_suit(self) -> Suit:
        return self.starting_suit
    
    def add_play(self, player : Player, card : Card):
        self.plays.append((player, card))
    
    def get_winner(self) -> Player:
        return self.winner
    
    def set_starting_suit(self, suit : Suit):
        self.starting_suit = suit

    def set_winning_play(self, play : tuple):
        self.winning_play = play
    

    def calc_winner(self, trump_suit : Suit):
        """
        Calculates the winner of the trick. The winner is the player who played the highest card of the starting suit, 
        or the player who played the highest trump card.
        This method must only be called when all players have played a card.
        """
        winner, winning_card = self.plays[0]

        for player, card in self.plays:
            # In case of a same-suit play, the highest rank wins
            if card.suit == self.starting_suit and card.rank > winning_card.rank:
                winner, winning_card = player, card
            elif card.suit == trump_suit:
                # In case of a trump play, if the winning play is not a trump play the trump card wins, regardless of rank.
                # if the winning play is a trump play, the highest rank wins.
                if winning_card.suit != trump_suit or card.rank > winning_card.rank:
                    winner, winning_card = player, card

        self.set_winning_play((winner, winning_card))

        return winner, winning_card

class Game:
    def __init__(self, stats_recorder : StatsRecorder = None):
        self.tricks = []
        self.deck = Deck() # The deck is shuffled at instantiation
        self.player_pool = Pool()
        self.next_player : Player
        self.trump_suit : Suit
        self.trump_card : Card
        self.stats_recorder = stats_recorder # To be incremented mid-game

        log.info("New game instantiated")

    def add_player(self, player : Player):
        self.player_pool.add_player(player)

    def set_first_player(self, player):
        self.first_player = player

    def start_match(self): 
        if len(self.player_pool) < MIN_PLAYERS:
            log.error("Not enough players to start a match")
            raise Exception("Not enough players to start a match")
        
        log.info("Starting match")
        
        # Drawing trump card
        self.trump_card  = self.deck.draw_card()
        self.trump_suit = self.trump_card.suit
        log.info(f"Trump card is {self.trump_card}")

        # Deal cards to players
        log.info("Dealing cards to players")
        self.deal_cards(CARDS_PER_PLAYER)
        
        # Set first player
        self.set_first_player(self.player_pool.get_players()[0])

    def deal_cards(self, num_cards):
        for _ in range(num_cards):
            for player in self.player_pool.get_players():
                card = self.deck.draw_card()

                if card:
                    player.add_to_hand(card)
                    log.debug(f"Dealt {card} to {player.name}")
                elif self.trump_card:
                    # TODO: Review this logic
                    player.add_to_hand(self.trump_card)
                    log.debug(f"Dealt trump card {card} to {player.name}")
                    self.trump_card = None
        
    def turn(self, trick  : Trick)-> Card:
        player = self.player_pool.get_current_player()
        card_played = player.action(self, trick)

        # TODO: Validate played card here (i.e. valid suit, etc.), repeat if card_played is invalid

        # Consuming card from player's hand
        player.play(card_played)

        return player, card_played

    def next_round(self):
        log.info(f"Starting trick number {len(self.tricks) + 1}")

        for player in self.player_pool.get_players():
            log.debug(f"{player.get_name()}'s hand: {player.get_hand()}")

        # Setup new round
        trick = Trick()
        
        # Set first player
        self.player_pool.set_current_player(self.first_player) 
        
        # Draw first card, and setting its suit as the round's suit
        _, first_card = self.turn( trick)
        trick.set_starting_suit(first_card.suit)
        trick.add_play(self.first_player, first_card)
        log.info(f"{self.first_player} played {first_card}")
        
        # Advance to next player
        self.player_pool.advance_player()            

        # Execute turns for all other players    
        for _ in range(len(self.player_pool) - 1):
            # Delay for readability
            sleep(ROUND_DELAY_SECONDS)

            # Adding current play to trick
            player, card_played = self.turn(trick)
            trick.add_play(player, card_played)
            log.info(f"{player.name} played {card_played}")
        
            self.player_pool.advance_player()

        self.tricks.append(trick)

        # Calculating winner, saving trick and setting next-round first player
        winner, winning_card = trick.calc_winner(self.trump_suit)
        log.info(f"Round winner is {winner.name} with {winning_card}")

        self.first_player = winner
        winner.add_to_pile(trick.get_cards())
        log.debug(f"{winner.name}'s pile: {winner.get_pile()}")

        # Topping up player hands
        self.deal_cards(1)

        # TODO: Define end-of-game logic/conditions

    def __str__(self):
        print('=====================================================')
        print(f'|| trump_card  {self.trump_card.simple_print() } ')
        print(f'|| deck {len(self.deck)}')
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