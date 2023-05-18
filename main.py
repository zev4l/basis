from engine.game import Game
from engine.players import Human, RandomAgent

player1 = RandomAgent("Player 1")
player2 = RandomAgent("Player 2")

game = Game()
game.add_player(player1)
game.add_player(player2)
game.start_match()
game.next_round()