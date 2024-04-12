from .player import Player
from .tournament import Tournament
from .round import Round
from tinydb import Query
from datetime import datetime
import random


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
            game_list = round_data.get("game_list", [])  # type: ignore
            player_list = tournament_data.get("player_list", [])
            num_players = len(player_list)
            # Vérifie que les joueurs sont bien un nombre pair
            if num_players % 2 != 0:
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
                if not pair_already_in_game:
                    game_list.append(
                        {"game_id": game_id, "players": player_pair}
                        )
            round_table.update(
                {"game_list": game_list}, Query().round_index == round_index
            )

    def play_game(self, name_tournament, round_index):
        round_table = self.tournament.db_tournament.table("rounds")
        round_data = self.round.find_round(name_tournament, round_index)
        result_list = []
        if round_data:
            game_list = round_data.get("game_list", [])  # type: ignore
            if game_list:
                for game in game_list:
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
                            {"game_list": game_list},
                            Query().round_index == round_index
                        )
                        result_list.append(
                            ("win", winner['name'], looser['name'])
                            )
                    else:
                        for player in game["players"]:
                            player["score"] = 0.5
                        round_table.update(
                            {"game_list": game_list},
                            Query().round_index == round_index
                        )
                        player1_name = game['players'][0]['name']
                        player2_name = game['players'][1]['name']
                        result_list.append(
                            ("draw", player1_name, player2_name)
                            )
        return result_list

    def get_game_player(self, name_tournament, round_index):
        round_data = self.round.find_round(name_tournament, round_index)
        players_list = []
        game_list = round_data.get("game_list", [])  # type: ignore
        for game in game_list:
            for player in game['players']:
                player["score"] = 0
            players_list.append(
                (game['players'][0]['name'], game['players'][1]['name'])
                )
        return players_list

    def update_scores(self, name_tournament, round_index, results):
        self.tournament.initialize_db(name_tournament)
        round_table = self.tournament.db_tournament.table("rounds")
        round_data = self.round.find_round(name_tournament, round_index)
        if round_data:
            game_list = round_data.get("game_list", [])  # type: ignore
            if game_list:
                for game, result in zip(game_list, results):
                    for player in game["players"]:
                        player["score"] = 0

                    if result != "Match nul":
                        winner_name = result
                        for player in game["players"]:
                            if player["name"] == winner_name:
                                player["score"] += 1
                    else:
                        for player in game["players"]:
                            player["score"] += 0.5

                # Mettre à jour la base de données avec les scores mis à jour
                round_table.update({"game_list": game_list},
                                   Query().round_index == round_index)

    def get_num_game(self, name_tournament, round_index):
        round_data = self.round.find_round(name_tournament, round_index)
        if round_data:
            game_list = round_data.get('game_list', [])  # type: ignore
            return len(game_list)

    def end_game(self, name_tournament, round_index):
        self.tournament.initialize_db(name_tournament)
        tournament_data = self.tournament.find_tournament(name_tournament)
        round_data = self.round.find_round(name_tournament, round_index)
        player_list = tournament_data.get("player_list", [])  # type: ignore
        game_list = round_data.get("game_list", [])  # type: ignore
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
            sorted_players = sorted(
                player_list, key=lambda x: x["score"], reverse=True
                )
            self.tournament.tournament.update({"player_list": sorted_players})


if __name__ == "__main__":
    pass
