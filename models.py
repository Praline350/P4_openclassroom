import json
from tinydb import TinyDB, Query
import os
from datetime import datetime, timedelta
import time
import random

# Chemins vers les fichiers JSON de données

JSON_DATA_PLAYERS_PATH = "data/data_players.json"
FOLDER_DATA_TOURNAMENTS_PATH = "data/data_tournament"
JSON_DATA_ROUNDS_PATH = "data/data_rounds.json"

# Chemins vers les fichiers export

FOLDER_EXPORT_DATA = "export_data"
EXPORT_PLAYERS_PATH = "export_data\export_players.txt"
EXPORT_PLAYERS_IN_TOURNAMENT_PATH = "export_data\export_player_in_tournament.txt"
EXPORT_ROUNDS_PATH = "export_data\export_rounds.txt"
EXPORT_TOURNAMENT_PATH = "export_data\export_tournament.txt"


class Player:

    def __init__(self):
        # Initialisation de la base de données des joueurs
        self.db_player = TinyDB(JSON_DATA_PLAYERS_PATH, indent=4, encoding="utf-8")
        self.players = self.db_player.table("Players")
        if not os.path.exists(JSON_DATA_PLAYERS_PATH):
            with open(JSON_DATA_PLAYERS_PATH, "w") as f:
                json.dump([], f)
        # Initialisation de la requête pour les joueurs

    def write_player(self, surname, name, birth_date, national_id):
        # Écriture des données d'un joueur dans la base de données
        self.data = {
            "surname": surname,
            "name": name,
            "birth_date": birth_date,
            "national_id": national_id,
        }
        self.players.insert(self.data)

    def find_player(self, national_id):
        # Recherche d'un joueur par son ID national
        player_data = self.players.search(Query().national_id == national_id)
        if player_data:
            return player_data[0]
        else:
            return None

    def get_all_player_id(self):
        player_data = self.players.all()
        sorted_id = sorted(player_data, key=lambda x: x["national_id"])
        players_ids = []
        for ids in sorted_id:
            players_ids.append(ids["national_id"])
        return players_ids

    def get_all_player_name(self):
        player_name = []
        player_data = self.players.all()
        sorted_name = sorted(player_data, key=lambda x: x["name"])
        for name in sorted_name:
            player_name.append(name["name"])
        return player_name

    def remove_player(self, national_id):
        self.players.remove(Query().national_id == national_id)
        player_data = self.players.search(Query().national_id == national_id)
        if not player_data:
            return True  # retourne true si le joueur est suppr


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
                        f"Joueur {player_data['name']} ajouté à {name_tournament}",
                    )
                else:
                    return False, f"{player_data['name']} déjà dans {name_tournament}"
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
                    print(f"Joueur {player['name']} retiré du {name_tournament}")
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


class Round:

    def __init__(self):
        self.tournament = Tournament()
        self.player = Player()

    def add_round(self, name_tournament):
        self.tournament.initialize_db(name_tournament)
        round_table = self.tournament.db_tournament.table("rounds")
        start_date = datetime.now().strftime("%d-%m-%Y")
        start_hour = datetime.now()
        len_round = len(round_table)
        round_index = len_round + 1
        actual_round = round_index
        round_data = {
            "round_index": round_index,
            "start_date": start_date,
            "start_hour": start_hour.strftime("%H:%M"),
            "end_date": "",
            "end_hour": "",
            "game_list": [],
        }
        round_table.insert(round_data)
        self.tournament.tournament.update(
            {"actual_round": actual_round}, Query().name_tournament == name_tournament
        )

        return round_index

    def mix_players_random(self, name_tournament):
        self.tournament.initialize_db(name_tournament)
        tournament_data = self.tournament.find_tournament(name_tournament)
        if tournament_data:
            tournament_round = tournament_data.get("player_list", [])
            random.shuffle(tournament_round)
            self.tournament.tournament.update(
                {"player_list": tournament_round},
                Query().name_tournament == name_tournament,
            )

    def find_round(self, name_tournament, round_index):
        self.tournament.initialize_db(name_tournament)
        round_table = self.tournament.db_tournament.table("rounds")
        round_data = round_table.get(Query().round_index == round_index)
        if round_data and round_table:
            return round_data

    def remove_round(self, name_tournament, round_index):
        self.tournament.initialize_db(name_tournament)
        round_table = self.tournament.db_tournament.table("rounds")
        round_data = round_table.search(Query().round_index == round_index)
        if round_data:
            round_table.remove(Query().round_index == round_index)
            print(f"Round {round_index} supprimé avec succès")
            return True
        else:
            return None


class Game:

    def __init__(self):
        self.round = Round()
        self.tournament = Tournament()
        self.player = Player()

    def make_game(self, name_tournament, round_index):
        self.tournament.initialize_db(name_tournament)
        tournament_data = self.tournament.find_tournament(name_tournament)
        round_table = self.tournament.db_tournament.table("rounds")
        round_data = self.round.find_round(name_tournament, round_index)
        if tournament_data and round_data:
            game_list = round_data.get("game_list", [])
            player_list = tournament_data.get("player_list", [])
            num_players = len(player_list)
            # Vérifie que les joueurs sont bien un nombre pair
            if num_players % 2 != 0:
                print("nombre impaire")
                return False
            for i in range(0, num_players, 2):
                player_pair = (player_list[i], player_list[i + 1])
                game_id = len(game_list) + 1
                pair_already_in_game = False
                for game in game_list:
                    if (
                        player_pair[0] in game["players"]
                        or player_pair[1] in game["players"]
                    ):
                        pair_already_in_game = True
                        break
                # Si les joueurs ne sont pas encore dans un match, créer un match par pair
                if not pair_already_in_game:
                    game_list.append({"game_id": game_id, "players": player_pair})
            print(game_list)
            round_table.update(
                {"game_list": game_list}, Query().round_index == round_index
            )

    def play_game(self, name_tournament, round_index):
        round_table = self.tournament.db_tournament.table("rounds")
        round_data = self.round.find_round(name_tournament, round_index)
        if round_data:
            game_list = round_data.get("game_list", [])
            if game_list:
                for game in game_list:
                    time.sleep(0.7)
                    # Remet le score a 0 pour avoir un score unique par match
                    for player in game["players"]:
                        player["score"] = 0
                    win_pourcentage = 0.3
                    result = random.random()
                    if result > win_pourcentage:
                        winner = random.choice(game["players"])
                        winner_index = game["players"].index(winner)
                        game["players"][winner_index]["score"] = 1
                        looser = game["players"][1 - winner_index]
                        round_table.update(
                            {"game_list": game_list}, Query().round_index == round_index
                        )
                        print(f"{winner['name']} à gagner contre {looser['name']}")
                    else:
                        for player in game["players"]:
                            player["score"] = 0.5
                        round_table.update(
                            {"game_list": game_list}, Query().round_index == round_index
                        )
                        print(
                            f"Match nul entre {game['players'][0]['name']} et {game['players'][1]['name']}"
                        )

    def end_game(self, name_tournament, round_index):
        self.tournament.initialize_db(name_tournament)
        tournament_data = self.tournament.find_tournament(name_tournament)
        round_data = self.round.find_round(name_tournament, round_index)
        player_list = tournament_data.get("player_list", [])
        game_list = round_data.get("game_list", [])
        end_date = datetime.now().strftime("%d-%m-%Y")
        end_hour = datetime.now().strftime("%H:%M")
        for game in game_list:
            for player in game["players"]:
                national_id = player["national_id"]
                score_change = player["score"]
                for p in player_list:
                    if p["national_id"] == national_id:
                        p["score"] += score_change
        self.tournament.tournament.update({"player_list": player_list})
        round_data["end_date"] = end_date  # type: ignore
        round_data["end_hour"] = end_hour  # type: ignore
        self.tournament.db_tournament.table("rounds").update(
            round_data, doc_ids=[round_index]  # type: ignore
        )

    def sorted_score(self, name_tournament):
        self.tournament.initialize_db(name_tournament)
        tournament_data = self.tournament.find_tournament(name_tournament)
        if tournament_data:
            player_list = tournament_data.get("player_list", [])
            sorted_players = sorted(player_list, key=lambda x: x["score"], reverse=True)
            self.tournament.tournament.update({"player_list": sorted_players})


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
                    str(data[i]).replace("{", "").replace("}", "").replace("'", "")
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
        player_list = tournament_data.get("player_list", [])
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
                                f"        Player: {player_info['name']}, National ID: {player_info['national_id']}, Score: {player_info['score']}\n"
                            )
                    file.write("\n")
            print("Données exportées")
        except Exception:
            return False
