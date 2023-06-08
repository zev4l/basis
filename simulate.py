from engine.players import RandomAgent, SimpleGreedyAgent, MinimizePointLossGreedyAgent, MPLGreedyTrumpSaveAgent
from engine.game import Game
from utils.stats import StatsRecorder
import logging

player1 = RandomAgent("Player 1")
player2 = SimpleGreedyAgent("Player 2")
player3 = SimpleGreedyAgent("Player 3")
player4 = RandomAgent("Player 4")

stats = StatsRecorder()

GAMES = 10000
ROUND_DELAY_SECONDS = 0

for i in range(GAMES):
    game = Game(stats_recorder=stats, delay=ROUND_DELAY_SECONDS, log_level=logging.ERROR)
    game.add_player(player1)
    game.add_player(player2)
    game.add_player(player3)
    game.add_player(player4)
    game.start_match()

    while not game.is_over():
        game.next_round()

    print(f"Simulated game {i+1}/{GAMES}", end="\r")

print()
stats.print_table()