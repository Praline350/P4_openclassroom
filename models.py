import json
from tinydb import TinyDB, Query
import os
from datetime import datetime, timedelta
import time
import random


JSON_DATA_PLAYERS_PATH = "data/data_players.json"
JSON_DATA_TOURNAMENTS_PATH = "data/data_tournaments.json"
JSON_DATA_ROUNDS_PATH = "data/data_rounds.json"


class Player:

    def __init__(self):
        self.db_player = TinyDB(JSON_DATA_PLAYERS_PATH)
        self.players = self.db_player.table("Players")
        if not os.path.exists(JSON_DATA_PLAYERS_PATH):
            with open(JSON_DATA_PLAYERS_PATH, "w") as f:
                json.dump([], f)
        self.PlayerQuery = Query()

    def write_player(self, surname, name, birth_date, national_id):
        self.data = {
            "surname": surname,
            "name": name,
            "birth_date": birth_date,
            "national_id": national_id,
        }
        self.players.insert(self.data)

    def find_player(self, national_id):
        player_data = self.players.search(self.PlayerQuery.national_id == national_id)
        if player_data:
            return player_data[0]
        else:
            return None


class Tournament:

    def __init__(self):
        self.player = Player()
        self.db_tournament = TinyDB(JSON_DATA_TOURNAMENTS_PATH)

        if not os.path.exists(JSON_DATA_TOURNAMENTS_PATH):
            with open(JSON_DATA_TOURNAMENTS_PATH, "w") as f:
                json.dump([], f)
        self.PlayerQuery = Query()
        self.TournamentQuery = Query()

    def write_tournament(
        self, name_tournament, localisation, round, start_date, end_date
    ):
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
        tournament_data = self.find_tournament(name_tournament)
        if tournament_data:
            self.db_tournament.remove(
                self.TournamentQuery.name_tournament == name_tournament
            )

    def add_player(self, name_tournament, id_player):
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
                    player_list.append({"national_id": national_id})
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
        tournament_table = self.db_tournament.table(name_tournament)
        tournament_data = tournament_table.all()
        if tournament_data:
            return tournament_data[0]  # Retourne le premier tournoi trouvé
        else:
            return None

    def get_name_tournaments(self):
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
        self.player = Player()
        self.RoundQuery = Query()
        self.PlayerQuery = Query()

    def make_game(
        self,
        name_tournament,
        round_index,
        id_player_one,
        id_player_two,
        score_p_one,
        score_p_two,
    ):
        self.round_index = round_index
        self.score_p_one = score_p_one
        self.score_p_two = score_p_two
        player_one = (id_player_one, score_p_one)
        player_two = (id_player_two, score_p_two)
        self.players = (player_one, player_two)
        return self.players
