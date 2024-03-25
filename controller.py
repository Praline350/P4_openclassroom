from models import Player, Tournament, Round, Game

from view import PromptForm, Menu
import os
import sys
from tinydb import TinyDB, Query
import time

JSON_DATA_PLAYERS_PATH = "data/data_players.json"
JSON_DATA_TOURNAMENTS_PATH = "data/data_tournaments.json"


class Controller:
    def __init__(self):
        self.form = PromptForm()
        self.menu = Menu()
        self.player = Player()
        self.tournament = Tournament()
        self.round = Round()
        self.game = Game()

    def menu_choice(self):
        while True:
            user_input = self.menu.menu_index()
            match user_input:
                case "Menu joueur":
                    self.menu_player_choice()
                case "Menu tournois":
                    self.menu_tournament_choice()
                case "Commencer un tournoi":
                    self.begin_tournament()
                case "Sortir":
                    sys.exit()
                case _:
                    print("Choix invalide")

    def menu_player_choice(self):
        while True:
            user_input = self.menu.menu_player()
            match user_input:
                case "Ajouter un joueur":
                    surname, name, birth_date, national_id = (
                        self.form.prompt_for_add_player()
                    )
                    self.player.write_player(surname, name, birth_date, national_id)
                    pass
                case "Retour":
                    break
                case "Sortir":
                    sys.exit()
                case _:
                    print("Choix invalide")

    def menu_tournament_choice(self):
        while True:

            user_input = self.menu.menu_tournament()
            match user_input:
                case "Ajouter un tournois":
                    name_tournament, localisation, round, start_date, end_date = (
                        self.form.prompt_for_add_tournament()
                    )
                    self.tournament.write_tournament(
                        name_tournament, localisation, round, start_date, end_date
                    )
                    break
                case "Ajouter un joueur au tournoi":
                    while True:
                        tournament_list = self.tournament.get_name_tournaments()
                        name_tournament, id_player = self.form.tournament_add_player(
                            tournament_list
                        )
                        self.tournament.add_player(name_tournament, id_player)
                        user_input = self.form.prompt_continue_add()
                        if user_input == "YES":
                            pass
                        if user_input == "NO":
                            break
                case "Supprimer un joueur du tournoi":
                    tournament_list = self.tournament.get_name_tournaments()
                    name_tournament, id_player = self.form.prompt_for_remove_player(
                        name_tournament, id_player
                    )
                    print(f'{id_player} enlevé du tournoi "{name_tournament}"')
                case "Ajouter un round au tournoi":
                    tournament_list = self.tournament.get_name_tournaments()
                    name_tournament = self.form.tournament_add_round(tournament_list)
                    self.round.add_round(name_tournament)
                case "Supprimer un tournoi":
                    tournament_list = self.tournament.get_name_tournaments()
                    name_tournament = self.form.prompt_for_remove_tournament(
                        tournament_list
                    )
                    self.tournament.remove_tournament(name_tournament)
                    print(f"{name_tournament} Supprimé")

                case "Retour":
                    break
                case "Sortir":
                    sys.exit()
                case _:
                    print("Choix invalide")

    def begin_tournament(self):
        while True:
            tournament_list = self.tournament.get_name_tournaments()
            name_tournament = self.menu.menu_begin_tournament(tournament_list)
            round_index = 1
            actual_round = 1
            self.round.add_round(name_tournament)
            self.play_round(name_tournament, round_index, actual_round)

    def play_round(self, name_tournament, round_index, actual_round):
        while True:
            self.game.make_game(name_tournament, round_index)
            print(f"----DEBUT ROUND {actual_round}-----")
            self.game.play_game(name_tournament, round_index)
            self.game.end_game(name_tournament, round_index)
            self.game.generate_pair_score(name_tournament)
            round_index = self.round.add_round(name_tournament)
            user_input = self.form.prompt_continue_tournament()
            actual_round += 1
            if user_input == "YES":
                pass
            if user_input == "No":
                break

            if actual_round ==5:
                print("Tounrnoi terminer")
                tournament_data = self.tournament.find_tournament(name_tournament)
                if tournament_data:
                    player_list = tournament_data.get("player_list", [])
                    sorted_players = sorted(
                        player_list, key=lambda x: x["score"], reverse=True
                    )
                    winner = sorted_players[0]
                    for player in player_list:
                        print(
                            f'Joueur {player["name"]}: Score {player["score"]}'
                        )
                    print(f"LE GAGNANT EST {winner['name']} avec {winner['score']} points, BRAVO !")
                    time.sleep(0.5)
                    self.menu_choice()
