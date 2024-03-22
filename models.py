import json
from tinydb import TinyDB, Query
import os
from datetime import datetime, timedelta
import time
import random

# Chemins vers les fichiers JSON de données

JSON_DATA_PLAYERS_PATH = "data/data_players.json"
JSON_DATA_TOURNAMENTS_PATH = "data/data_tournaments.json"
JSON_DATA_ROUNDS_PATH = "data/data_rounds.json"


class Player:

    def __init__(self):
        # Initialisation de la base de données des joueurs
        self.db_player = TinyDB(JSON_DATA_PLAYERS_PATH)
        self.players = self.db_player.table("Players")
        if not os.path.exists(JSON_DATA_PLAYERS_PATH):
            with open(JSON_DATA_PLAYERS_PATH, "w") as f:
                json.dump([], f)
        # Initialisation de la requête pour les joueurs
        self.PlayerQuery = Query()

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
        player_data = self.players.search(self.PlayerQuery.national_id == national_id)
        if player_data:
            return player_data[0]
        else:
            return None


class Tournament:

    def __init__(self):
        self.player = Player()
        # Initialisation de la base de données des tournois
        self.db_tournament = TinyDB(JSON_DATA_TOURNAMENTS_PATH)
        if not os.path.exists(JSON_DATA_TOURNAMENTS_PATH):
            with open(JSON_DATA_TOURNAMENTS_PATH, "w") as f:
                json.dump([], f)
        # Initialisation des requêtes pour les joueurs et les tournois
        self.PlayerQuery = Query()
        self.TournamentQuery = Query()

    def write_tournament(
        self, name_tournament, localisation, round, start_date, end_date
    ):
        # Écriture des données d'un tournoi dans la base de données
        self.tournaments = self.db_tournament.table(name_tournament)
        self.data = {
            "name_tournament": name_tournament,
            "localisation": localisation,
            "rounds_number": round,
            "rounds": [],
            "actual_round": 1,
            "start_date": start_date,
            "end_date": end_date,
            "player_list": [],
            "description": "",
        }
        self.tournaments.insert(self.data)

    def remove_tournament(self, name_tournament):
        # Suppression d'un tournoi de la base de données
        tournament_data = self.find_tournament(name_tournament)
        if tournament_data:
            self.db_tournament.remove(
                self.TournamentQuery.name_tournament == name_tournament
            )

    def add_player(self, name_tournament, id_player):
        # Ajout d'un joueur à un tournoi
        self.name_tournament = name_tournament
        self.id_player = id_player
        tournament_table = self.db_tournament.table(name_tournament)
        player_data = self.player.find_player(id_player)
        if player_data:
            player_name = player_data["name"]
            national_id = player_data["national_id"]
            tournament_data = self.find_tournament(name_tournament)
            if tournament_data:
                player_list = tournament_data.get("player_list", [])
                player_in_tournament = any(
                    player.get("national_id") == id_player for player in player_list
                )
                if not player_in_tournament:
                    player_list.append({"national_id": national_id, "score": 0})
                    tournament_table.update(
                        {"player_list": player_list},
                        self.TournamentQuery.name_tournament == name_tournament,
                    )
                    print(f"Joueur {player_name} ajouté")
                else:
                    print("Joueur déjà dans le tournoi")
        else:
            print("tournoi inexistant")

    def find_tournament(self, name_tournament):
        # Recherche d'un tournoi par son nom
        tournament_table = self.db_tournament.table(name_tournament)
        tournament_data = tournament_table.all()
        if tournament_data:
            return tournament_data[0]  # Retourne le premier tournoi trouvé
        else:
            return None

    def get_name_tournaments(self):
        # Récupération de la liste des noms de tournois
        return self.db_tournament.tables()


class Round:

    def __init__(self):
        self.tournament = Tournament()
        self.db_rounds = TinyDB(JSON_DATA_ROUNDS_PATH)

        if not os.path.exists(JSON_DATA_ROUNDS_PATH):
            with open(JSON_DATA_ROUNDS_PATH, "w") as f:
                json.dump([], f)
        self.RoundsQuery = Query()
        self.TournamentQuery = Query()

    def add_round(self, name_tournament):
        self.rounds = self.db_rounds.table(name_tournament)

        start_date = datetime.now()
        end_date = start_date + timedelta(hours=4)
        tournament_table = self.tournament.db_tournament.table(name_tournament)
        tournament_data = self.tournament.find_tournament(name_tournament)
        if tournament_data:
            tournament_round = tournament_data.get("rounds", [])
            round_index = len(tournament_round) + 1
            self.data = {
                "round_index": round_index,
                "start_date": start_date.strftime("%H:%M"),
                "end_date": end_date.strftime("%H:%M"),
                "game_list": [],
            }
            self.rounds.insert(self.data)
            tournament_round.append(self.data)
            tournament_table.update(
                {"rounds": tournament_round},
                self.TournamentQuery.name_tournament == name_tournament,
            )
        else:
            print("tournoi inexistant")

    def find_round(self, round_index, name_tournament):
        round_table = self.db_rounds.table(name_tournament)
        rounds = round_table.all()
        for round_data in rounds:
            if round_data.get("round_index") == round_index:
                return round_data
        return None

    def mix_players_random(self, name_tournament):
        tournament_data = self.tournament.find_tournament(name_tournament)
        if tournament_data:
            tournament_round = tournament_data.get("player_list", [])
            random.shuffle(tournament_round)
            self.tournament.tournaments.update(
                {"player_list": tournament_round},
                self.TournamentQuery.name_tournament == name_tournament,
            )

    def add_game(self, game):
        pass


class Game:
    def __init__(self):
        self.round = Round()
        self.tournament = Tournament()
        self.player = Player()
        self.RoundQuery = Query()
        self.PlayerQuery = Query()

    def make_game(self, name_tournament, round_index):
        self.round_index = round_index
        tournament_table = self.tournament.db_tournament.table(name_tournament)
        round_table = self.round.db_rounds.table(name_tournament)
        round_data = self.round.find_round(round_index, name_tournament)
        tournament_data = self.tournament.find_tournament(name_tournament)
        if tournament_data:
            player_list = tournament_data.get("player_list", [])
            num_players = len(player_list)
            if num_players % 2 != 0:
                print("nombre impaire")
                return
            game_id = 1
            for i in range(0, num_players, 2):
                player_pair = (player_list[i], player_list[i + 1])
                game_list = round_data.get("game_list", [])
                pair_already_in_game = False
                for match in game_list:
                    if (
                        player_pair[0] in match["players"]
                        or player_pair[1] in match["players"]
                    ):
                        pair_already_in_game = True
                        break
                if not pair_already_in_game:
                    game_data = {"game_id": game_id, "players": player_pair}
                    game_list.append(game_data)
                    round_table.update({"game_list": game_list}, doc_ids=[round_index])

                    game_id += 1
                else:
                    print("Un joueur est déjà présent dans la game_list")

    def play_game(self, name_tournament, round_index):
        round_table = self.round.db_rounds.table(name_tournament)
        round_data = self.round.find_round(round_index, name_tournament)
        if round_data:
            game_list = round_data.get("game_list", [])
            if game_list:
                for game in game_list:
                    win_pourcentage = 0.3
                    result = random.random()
                    if result > win_pourcentage:
                        winner = random.choice(game["players"])
                        winner_index = game["players"].index(winner)
                        game["players"][winner_index]["score"] += 1
                        print(f"{winner} à gagner")
                    else:
                        for player in game["players"]:
                            player["score"] += 0.5
                        print("match nul")
                round_table.update({"game_list": game_list})


round_index = 1
name_tournament = "tournoi eliminatoire"
game = Game()
game.play_game(name_tournament, round_index)
