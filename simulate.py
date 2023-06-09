#!/usr/bin/env python3

import argparse
import sys
import logging
import matplotlib
import numpy as np
from random import shuffle
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline # For interpolation
from engine.players import Player
from engine.game import Game
from utils.stats import StatsRecorder

# Loading the available player types (excluding Human)
PLAYER_TYPES = {clazz.__name__: clazz for clazz in Player.__subclasses__() if clazz.__name__ != 'Human'}

def run_simulations(iterations, delay, player_types, graph, interpolate, output, display=False):
    player_instances = []

    # Create player instances based on the specified player types
    for i in range(len(player_types)):
        player_class = PLAYER_TYPES[player_types[i]]
        if player_class:
            player_instance = player_class(f"Player {i + 1}")
            player_instances.append(player_instance)

    # Validate the number of players
    if len(player_instances) < 2 or len(player_instances) > 6:
        print('Invalid number of players. \nWhen using --player, specify between 2 and 6 players.')
        sys.exit(1)

    stats = StatsRecorder()

    for i in range(iterations):
        game = Game(stats_recorder=stats, delay=delay, log_level=logging.ERROR)

        # Shuffle the player starting positions
        shuffle(player_instances)
        
        # Add player instances to the game
        for player in player_instances:
            game.add_player(player)

        game.start_match()

        while not game.is_over():
            game.next_round()


        if display:
            print(f"Simulated game {i + 1}/{iterations}", end="\r")

    if display:
        # Display stats table
        print()
        stats.print_table()

    if graph:
        # Display the graph
        display_graph(stats, interpolate=interpolate)

    if (output):
        # Save the data to file
        stats.save(output)

    return [stats.get_player_stats(player) for player in stats.rank_players("wins")]

    

def display_graph(stats, interpolate=False):
    bar_criteria = ['wins', 'draws', 'average_points_per_game', 'highest_game_turnover', 'average_points_per_trick', 'highest_trick_turnover']
    line_criteria = ['game_turnovers']

    generations = range(1, len(list(stats.player_stats.values())[0]['game_turnovers']) + 1)
    num_players = len(stats.player_stats)
    ranked_players = stats.rank_players()

    # Bar chart for bar_criteria
    plt.figure("Overall Player Statistics")
    width = 0.2
    x = np.arange(num_players)

    for i, criterion in enumerate(bar_criteria):
        y = [stats.get_player_stats(player)[criterion] for player in ranked_players]
        plt.bar(x + (i * width), y, width=width, label=criterion)

    plt.xlabel('Players')
    plt.ylabel('Value')
    plt.title('Overall Player Statistics')
    plt.xticks(x + width * (len(bar_criteria) - 1) / 2, [f"{player.name} ({player.type})" for player in ranked_players])
    plt.grid(True)
    plt.legend()

    # Line graph with smoothing for line_criteria
    plt.figure("Per-iteration Player Statistics")
    for player in ranked_players:
        for criterion in line_criteria:
            y = stats.player_stats[player][criterion]

            if interpolate:
                # Perform spline interpolation for smoothing
                # Choose number of points to interpolate based on the number of iterations
                points = 100 if len(generations) < 100 else 1000 if len(generations) < 1000 else 10000
                x = np.linspace(min(generations), max(generations), points)  # Increase the number of points for smoother curve
                spl = make_interp_spline(generations, y, k=3)  # Cubic spline interpolation
                y = spl(x)
            else:
                x = generations

            plt.plot(x, y, label=f"{player.name} ({criterion})")

    plt.xlabel('Iterations')
    plt.ylabel('Values per player')
    plt.title('Per-iteration Player Statistics')
    plt.grid(True)
    plt.legend()

    # Display the plots on separate windows
    plt.show(block=False)
    plt.figure(1)
    plt.show()

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='BASIS Multi-Agent Platform')

    # Add arguments
    parser.add_argument('--iterations', type=int, default=1000, help='Number of simulations to run')
    parser.add_argument('--delay', type=int, default=0, help='Delay in seconds between each round')
    parser.add_argument('--player', action="append", nargs='+', choices=list(PLAYER_TYPES.keys()), help='Player types')
    parser.add_argument('--graph', action="store_true", help='Display graph')
    parser.add_argument('--interpolate', action="store_true", help='Interpolate graph, useful for large number of iterations')
    parser.add_argument('--output', default=None, action="store", help='Save data to file')
    

    # Parse the arguments
    args = parser.parse_args()

    # --interpolate is only valid if --graph is specified
    if args.interpolate and not args.graph:
        print('Invalid argument. --interpolate is only valid if --graph is specified.')
        sys.exit(1)

    # Flatting the player-argument list
    player_types = [item for sublist in args.player for item in sublist] if args.player else [
        "SimpleGreedyAgent", 
        "MinimizePointLossGreedyAgent",
        "MPLGreedyTrumpSaveAgent",
        "GreedyCountingAgent"]

    # Run the simulations
    run_simulations(args.iterations, args.delay, player_types, graph=args.graph, interpolate=args.interpolate, output=args.output)

if __name__ == '__main__':
    main()
