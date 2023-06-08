from engine.structures import Card, Rank, Suit
from engine.game import Game
from engine.players import Human, MPLGreedyTrumpSaveAgent, SimpleGreedyAgent,MinimizePointLossGreedyAgent

# Test callback
def player_change_callback(new_player):
    print("Callback called, new player: ", new_player)

# Test user input

def human_input_handler():
    i = input("Pick a card (1-3): ")
    return int(i) - 1

player1 = MPLGreedyTrumpSaveAgent("Player 1")
player2 = SimpleGreedyAgent("Player 2")
player3 = MinimizePointLossGreedyAgent("Player 3")

game = Game()
game.add_player(player1)
game.add_player(player2)
game.add_player(player3)
game.start_match()
while not game.is_over():
	game.next_round()
print("GAME DONE")