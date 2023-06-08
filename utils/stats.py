from engine.players import Player
from prettytable import PrettyTable

class StatsRecorder:
    def __init__(self):
        self.player_stats = {}

    def _register_player(self, player: Player):
        if player not in self.player_stats:
            self.player_stats[player] = {
                "wins": 0, 
                "losses": 0, 
                "draws": 0,
                "point_turnovers": [],          # Per game
                "highest_point_turnover": 0     # Per trick
                }

    def increment_wins(self, player: Player):
        self._register_player(player)
        self.player_stats[player]["wins"] += 1

    def increment_draws(self, player: Player):
        self._register_player(player)
        self.player_stats[player]["draws"] += 1

    def increment_losses(self, player: Player):
        self._register_player(player)
        self.player_stats[player]["losses"] += 1

    def add_points(self, player: Player, points: int):
        """
        Adds the number of points a player scored per game.
        """
        self._register_player(player)
        self.player_stats[player]["point_turnovers"].append(points)

    def update_highest_point_turnover(self, player: Player, points: int):
        """
        Updates the highest number of points a player scored in a single trick.
        """
        if points > self.player_stats[player]["highest_point_turnover"]:
            self.player_stats[player]["highest_point_turnover"] = points

    def compare_players(self, player1: Player, player2: Player):
        """
        Compares two players based on their wins, losses, and point turnovers.
        """
        comparison = {
            player1: self.get_player_stats(player1),
            player2: self.get_player_stats(player2)
        }

        return comparison
    
    def get_player_stats(self, player: Player):
        return {
                "wins": self.player_stats[player].get("wins", 0),
                "losses": self.player_stats[player].get("losses", 0),
                "draws": self.player_stats[player].get("draws", 0),
                "average_points_per_game": sum(self.player_stats[player].get("point_turnovers", 0)) / len(self.player_stats[player].get("point_turnovers", 0)) if self.player_stats[player].get("point_turnovers", False) else 0,
                "highest_point_turnover": self.player_stats[player].get("highest_point_turnover", 0)
            }

    def rank_players(self, criterion="wins"):
        if criterion == "wins":
            sorted_players = sorted(
                self.player_stats.keys(), key=lambda p: self.player_stats[p]["wins"], reverse=True
            )
        elif criterion == "points":
            sorted_players = sorted(
                self.player_stats.keys(),
                key=lambda p: sum(self.player_stats[p]["point_turnovers"]),
                reverse=True,
            )
        elif criterion == "average_point_turnover":
            sorted_players = sorted(
                self.player_stats.keys(),
                key=lambda p: self.player_stats[p]["average_point_turnover"],
                reverse=True,
            )
        else:
            raise ValueError("Invalid criterion. Available options are 'wins', 'points', and 'average_point_turnover'.")

        return sorted_players
    
    def print_table(self, criterion="wins"):
        sorted_players = self.rank_players(criterion)

        table = PrettyTable()
        table.field_names = ["Player", "Type", "Wins", "Draws", "Losses", "W/L Ratio", "Average Points / Game", "Highest Point Turnover (Trick)"]

        for player in sorted_players:
            stats = self.get_player_stats(player)

            win_loss_ratio = stats["wins"] / stats["losses"] if stats["losses"] != 0 else stats["wins"]

            table.add_row([player, player.type, stats["wins"], stats["draws"], stats["losses"], win_loss_ratio, f"{stats['average_points_per_game']:.2f}", stats["highest_point_turnover"]])

        print(f"Ranking based on {criterion}:")
        print(table)