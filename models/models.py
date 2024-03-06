import json
import pprint
import os

JSON_DATA_FILE_PATH = "D:\openclassroom\projets\Projet 4\programmation\data.json"


class Player:

    def __init__(self, surname, name, birth_date, national_id):
        """Initialise un joueur avec ses information personnelle"""
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.national_id = national_id

    def to_dictionnary(self):
        """Retourne les infos du joueur dans un dictionnaire"""

        return {
            "surname": self.surname,
            "name": self.name,
            "birth_date": self.birth_date,
            "national_id": self.national_id,
        }

    def inscription(self):
        if (
            os.path.exists(JSON_DATA_FILE_PATH)
            and os.path.getsize(JSON_DATA_FILE_PATH) > 0
        ):
            # Lire les données JSON existantes depuis le fichier
            with open(JSON_DATA_FILE_PATH, "r") as json_file:
                data_players = json.load(json_file)
        else:
            # Sinon créer le fichier Json et le dictionnaire players
            with open(JSON_DATA_FILE_PATH, "w") as json_file:
                pass
            data_players = {"players": []}
        # Ajoute les information dans le dictionnaire players et l'ecrit dans le fichier json
        data_players["players"].append(self.to_dictionnary())
        with open(JSON_DATA_FILE_PATH, "w") as json_data:
            json.dump(data_players, json_data, indent=4)


class Tournament:

    def __init__(self, name_tournament, localisation, round, players):
        self.name_tournament = name_tournament
        self.localisation = localisation
        self.round = round
        self.players = players


class Round:

    def __init__(self, name_round, player, score):
        self.name_round = name_round
        self.player = player
        self.score = score


class Game:
    pass
