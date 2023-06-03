from engine.game import Game
from engine.players import Player, Human, RandomAgent, SimpleGreedyAgent
from UI.game import BiscaGameUI

player1 = RandomAgent("Player 1")
player2 = SimpleGreedyAgent("Player 2")

game = Game()
UI = BiscaGameUI()

# Get all available agents
agent_types = dict()
agent_names = []
for subclass in Player.__subclasses__():
    agent_types[subclass.__name__] = subclass
    agent_names.append(subclass.__name__)

agent_count = UI.showInitialScreen(agent_names)

player_count = 1
for agent in agent_count.keys():
     for playernr in range(agent_count[agent]):
           player = agent_types[agent](f'Player {str(player_count)}')
           game.add_player(player)
           player_count += 1

game.start_match()
while not game.is_over():

	game.next_round()

#print("GAME DONE")