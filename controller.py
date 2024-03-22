from models import Player, Tournament, Round

from view import PromptForm, Menu
import os
import sys
from tinydb import TinyDB, Query

JSON_DATA_PLAYERS_PATH = "data/data_players.json"
JSON_DATA_TOURNAMENTS_PATH = "data/data_tournaments.json"


class Controller:
    def __init__(self):
        self.form = PromptForm()
        self.menu = Menu()
        self.player = Player()
        self.tournament = Tournament()
        self.round = Round()

    def menu_choice(self):
        while True:
            user_input = self.menu.menu_index()
            match user_input:
                case "Menu joueur":
                    self.menu_player_choice()
                case "Menu tournois":
                    self.menu_tournament_choice()
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
                    tournament_list = self.tournament.get_name_tournaments()
                    name_tournament, id_player = self.form.tournament_add_player(
                        tournament_list
                    )
                    self.tournament.add_player(name_tournament, id_player)
                    pass
                case "Ajouter un round au tournoi":
                    tournament_list = self.tournament.get_name_tournaments()
                    name_tournament = self.form.tournament_add_round(tournament_list)
                    self.round.add_round(name_tournament)
                case "Supprimer un tournoi":
                    tournament_list = self.tournament.get_name_tournaments()
                    name_tournament = self.form.prompt_for_remove_tournament(tournament_list)
                    self.tournament.remove_tournament(name_tournament)
                    print(f"{name_tournament} Supprimé")

                case "Retour":
                    break
                case "Sortir":
                    sys.exit()
                case _:
                    print("Choix invalide")
