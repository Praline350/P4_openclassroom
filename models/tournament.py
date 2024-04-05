from .player import Player
from tinydb import TinyDB, Query
import os

FOLDER_DATA_TOURNAMENTS_PATH = "data/data_tournament"


class Tournament:

    def __init__(self):
        self.player = Player()
        # Initialisation du folder data_tournament
        if not os.path.exists(FOLDER_DATA_TOURNAMENTS_PATH):
            os.makedirs(FOLDER_DATA_TOURNAMENTS_PATH)
        # Initialisation des requêtes pour les joueurs et les tournois

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
            "player_list": [],
            "description": "",
        }
        self.tournament.insert(self.data)

    def remove_tournament(self, name_tournament):
        file_path = f"data/data_tournament/{name_tournament}.json"
        if os.path.exists(file_path):
            os.remove(file_path)
            print("Tournoi supprimé avec succès.")
            return True
        else:
            print("Tournoi inexistant.")
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
                        f"Joueur {player_data['name']}"
                        f"ajouté à {name_tournament}"
                    )
                else:
                    return (
                        True,
                        f"{player_data['name']} déjà dans {name_tournament}"
                    )
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
                    print(
                        f"Joueur {player['name']} retiré du {name_tournament}"
                        )
                    return True
            self.tournament.update(
                {"player_list": player_list},
                Query().name_tournament == name_tournament,
            )

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
            # retourne True si le joueur est dans le tournoi
            return player_in_tournament

    def get_name_tournaments(self):
        names_tournament = []
        for filename in os.listdir(FOLDER_DATA_TOURNAMENTS_PATH):
            name_tournament = os.path.splitext(filename)[0]
            names_tournament.append(name_tournament)
        return names_tournament

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
