from models import Player, DataJson, Tournament

from view import PromptForm, Menu
import os
import sys


class Controller:
    def __init__(self):
        self.data_json = DataJson()
        self.form = PromptForm()
        self.menu = Menu()
        self.player = Player()
        self.tournament = Tournament()

    def menu_choice(self):
        while True:
            user_input = self.menu.menu_index()
            match user_input:
                case "1":
                    self.menu_player_choice()
                case "2":
                    self.menu_tournament_choice()
                case "4":
                    pass
                case "5":
                    sys.exit()
                case _:
                    print("Choix invalide")

    def menu_player_choice(self):
        while True:
            user_input = self.menu.menu_player()
            match user_input:
                case "1":
                    surname, name, birth_date, national_id = (
                        self.form.prompt_for_add_player()
                    )
                    self.player.write_player(surname, name, birth_date, national_id)
                    pass
                case "4":
                    pass
                case "5":
                    sys.exit()
                case _:
                    print("Choix invalide")

    def menu_tournament_choice(self):
        while True:
            user_input = self.menu.menu_tournament()
            match user_input:
                case "1":
                    name_tournament, localisation, round, start_date, end_date = (
                        self.form.prompt_for_add_tournament()
                    )
                    self.tournament.write_tournament(
                        name_tournament, localisation, round, start_date, end_date
                    )
                    break
                case "2":
                    name_tournament, id_player = self.form.tournament_add_player()
                    self.tournament.add_player(name_tournament, id_player)
                    break
                case "4":
                    pass
                case "5":
                    sys.exit()
                case _:
                    print("Choix invalide")
