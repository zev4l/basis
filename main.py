from engine.game import Game
from engine.players import RandomAgent, SimpleGreedyAgent

player1 = RandomAgent("Player 1")
player2 = SimpleGreedyAgent("Player 2")

game = Game()
game.add_player(player1)
game.add_player(player2)
game.start_match()
while not game.is_over():
    game.next_round()
print("GAME DONE")