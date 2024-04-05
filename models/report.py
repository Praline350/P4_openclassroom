from .player import Player
from .tournament import Tournament
from .round import Round
from tinydb import Query
import os

# Chemins vers les fichiers export

FOLDER_EXPORT_DATA = "export_data"
EXPORT_PLAYERS_PATH = "export_data/export_players.txt"
EXPORT_PLAYERS_IN_TOURNAMENT_PATH = (
    "export_data/export_player_in_tournament.txt"
)
EXPORT_ROUNDS_PATH = "export_data/export_rounds.txt"
EXPORT_TOURNAMENT_PATH = "export_data/export_tournament.txt"


class Report:
    def __init__(self):
        if not os.path.exists(FOLDER_EXPORT_DATA):
            os.makedirs(FOLDER_EXPORT_DATA)
        self.round = Round()
        self.tournament = Tournament()
        self.player = Player()
        self.RoundQuery = Query()
        self.PlayerQuery = Query()
        self.TournamentQuery = Query()

    def format_report(self, data):
        if isinstance(data, list):
            for i in range(len(data)):
                data[i] = (
                    str(data[i]).replace("{", "").replace("}", ""),
                    str(data[i]).replace("'", ""),
                )
            return data
        elif isinstance(data, dict):
            formatted_data = ""
            for key, value in data.items():
                formatted_data += f"{key}: {value}\n"
            return formatted_data

    def player_report(self):
        player_data = self.player.players.all()
        sorted_players = sorted(player_data, key=lambda x: x["name"])
        return sorted_players

    def tournament_report(self, name_tournament):
        tournament_data = self.tournament.find_tournament(name_tournament)
        if tournament_data:
            filtered_data = {
                "name_tournament": tournament_data["name_tournament"],
                "localisation": tournament_data["localisation"],
                "start_date": tournament_data["start_date"],
                "end_date": tournament_data["end_date"],
            }
            return filtered_data
        else:
            print("Le tournoi spécifié n'existe pas.")
            return None

    def player_in_tournament_report(self, name_tournament):
        tournament_data = self.tournament.find_tournament(name_tournament)
        player_list = tournament_data.get("player_list", [])  # type: ignore
        sorted_players = sorted(player_list, key=lambda x: x["name"])
        return sorted_players

    def export_players_to_file(self, data):
        try:
            with open(EXPORT_PLAYERS_PATH, "w") as file:
                for item in data:
                    file.write(f"{item}\n")
        except Exception:
            return False
        else:
            print("Données exportées avec succès.")
            return True

    def export_tournament_to_file(self, data):
        try:
            with open(EXPORT_TOURNAMENT_PATH, "a") as file:
                file.write(str(data) + "\n")
        except Exception:
            return False
        else:
            print("Données exporté")
            return True

    def export_player_in_tournament(self, name_tournament, data):
        try:
            with open(EXPORT_PLAYERS_IN_TOURNAMENT_PATH, "w") as file:
                file.write(f"Tournoi: {name_tournament}\n")
                for item in data:
                    file.write(f"{item}\n")
        except Exception:
            return False
        else:
            print("données exporté")
            return True

    def round_report(self, name_tournament):
        tournament_data = self.tournament.find_tournament(name_tournament)
        if tournament_data:
            round_table = self.tournament.db_tournament.table("rounds")
            all_rounds = round_table.all()
            return all_rounds
        else:
            return False

    def export_round_to_file(self, data):
        try:
            with open(EXPORT_ROUNDS_PATH, "w") as file:
                for round_info in data:
                    file.write(f"Round Index: {round_info['round_index']}\n")
                    file.write(f"Start Date: {round_info['start_date']}\n")
                    file.write(f"End Date: {round_info['end_date']}\n")
                    file.write("Game List:\n")
                    for game_info in round_info["game_list"]:
                        file.write(f"    Game ID: {game_info['game_id']}\n")
                        for player_info in game_info["players"]:
                            file.write(
                                f"        Player: {player_info['name']}, "
                                f"National ID: {player_info['national_id']}, "
                                f"Score: {player_info['score']}\n"
                            )
                    file.write("\n")
            print("Données exportées")
        except Exception:
            return False
