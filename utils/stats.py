from engine.players import Player
from prettytable import PrettyTable
from datetime import datetime
import os
import json


class StatsRecorder:
    """
    A class for recording statistics across various games.
    """
    def __init__(self):
        self.player_stats = {}

    def _register_player(self, player: Player):
        """
        Registers a player in the stats recorder.
        """
        if player not in self.player_stats:
            self.player_stats[player] = {
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "trick_turnovers": [],  # Per trick
                "game_turnovers": [],  # Per game
            }

    def increment_wins(self, player: Player):
        """
        Increments the number of wins a player has.
        """
        self._register_player(player)
        self.player_stats[player]["wins"] += 1

    def increment_draws(self, player: Player):
        """
        Increments the number of draws a player has.
        """
        self._register_player(player)
        self.player_stats[player]["draws"] += 1

    def increment_losses(self, player: Player):
        """
        Increments the number of losses a player has.
        """
        self._register_player(player)
        self.player_stats[player]["losses"] += 1

    def add_game_points(self, player: Player, points: int):
        """
        Adds the number of points a player scored per game.
        """
        self._register_player(player)
        self.player_stats[player]["game_turnovers"].append(points)

    def add_trick_points(self, player: Player, points: int):
        """
        Adds the number of points a player scored per trick.
        """
        self._register_player(player)
        self._register_player(player)
        self.player_stats[player]["trick_turnovers"].append(points)

    def compare_players(self, player1: Player, player2: Player):
        """
        Compares two players based on their wins, losses, and point turnovers.
        """
        comparison = {
            player1: self.get_player_stats(player1),
            player2: self.get_player_stats(player2),
        }

        return comparison

    def get_player_stats(self, player: Player):
        """
        Returns a dictionary of a player's stats, including a calculation of the average points per game.
        """
        return {
            "type": player.type,
            "wins": self.player_stats[player].get("wins", 0),
            "losses": self.player_stats[player].get("losses", 0),
            "draws": self.player_stats[player].get("draws", 0),
            "average_points_per_game": sum(self.player_stats[player].get("game_turnovers", 0)) / len(self.player_stats[player].get("game_turnovers", 0))
            if self.player_stats[player].get("game_turnovers", False)
            else 0,
            "highest_game_turnover": max(
                self.player_stats[player].get("game_turnovers", 0)
            ),
            "average_points_per_trick": sum(
                self.player_stats[player].get("trick_turnovers", 0)
            )
            / len(self.player_stats[player].get("trick_turnovers", 0))
            if self.player_stats[player].get("trick_turnovers", False)
            else 0,
            "highest_trick_turnover": max(
                self.player_stats[player].get("trick_turnovers", 0)
            )
        }

    def rank_players(self, criterion="wins"):
        """
        Ranks players based on a given criterion, out of wins, total points scored and average points scored per game.
        """
        if criterion == "wins":
            sorted_players = sorted(
                self.player_stats.keys(),
                key=lambda p: self.player_stats[p]["wins"],
                reverse=True,
            )
        elif criterion == "points":
            sorted_players = sorted(
                self.player_stats.keys(),
                key=lambda p: sum(self.player_stats[p]["game_turnovers"]),
                reverse=True,
            )
        elif criterion == "average_game_turnover":
            sorted_players = sorted(
                self.player_stats.keys(),
                key=lambda p: self.player_stats[p]["average_game_turnover"],
                reverse=True,
            )
        else:
            raise ValueError(
                "Invalid criterion. Available options are 'wins', 'points', and 'average_game_turnover'."
            )

        return sorted_players

    def save(self, filename=None):
        """
        Saves the stats to a JSON file.
        """
        if filename is None:
            filename = f"stats-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"

        parsed_stats = {
            "players": {},
            "iterations": len(
                self.player_stats[list(self.player_stats.keys())[0]]["game_turnovers"]
            ),
        }

        # Create directory if it doesn't exist
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, "w") as f:
            for player in self.player_stats:
                parsed_stats["players"][player.name] = self.get_player_stats(player)

            json.dump(parsed_stats, f, indent=4)

    def print_table(self, criterion="wins"):
        """
        Prints a table of the player stats.
        """
        sorted_players = self.rank_players(criterion)

        table = PrettyTable()
        table.field_names = [
            "Player",
            "Type",
            "Wins",
            "Draws",
            "Losses",
            "W/L Ratio",
            "Average Points / Game",
            "Highest Point Turnover (Game)",
            "Average Points / Trick",
            "Highest Point Turnover (Trick)",
        ]

        for player in sorted_players:
            stats = self.get_player_stats(player)

            win_loss_ratio = (
                stats["wins"] / stats["losses"]
                if stats["losses"] != 0
                else stats["wins"]
            )

            table.add_row(
                [
                    player,
                    player.type,
                    stats["wins"],
                    stats["draws"],
                    stats["losses"],
                    f"{win_loss_ratio:.5f}",
                    f"{stats['average_points_per_game']:.2f}",
                    stats["highest_game_turnover"],
                    f"{stats['average_points_per_trick']:.2f}",
                    stats["highest_trick_turnover"],
                ]
            )
            table.align = "l"

        print(f"Ranking based on {criterion}:")
        print(table)
