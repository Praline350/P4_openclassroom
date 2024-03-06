import json
import os
import tkinter as tk


JSON_DATA_PLAYERS_PATH = "data\data_players.json"


class PlayerForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Player Form")

        # Frame principal
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20)

        # Labels et Entrées
        tk.Label(self.main_frame, text="Nom :").grid(row=0, column=0, sticky="w")
        self.surname_entry = tk.Entry(self.main_frame)
        self.surname_entry.grid(row=0, column=1)

        tk.Label(self.main_frame, text="Prénom :").grid(row=1, column=0, sticky="w")
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self.main_frame, text="Date de naissance :").grid(
            row=2, column=0, sticky="w"
        )
        self.birth_date_entry = tk.Entry(self.main_frame)
        self.birth_date_entry.grid(row=2, column=1)

        tk.Label(self.main_frame, text="IDN :").grid(row=3, column=0, sticky="w")
        self.national_id_entry = tk.Entry(self.main_frame)
        self.national_id_entry.grid(row=3, column=1)

        # Bouton pour soumettre les données
        self.submit_button = tk.Button(
            self.main_frame, text="Soumettre", command=self.submit_data
        )
        self.submit_button.grid(row=4, columnspan=2, pady=10)

    def submit_data(self):
        surname = self.surname_entry.get()
        name = self.name_entry.get()
        birth_date = self.birth_date_entry.get()
        national_id = self.national_id_entry.get()

        player = Player(surname, name, birth_date, national_id)
        player.inscription()

        self.root.destroy()


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
            os.path.exists(JSON_DATA_PLAYERS_PATH)
            and os.path.getsize(JSON_DATA_PLAYERS_PATH) > 0
        ):
            # Lire les données JSON existantes depuis le fichier
            with open(JSON_DATA_PLAYERS_PATH, "r") as json_file:
                data_players = json.load(json_file)
        else:
            # Sinon créer le fichier Json et le dictionnaire players
            with open(JSON_DATA_PLAYERS_PATH, "w") as json_file:
                pass
            data_players = {"players": []}
        # Ajoute les information dans le dictionnaire players et l'ecrit dans le fichier json
        data_players["players"].append(self.to_dictionnary())
        with open(JSON_DATA_PLAYERS_PATH, "w") as json_data:
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
