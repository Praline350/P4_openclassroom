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


class Player:

    def __init__(self):
        # Initialisation de la base de données des joueurs
        self.db_player = TinyDB(JSON_DATA_PLAYERS_PATH, indent=4)
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


class Tournament:

    def __init__(self):
        self.player = Player()
        # Initialisation du folder data_tournament
        if not os.path.exists(FOLDER_DATA_TOURNAMENTS_PATH):
            os.makedirs(FOLDER_DATA_TOURNAMENTS_PATH)
        # Initialisation des requêtes pour les joueurs et les tournois

    def initialize_db(self, name_tournament):
        file_path = f"data/data_tournament/{name_tournament}.json"
        self.db_tournament = TinyDB(file_path, indent=4)
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
            "player_list": [],
            "description": "",
        }
        self.tournament.insert(self.data)

    def remove_tournament(self, name_tournament):
        file_path = f"data/data_tournament/{name_tournament}.json"
        if os.path.exists(file_path):
            os.remove(file_path)
            print("Tournoi supprimé avec succès.")
        else:
            print("Tournoi inexistant.")

    def add_player(self, name_tournament, id_player):
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
                    print(f"Joueur {player_data['name']} ajouté à {name_tournament}")
                else:
                    print(f"{player_data['name']} déjà dans {name_tournament}")
            else:
                print("tournoi inexistant")
        else:
            print("Joueur inéxistant")

    def remove_player(self, name_tournament, id_player):
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
                    break
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


class Round:

    def __init__(self):
        self.tournament = Tournament()
        self.player = Player()

    def add_round(self, name_tournament):
        self.tournament.initialize_db(name_tournament)
        round_table = self.tournament.db_tournament.table("rounds")
        start_date = datetime.now()
        end_date = start_date + timedelta(hours=4)
        len_round = len(round_table)
        round_index = len_round + 1
        round_data = {
            "round_index": round_index,
            "start_date": start_date.strftime("%H:%M"),
            "end_date": end_date.strftime("%H:%M"),
            "game_list": []
        }
        round_table.insert(round_data)

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


class Game:

    def __init__(self):
        self.round = Round()
        self.tournament = Tournament()
        self.player = Player()

    def make_game(self, name_tournament, round_index):
        self.tournament.initialize_db(name_tournament)
        tournament_data = self.tournament.find_tournament(name_tournament)
        round_table = self.tournament.db_tournament.table('rounds')
        round_data = self.round.find_round(name_tournament, round_index)
        if tournament_data and round_data:
            game_list = round_data.get("game_list", [])
            player_list = tournament_data.get("player_list", [])
            num_players = len(player_list)
            # Vérifie que les joueurs sont bien un nombre pair
            if num_players % 2 != 0:
                print("nombre impaire")
                return
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
            round_table.update({'game_list': game_list}, Query().round_index == round_index)
                    
            

            # self.tournament.tournament.update({'rounds': game_list}, Query().name_tournament == name_tournament)

    def play_game(self, name_tournament, round_index):
        round_table = self.round.db_rounds.table(name_tournament)
        round_data = self.round.find_round(round_index, name_tournament)
        if round_data:
            game_list = round_data.get("game_list", [])
            if game_list:
                for game in game_list:
                    time.sleep(1)
                    # Initialise un pourcentage de victoire et de match nul
                    win_pourcentage = 0.3
                    result = random.random()
                    if result > win_pourcentage:
                        winner = random.choice(game["players"])
                        winner_index = game["players"].index(winner)
                        game["players"][winner_index]["score"] = 1
                        print(
                            f"{winner['name']} à gagner contre {game['players'][1 - winner_index]['name']}"
                        )
                    else:
                        for player in game["players"]:
                            player["score"] = 0.5
                        print(
                            f"Match nul entre {game['players'][0]['name']} et {game['players'][1]['name']}"
                        )
                round_table.update({"game_list": game_list})

    def end_game(self, name_tournament, round_index):
        tournament_table = self.tournament.db_tournament.table(name_tournament)
        round_data = self.round.find_round(round_index, name_tournament)
        tournament_data = self.tournament.find_tournament(name_tournament)
        game_list = round_data.get("game_list", [])
        player_list = tournament_data.get("player_list", [])
        for game in game_list:
            for player in game["players"]:
                national_id = player["national_id"]
                score_change = player["score"]
                for p in player_list:
                    if p["national_id"] == national_id:
                        p["score"] += score_change
        tournament_table.update({"player_list": player_list})

    def generate_pair_score(self, name_tournament):
        tournament_table = self.tournament.db_tournament.table(name_tournament)
        tournament_data = self.tournament.find_tournament(name_tournament)
        if tournament_data:
            player_list = tournament_data.get("player_list", [])
            sorted_players = sorted(player_list, key=lambda x: x["score"], reverse=True)
            tournament_table.update({"player_list": sorted_players})


class Report:
    def __init__(self):
        self.round = Round()
        self.tournament = Tournament()
        self.player = Player()
        self.RoundQuery = Query()
        self.PlayerQuery = Query()
        self.TournamentQuery = Query()

    def player_report(self):
        player_data = self.player.players.all()
        sorted_players = sorted(player_data, key=lambda x: x["name"])
        return sorted_players

    def export_players_to_file(self, data, file_path):
        with open(file_path, "w") as file:
            for item in data:
                file.write(f"{item}\n")
        print("Données exporté")

    def export_tournament_to_file(self, data, file_path):
        with open(file_path, "a") as file:
            file.write(str(data) + "\n")
        print("Données exportées avec succès.")

    def export_player_in_tournament(self, data, file_path, name_tournament):
        with open(file_path, "w") as file:
            file.write(f"Tournoi: {name_tournament}\n")
            for item in data:
                file.write(f"{item}\n")
        print("Données exportées avec succès.")

    def player_in_tournament_report(self, name_tournament):
        tournament_data = self.tournament.find_tournament(name_tournament)
        player_list = tournament_data.get("player_list", [])
        sorted_players = sorted(player_list, key=lambda x: x["name"])
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

    def round_report(self, name_tournament):
        tournament = self.round.db_rounds.table(
            name_tournament
        )  # Sélectionne la table correspondant au nom du tournoi
        rounds_info = tournament.all()

        report_list = []  # Initialisation d'une liste pour stocker le rapport

        for round_details in rounds_info:
            round_info = [
                name_tournament,
                round_details["round_index"],
                round_details["start_date"],
                round_details["end_date"],
            ]
            games_list = []  # Liste pour stocker les parties du round
            for game in round_details["game_list"]:
                game_info = [
                    game["game_id"]
                ]  # Liste pour stocker les informations sur la partie
                players_info = (
                    []
                )  # Liste pour stocker les informations sur les joueurs de la partie
                for player in game["players"]:
                    player_info = [
                        player["name"],
                        player["national_id"],
                        player["score"],
                    ]  # Liste pour stocker les informations sur le joueur
                    players_info.append(player_info)
                game_info.append(players_info)
                games_list.append(game_info)
            round_info.append(games_list)
            report_list.append(round_info)

        return report_list  # Retourne la liste contenant le rapport sur les rounds et les parties

    def export_round_to_file(self, data, file_path):
        with open(file_path, "w") as file:
            for round_info in data:
                file.write(f"Tournament Type: {round_info[0]}\n")
                file.write(f"Round Index: {round_info[1]}\n")
                file.write(f"Start Date: {round_info[2]}\n")
                file.write(f"End Date: {round_info[3]}\n")
                file.write("Game List:\n")
                for game_info in round_info[4]:
                    file.write(f"Game ID: {game_info[0]}\n")
                    for player_info in game_info[1]:
                        file.write(
                            f"Player: {player_info[0]}, National ID: {player_info[1]}, Score: {player_info[2]}\n"
                        )
                file.write("\n")
        print("Données exportées")
