from engine.structures import Card, Rank, Suit
from engine.game import Game
from engine.players import Human, RandomAgent, SimpleGreedyAgent

# Test callback
def player_change_callback(new_player):
    print("Callback called, new player: ", new_player)

# Test user input

def human_input_handler():
    i = input("Pick a card (1-3): ")
    return int(i) - 1

player1 = RandomAgent("Player 1")
player2 = SimpleGreedyAgent("Player 2")
player3 = Human("Player 3")
player3.register_input_handler(human_input_handler)

game = Game()
game.add_player(player1)
game.add_player(player2)
game.add_player(player3)
game.player_pool.register_callback(player_change_callback)
game.start_match()
while not game.is_over():
	game.next_round()
print("GAME DONE")