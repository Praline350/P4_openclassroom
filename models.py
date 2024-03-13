import json
from tinydb import TinyDB, Query
import os
from datetime import datetime, timedelta
import time

JSON_DATA_PLAYERS_PATH = "data/data_players.json"
JSON_DATA_TOURNAMENTS_PATH = "data/data_tournaments.json"


"""class DataJson:
    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data")
            os.makedirs(JSON_DATA_PLAYERS_PATH)
            os.makedirs(JSON_DATA_TOURNAMENTS_PATH)

    def read_data(self, file_path):
        self.file_path = file_path
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r") as json_file:
                return json.load(json_file)
        else:
            pass

    def write_data(self, data, file_path):
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
"""


class Player:

    def __init__(self):
        self.db_player = TinyDB(JSON_DATA_PLAYERS_PATH)
        self.players = self.db_player.table("Players")
        if not os.path.exists(JSON_DATA_PLAYERS_PATH):
            with open(JSON_DATA_PLAYERS_PATH, "w") as f:
                json.dump([], f)

    def write_player(self, surname, name, birth_date, national_id):
        self.data = {
            "surname": surname,
            "name": name,
            "birth_date": birth_date,
            "national_id": national_id,
        }
        self.players.insert(self.data)

    def find_player(self, national_id):
        PlayerQuery = Query()
        player_data = self.players.search(PlayerQuery.national_id == national_id)
        if player_data:
            return player_data[0]
        else:
            return None


class Tournament:

    def __init__(self):
        self.player = Player()
        self.db_tournament = TinyDB(JSON_DATA_TOURNAMENTS_PATH)
        self.tournaments = self.db_tournament.table("Tournois")
        if not os.path.exists(JSON_DATA_TOURNAMENTS_PATH):
            with open(JSON_DATA_TOURNAMENTS_PATH, "w") as f:
                json.dump([], f)

    def write_tournament(
        self, name_tournament, localisation, round, start_date, end_date
    ):
        self.data = {
            "Nom du tournoi": str(name_tournament),
            "localisation": localisation,
            "Nombre de tours": round,
            "Debut du tournoi": start_date,
            "Fin du tournoi": end_date,
            "Liste des joueurs": [],
        }
        self.tournaments.insert(self.data)

    def add_player(self, name_tournament, id_player):
        self.name_tournament = name_tournament
        file_path = (
            f"{JSON_DATA_TOURNAMENTS_PATH}\{name_tournament}\{name_tournament}.json"
        )
        self.id_player = id_player
        player_data = self.player.find_player(self.id_player)
        if player_data:
            self.name = player_data["name"]
            self.surname = player_data["surname"]
            player = (self.name, self.surname)
        tournament_data = self.data_json.read_data(file_path)
        if tournament_data:
            tournament_data["Liste des joueurs"].append(player)
            self.data_json.write_data(tournament_data, file_path)


class Round:

    def __init__(self, name_round):
        start_date = datetime.now()
        self.name_round = name_round
        self.start_date = start_date.strftime("%H:%M")
        self.end_date = start_date + timedelta(hours=4)
        self.game_list = []

    def add_game(self, game):
        self.game = game
        self.game_list.append(game)


class Game:
    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.players = (self.player_one, self.player_two)
