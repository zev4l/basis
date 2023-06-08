from engine.players import Player
from engine.structures import Pool, Deck, Suit, Card, State
from utils.stats import StatsRecorder
from utils.log import Logger
from time import sleep
import logging

# Constants
MIN_PLAYERS = 2
CARDS_PER_PLAYER = 3
ROUND_DELAY_SECONDS = 1

log = Logger()

class Trick:
    def __init__(self):
        self.plays = []  # List of tuples (player, card)
        self.starting_suit = None
        self.winning_play = None

    def get_cards(self) -> list:
        return [card for _, card in self.plays]

    def get_starting_suit(self) -> Suit:
        return self.starting_suit

    def add_play(self, player: Player, card: Card):
        self.plays.append((player, card))

    def get_winner(self) -> Player:
        return self.winning_play[0]

    def set_starting_suit(self, suit: Suit):
        self.starting_suit = suit

    def set_winning_play(self, play: tuple):
        self.winning_play = play

    def calc_winner(self, trump_suit: Suit):
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
    """
    Houses main game logic, including tricks and winning logic.
    """

    def __init__(self, stats_recorder: StatsRecorder = None, delay: int = ROUND_DELAY_SECONDS, log_level: int = logging.DEBUG):
        global log
        self.state = State.INIT
        self.tricks = []
        self.current_trick = None
        self.deck = Deck()  # The deck is shuffled at instantiation
        self.player_pool = Pool()
        self.next_player: Player
        self.trump_suit: Suit
        self.trump_card: Card
        self.stats_recorder = stats_recorder  # To be incremented mid-game
        self.winner = None
        self.delay = delay
        log.set_level(log_level)

        log.info("New game instantiated")

    def add_player(self, player: Player):
        # Reset player's hand and pile
        player.hand = []
        player.pile = []
        self.player_pool.add_player(player)

    def set_first_player(self, player):
        self.first_player = player

    def start_match(self):
        if len(self.player_pool) < MIN_PLAYERS:
            log.error("Not enough players to start a match")
            raise Exception("Not enough players to start a match")

        if len(self.player_pool) == 3 or len(self.player_pool) == 6:
            self.deck.rectify()
            log.debug(
                f"Rectifying deck as a {len(self.player_pool)}-player situation has been encountered."
            )

        log.info("Starting match")

        # Drawing trump card
        self.trump_card = self.deck.draw_card()
        self.trump_suit = self.trump_card.suit
        log.info(f"Trump card is {self.trump_card}")

        # Deal cards to players
        log.info("Dealing cards to players")
        self.deal_cards(CARDS_PER_PLAYER)

        # Set first player
        self.set_first_player(self.player_pool.get_players()[0])

        # Set state to RUNNING
        self.state = State.RUNNING

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
                    log.debug(f"Dealt trump card {self.trump_card} to {player.name}")
                    self.trump_card = None

    def turn(self) -> Card:
        player = self.player_pool.get_current_player()
        card_played = player.action(self)

        # TODO: Validate played card here (i.e. valid suit, etc.), repeat if card_played is invalid

        # Consuming card from player's hand
        player.play(card_played)

        return player, card_played

    def next_round(self):
        if self.state == State.RUNNING:
            log.info(f"Starting trick number {len(self.tricks) + 1}")

            for player in self.player_pool.get_players():
                log.debug(f"{player.get_name()}'s hand: {player.get_hand()}")

            # Setup new round
            self.current_trick = Trick()

            # Set first player
            self.player_pool.set_current_player(self.first_player)

            # Draw first card, and setting its suit as the round's suit
            # Delay for readability
            sleep(self.delay)

            _, first_card = self.turn()
            self.current_trick.set_starting_suit(first_card.suit)
            self.current_trick.add_play(self.first_player, first_card)
            log.info(f"{self.first_player} played {first_card}")

            # Advance to next player
            self.player_pool.advance_player()

            # Execute turns for all other players
            for _ in range(len(self.player_pool) - 1):                
                # Delay for readability
                sleep(self.delay)

                # Adding current play to trick
                player, card_played = self.turn()
                self.current_trick.add_play(player, card_played)
                log.info(f"{player.name} played {card_played}")

                self.player_pool.advance_player()

            self.tricks.append(self.current_trick)

            # Calculating winner, saving trick and setting next-round first player
            winner, winning_card = self.current_trick.calc_winner(self.trump_suit)
            log.info(f"Round winner is {winner.name} with {winning_card}")

            self.first_player = winner
            winner.add_to_pile(self.current_trick.get_cards())
            log.debug(f"{winner.name}'s pile: {winner.get_pile()}")

            # Record trick turnover
            if self.stats_recorder:
                self.stats_recorder.update_highest_point_turnover(winner, sum([card.points for card in self.current_trick.get_cards()]))

            # Delay for readability
            sleep(self.delay)

            # Topping up player hands
            self.deal_cards(1)

            self.check_game_end()

    def check_game_end(self):        
        # If the deck is empty and players have no more cards
        if len(self.deck) == 0 and all(
            [len(player.hand) == 0 for player in self.player_pool.players]
        ):
            # Asserting game winner
            points_per_player = {}

            for player in self.player_pool.players:
                points_per_player[player] = sum([card.points for card in player.pile])

            # Checking the max score
            max_score = max(points_per_player.values())

            # Checking if there is more than one player with max score
            if list(points_per_player.values()).count(max_score) > 1:
                self.state = State.DRAW

                # In this case, winner is a tuple of the winners
                self.winner = tuple(
                    [
                        player
                        for player, points in points_per_player.items()
                        if points == max(points_per_player.values())
                    ]
                )

                log.info(f"Game ended in a draw between {self.winner}")

            else:
                self.state = State.OVER
                self.winner = max(points_per_player, key=points_per_player.get)
                log.info(
                    f"Game ended. Winner is {self.winner} with {points_per_player[self.winner]} points"
                )

            # Record stats, incrementing wins, losses and draws
            if self.stats_recorder:
                for player in self.player_pool.players:
                    # Record points for this game
                    self.stats_recorder.add_points(player, points_per_player[player])

                    # In case it was a draw
                    if self.state == State.DRAW:
                        # Increment draw for each winner, as self.winner is a tuple
                        if player in self.winner:
                            self.stats_recorder.increment_draws(player)
                        # Increment losses for each player that is not a winner
                        else:
                            self.stats_recorder.increment_losses(player)
                    # In case it was not a draw
                    if self.state == State.OVER:
                        # Increment wins for the winner
                        if player == self.winner:
                            self.stats_recorder.increment_wins(player)
                        # Increment losses for each player that is not the winner
                        else:
                            self.stats_recorder.increment_losses(player)


            # Log a table of points per player
            log.debug("Points per player:")
            for player, points in points_per_player.items():
                log.debug(f"{player.name}: {points}")

    def is_over(self):
        return self.state == State.OVER or self.state == State.DRAW