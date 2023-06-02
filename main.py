from engine.game import Game
from engine.players import Human, RandomAgent, SimpleGreedAgent

player1 = RandomAgent("Player 1")
player2 = SimpleGreedAgent("Player 2")

game = Game()
game.add_player(player1)
game.add_player(player2)
game.start_match()
while (len(game.deck) > 0 ) :

	game.next_round()

print("GAME DONE")