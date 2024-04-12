from .player import Player
from .tournament import Tournament
from .round import Round
import os

# Chemins vers les fichiers export

FOLDER_EXPORT_DATA = "export_data"
EXPORT_PLAYERS_PATH = "export_data/export_players.txt"
EXPORT_PLAYERS_IN_TOURNAMENT_PATH = "export_data/export_player_in_tournament"
EXPORT_ROUNDS_PATH = "export_data/export_rounds"
EXPORT_TOURNAMENT_PATH = "export_data/export_tournament.txt"


class Report:
    def __init__(self):
        if not os.path.exists(FOLDER_EXPORT_DATA):
            os.makedirs(FOLDER_EXPORT_DATA)
        self.round = Round()
        self.tournament = Tournament()
        self.player = Player()

    def format_report(self, data):
        if isinstance(data, list):
            for index, item in enumerate(data):
                data[index] = (
                    str(item).replace("{", "").replace("}", "").replace(
                        "'", ""
                        )
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
        data = self.format_report(sorted_players)
        return data

    def tournament_report(self, name_tournament):
        tournament_data = self.tournament.find_tournament(name_tournament)
        if tournament_data:
            filtered_data = {
                "name_tournament": tournament_data["name_tournament"],
                "localisation": tournament_data["localisation"],
                "start_date": tournament_data["start_date"],
                "end_date": tournament_data["end_date"],
                "actual_round": tournament_data["actual_round"],
                "winner": tournament_data["winner"],
            }
            data = self.format_report(filtered_data)
            return data
        else:
            return False

    def player_in_tournament_report(self, name_tournament):
        tournament_data = self.tournament.find_tournament(name_tournament)
        player_list = tournament_data.get("player_list", [])  # type: ignore
        sorted_players = sorted(player_list, key=lambda x: x["name"])
        data = self.format_report(sorted_players)
        return data

    def export_players_to_file(self, data):
        try:
            with open(EXPORT_PLAYERS_PATH, "w", encoding="utf-8") as file:
                for item in data:
                    file.write(f"{item}\n")
        except Exception:
            return False
        else:
            return True

    def export_tournament_to_file(self, data):
        try:
            with open(EXPORT_TOURNAMENT_PATH, "a", encoding="utf-8") as file:
                file.write(str(data) + "\n")
        except Exception:
            return False
        else:
            return True

    def export_player_in_tournament(self, name_tournament, data):
        try:
            with open(
                f"{EXPORT_PLAYERS_IN_TOURNAMENT_PATH}_{name_tournament}.txt",
                "w", encoding="utf-8"
            ) as file:
                for item in data:
                    file.write(f"{item}\n")
        except Exception:
            return False
        else:
            return True

    def round_report(self, name_tournament):
        tournament_data = self.tournament.find_tournament(name_tournament)
        if tournament_data:
            round_table = self.tournament.db_tournament.table("rounds")
            all_rounds = round_table.all()
            data = self.format_round(all_rounds)
            return data
        else:
            return False

    def format_round(self, data):
        formatted_data = ""
        for round_info in data:
            formatted_data += f"Round Index: {round_info['round_index']}\n"
            formatted_data += f"Start Date: {round_info['start_date']}\n"
            formatted_data += f"End Date: {round_info['end_date']}\n"
            formatted_data += "Game List:\n"
            for game_info in round_info["game_list"]:
                formatted_data += f"    Game ID: {game_info['game_id']}\n"
                for player_info in game_info["players"]:
                    formatted_data += (
                        f"        Player: {player_info['name']}, "
                        f"National ID: {player_info['national_id']}, "
                        f"Score: {player_info['score']}\n"
                    )
            formatted_data += "\n"
        return formatted_data

    def export_round_to_file(self, name_tournament, data):
        try:
            with open(
                f"{EXPORT_ROUNDS_PATH}_{name_tournament}.txt",
                "w", encoding="utf-8"
            ) as file:
                file.write(data)
        except Exception:
            return False
        else:
            return True


if __name__ == "__main__":
    pass
