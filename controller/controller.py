from views.menu import Menu
from views.prompt_form import PromptForm
from views.display_message import DisplayMessage
from .controller_game import ControllerGame
import sys
from .controller_menu import ControllerMenu
from models.player import Player


class ControllerManager:
    def __init__(self):
        self.form = PromptForm()
        self.menu = Menu()
        self.controller = ControllerMenu()
        self.controller_game = ControllerGame()
        self.player = Player()
        self.diplay = DisplayMessage()

    def menu_choice(self):
        name = self.player.check_birday()
        if name:
            self.diplay.display_birthday(name)
        while True:
            user_input = self.menu.menu_index()
            match user_input:
                case "Menu joueur":
                    self.menu_player_choice()
                case "Menu tournois":
                    self.menu_tournament_choice()
                case "Jouer un tournoi":
                    self.controller_game.begin_tournament()
                case "Rapports":
                    self.menu_report_choice()
                case "Sortir":
                    sys.exit()
                case _:
                    print("Choix invalide")

    def menu_report_choice(self):
        while True:
            user_input = self.menu.menu_report()
            match user_input:
                case "Liste de tous les joueurs":
                    self.controller.menu_report_player()
                case "Informations tournoi":
                    self.controller.menu_report_tournament()
                case "Liste des joueurs dans un tournoi":
                    self.controller.menu_report_player_in_tournament()
                case "Liste des tours et matchs d'un tournoi":
                    self.controller.menu_report_round()
                case "Retour":
                    break
                case "Sortir":
                    sys.exit()
                case _:
                    print("Choix invalide")

    def menu_player_choice(self):
        while True:
            user_input = self.menu.menu_player()
            match user_input:
                case "Ajouter un joueur":
                    self.controller.menu_add_player()
                case "Supprimer un joueur":
                    self.controller.menu_remove_player()
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
                    self.controller.menu_add_tournament()
                case "Ajouter un joueur au tournoi":
                    self.controller.menu_add_player_in_tournament()
                case "Supprimer un joueur du tournoi":
                    self.controller.menu_remove_player_in_tournament()
                case "Supprimer un tournoi":
                    self.controller.menu_remove_tournament()
                case "Faire une sauvegarde du tournoi":
                    self.controller.menu_save_tournament()
                case "Ajouter une description":
                    self.controller.menu_add_description()
                case "Retour":
                    break
                case "Sortir":
                    sys.exit()
                case _:
                    print("Choix invalide")
