from .tournament import Tournament
from .player import Player
from datetime import datetime
from tinydb import Query
import random


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
            {"actual_round": actual_round},
            Query().name_tournament == name_tournament
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
