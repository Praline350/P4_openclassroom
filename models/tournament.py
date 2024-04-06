from .player import Player
from tinydb import TinyDB, Query
import os
from datetime import datetime
import shutil

FOLDER_DATA_TOURNAMENTS_PATH = "data/data_tournament"
FOLDER_BACKUP_TOURNAMENT_PATH = "data/backup_tournament"


class Tournament:

    def __init__(self):
        self.player = Player()
        # Initialisation du folder data_tournament
        if not os.path.exists(FOLDER_DATA_TOURNAMENTS_PATH):
            os.makedirs(FOLDER_DATA_TOURNAMENTS_PATH)
        # Initialisation des requêtes pour les joueurs et les tournois
        if not os.path.exists(FOLDER_BACKUP_TOURNAMENT_PATH):
            os.makedirs(FOLDER_BACKUP_TOURNAMENT_PATH)

    def initialize_db(self, name_tournament):
        file_path = f"data/data_tournament/{name_tournament}.json"
        self.db_tournament = TinyDB(file_path, indent=4, encoding="utf-8")
        self.tournament = self.db_tournament.table(name_tournament)

    def write_tournament(
        self, name_tournament, localisation, round, start_date, end_date
    ):
        self.initialize_db(name_tournament)
        self.data = {
            "name_tournament": name_tournament,
            "localisation": localisation,
            "rounds_number": round,
            "start_date": start_date,
            "end_date": end_date,
            "actual_round": 0,
            "winner": "",
            "description": "",
            "player_list": [],
        }
        self.tournament.insert(self.data)

    def remove_tournament(self, name_tournament):
        file_path = f"data/data_tournament/{name_tournament}.json"
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            return False

    def add_player_in_tournament(self, name_tournament, id_player):
        player_data = self.player.find_player(id_player)
        if player_data:
            player_in_tournament = self.find_player_in_tournament(
                name_tournament, id_player
            )
            tournament_data = self.find_tournament(name_tournament)
            if tournament_data:
                player_list = tournament_data.get("player_list", [])
                if not player_in_tournament:
                    player_list.append(
                        {
                            "national_id": player_data["national_id"],
                            "name": player_data["name"],
                            "score": 0,
                        }
                    )
                    self.tournament.update(
                        {"player_list": player_list},
                        Query().name_tournament == name_tournament,
                    )
                    return (
                        True,
                        f"Joueur {player_data['name']} " f"ajouté à {name_tournament}",
                    )
                else:
                    return (False, f"{player_data['name']} déjà dans {name_tournament}")
            else:
                return False, "tournoi inexistant"
        else:
            return False, "Joueur inexistant"

    def remove_player_in_tournament(self, name_tournament, id_player):
        player_in_tournament = self.find_player_in_tournament(
            name_tournament, id_player
        )
        tournament_data = self.find_tournament(name_tournament)
        if tournament_data:
            player_list = tournament_data.get("player_list", [])
        if player_in_tournament:
            for player in player_list:
                if player.get("national_id") == id_player:
                    player_list.remove(player)

            self.tournament.update(
                {"player_list": player_list},
                Query().name_tournament == name_tournament,
            )
            return True
        else:
            return False

    def find_tournament(self, name_tournament):
        file_path = f"data/data_tournament/{name_tournament}.json"
        self.db_tournament = TinyDB(file_path, indent=4)
        tournament_table = self.db_tournament.table(name_tournament)
        tournament_data = tournament_table.all()
        if tournament_data:
            return tournament_data[0]
        else:
            return None

    def find_player_in_tournament(self, name_tournament, id_player):
        self.initialize_db(name_tournament)
        tournament_data = self.find_tournament(name_tournament)
        if tournament_data:
            player_list = tournament_data.get("player_list", [])
            player_in_tournament = any(
                player["national_id"] == id_player for player in player_list
            )

            return player_in_tournament

    def get_ids_in_tournament(self, name_tournament):
        tournament_data = self.find_tournament(name_tournament)
        if tournament_data:
            player_list = tournament_data.get("player_list", [])
            player_ids = [player["national_id"] for player in player_list]
            return player_ids
        else:
            return False

    def get_name_tournaments(self):
        names_tournament = []
        for filename in os.listdir(FOLDER_DATA_TOURNAMENTS_PATH):
            name_tournament = os.path.splitext(filename)[0]
            names_tournament.append(name_tournament)
        return names_tournament

    def get_name_backup(self):
        name_backup = []
        for filename in os.listdir(FOLDER_BACKUP_TOURNAMENT_PATH):
            name_tournament = os.path.splitext(filename)[0]
            name_backup.append(name_tournament)
        return name_backup

    def get_round_index(self, name_tournament):
        self.initialize_db(name_tournament)
        round_table = self.db_tournament.table("rounds")
        round_index = len(round_table)
        return round_index

    def get_actual_round(self, name_tournament):
        tournament_data = self.find_tournament(name_tournament)
        if tournament_data:
            actual_round = tournament_data.get("actual_round")
            return actual_round

    def get_rounds_number(self, name_tournament):
        tournament_data = self.find_tournament(name_tournament)
        if tournament_data:
            rounds_number = tournament_data.get("rounds_number")
            return rounds_number

    def check_for_end(self, name_tournament):
        actual_round = self.get_actual_round(name_tournament)
        rounds_number = self.get_rounds_number(name_tournament)
        if actual_round == rounds_number:
            return True

    def end_tournament(self, name_tournament):
        self.initialize_db(name_tournament)
        tournament_data = self.find_tournament(name_tournament)
        if tournament_data:
            player_list = tournament_data.get("player_list", [])
            tournament_winner = player_list[0]["name"]
            self.tournament.update(
                {"actual_round": "tournament closed"},
                Query().name_tournament == name_tournament,
            )
            self.tournament.update(
                {"winner": tournament_winner},
                Query().name_tournament == name_tournament,
            )

            return tournament_winner

    def save_in_backup(self, name_tournament):
        tournament_file = f"{name_tournament}.json"
        tournament_path = os.path.join(FOLDER_DATA_TOURNAMENTS_PATH, tournament_file)
        current_date = datetime.now().strftime("%Y-%m-%d_%Hh%Mm")
        backup_filename = f"{name_tournament}_{current_date}.json"
        backup_path = os.path.join(FOLDER_BACKUP_TOURNAMENT_PATH, backup_filename)
        success = shutil.copy(tournament_path, backup_path)
        return success

    def restore_backup(self, backup_name):
        backup_path = os.path.join(FOLDER_BACKUP_TOURNAMENT_PATH, f"{backup_name}.json")
        name_tournament = backup_name.split("_")[0]
        path = os.path.join(FOLDER_DATA_TOURNAMENTS_PATH, f"{name_tournament}.json")
        print(backup_path, path)
        shutil.copy(backup_path, path)
        return name_tournament

    def add_description(self, name_tournament, data):
        self.initialize_db(name_tournament)
        tournament_data = self.find_tournament(name_tournament)
        if tournament_data:
            self.tournament.update(
                {"description": data}, Query().name_tournament == name_tournament
            )
            return True
        else:
            return False
