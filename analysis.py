#!/usr/bin/env python3

import itertools
import datetime
import json
from prettytable import PrettyTable
from simulate import run_simulations

EXPERIMENT_SIMULATIONS = 100000

def simulate_combinations(players):
    # Generate all combinations of agent groups for the specified number of players
    combinations = list(itertools.combinations(agent_types, players))

    # Initialize a dictionary to store the results
    results = {}

    # Loop through each combination of agent groups
    for combination in combinations:
        update_progress(players, combination)
        # Run the simulation for the current player group and agent combination
        stats = run_simulations(EXPERIMENT_SIMULATIONS, 0, combination, False, False, None, display=False)

        # Aggregate the results for each player
        for player_stats in stats:
            player_type = player_stats["type"]
            player_result = results.get(player_type, {})
            player_result.setdefault("wins", 0)
            player_result.setdefault("losses", 0)
            player_result.setdefault("draws", 0)
            player_result.setdefault("average_points_per_game", 0)
            player_result.setdefault("highest_game_turnover", 0)
            player_result.setdefault("average_points_per_trick", 0)
            player_result.setdefault("highest_trick_turnover", 0)

            player_result["type"] = player_type
            player_result["wins"] += player_stats["wins"]
            player_result["losses"] += player_stats["losses"]
            player_result["draws"] += player_stats["draws"]
            player_result["average_points_per_game"] =+ player_stats["average_points_per_game"]
            player_result["highest_game_turnover"] =+ player_stats["highest_game_turnover"]
            player_result["average_points_per_trick"] =+ player_stats["average_points_per_trick"]
            player_result["highest_trick_turnover"] =+ player_stats["highest_trick_turnover"]

            results[player_type] = player_result
    
    # Results aggregated by player type, for the given amount of players
    return results

# Define the agent types
agent_types = ["RandomAgent", "SimpleGreedyAgent", "MinimizePointLossGreedyAgent",
               "MPLGreedyTrumpSaveAgent", "MPLGreedyTrumpBasedAgent", "GreedyCountingAgent"]

# Define the maximum number of players
max_players = 6

def update_progress(player_num, combination):
    # Print the current player number and agent combination with \r
    print(f"Running simulations for groups of {player_num} players. Agent Combination: {combination}")

# Results per group size
results = {}

start = datetime.datetime.now()

# Loop through each player group size
for group_size in range(2, max_players+1):
    # Run the simulation for the current player group size
    results[group_size] = simulate_combinations(group_size)

end = datetime.datetime.now()

# Printing a table with the results for each player in each group size

# Define the table headers
headers = ["Player Type", "Wins", "Losses", "Draws", "Average Points Per Game", "Highest Game Turnover", "Average Points Per Trick", "Highest Trick Turnover"]

# Loop through each player group size
for group_size in range(2, max_players+1):

    # Create a new table
    table = PrettyTable()

    # Set the table headers
    table.field_names = headers

    # Sort the result values by wins
    sorted_results = sorted(results[group_size].values(), key=lambda x: x["wins"], reverse=True)
    results[group_size] = sorted_results

    # Loop through each player type and corresponding results
    for player_results in sorted_results:

        # Add a row to the table with the results
        table.add_row([player_results["type"], player_results["wins"], player_results["losses"], player_results["draws"], player_results["average_points_per_game"], player_results["highest_game_turnover"], player_results["average_points_per_trick"], player_results["highest_trick_turnover"]])
        table.align = "l"

    # Print the table
    print(f"Results for {group_size} players:")
    print(table)
    print()

# Save the results for each groupsize to a file with datetime as name
filename = f"analysis_results_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

with open(filename, "w") as f:
    json.dump(results, f, indent=4)

print(f"Analysis completed in {end-start}. Results saved to {filename}.")