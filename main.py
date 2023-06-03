from engine.game import Game
from engine.players import Player, Human, RandomAgent, SimpleGreedAgent
from UI.game import BiscaGameUI

# Start the first game

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
while (len(game.deck) > 0 ) :
	game.next_round()

#print("GAME DONE")