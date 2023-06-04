from engine.structures import Card, Rank, Suit
from engine.game import Game
from engine.players import RandomAgent, SimpleGreedyAgent

# Test callback
def test_callback(new_player):
    print("Callback called, new player: ", new_player)

player1 = RandomAgent("Player 1")
player2 = SimpleGreedyAgent("Player 2")

game = Game()
game.add_player(player1)
game.add_player(player2)
game.player_pool.register_callback(test_callback)
game.start_match()
while not game.is_over():
	game.next_round()
print("GAME DONE")