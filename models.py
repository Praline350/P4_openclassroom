import json
import pprint
import os

JSON_DATA_PLAYERS_PATH = "data\data_players.json"


class DataJson:
    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data")
            os.makedirs("data\data_players")
            os.makedirs("data\data_tournaments")

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


class Player:

    def __init__(self, surname, name, birth_date, national_id):
        """Initialise un joueur avec ses information personnelle"""
        self.data_json = DataJson()
        self.data = {
            "surname": surname,
            "name": name,
            "birth_date": birth_date,
            "national_id": national_id,
        }

    def add_player(self, surname, name):
        file_path = f"data\data_players\{surname}_{name}.json"
        self.data_json.write_data(self.data, file_path)


class Tournament:

    def __init__(self, name_tournament, localisation, round, date):
        self.data_json = DataJson()
        self.data = {
            "name_tournament": name_tournament,
            "localisation": localisation,
            "rounds": round,
            "date": date,
        }

    def add_tournament(self, name_tournament, date):
        file_path = f"data\data_tournaments\{name_tournament}_{date}.json"
        self.data_json.write_data(self.data, file_path)

    def inscription(self, player):
        self.player = player


class Round:

    def __init__(self, name_round, player, score):
        self.name_round = name_round
        self.player = player
        self.score = score


class Game:
    pass
