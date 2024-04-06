from .validator import Validator
import questionary


class Menu:

    def __init__(self):
        self.validator = Validator()

    def menu_index(self):
        user_input = 0
        user_input = questionary.select(
            "------MENU------",
            choices=[
                "Menu joueur",
                "Menu tournois",
                "Jouer un tournoi",
                "Rapports",
                "Sortir",
            ],
        ).ask()
        print(user_input)
        return user_input

    def menu_player(self):
        user_input = 0
        user_input = questionary.select(
            "------MENU JOUEUR-----",
            choices=[
                "Ajouter un joueur",
                "Supprimer un joueur",
                "Retour",
                "Sortir"
                ]
        ).ask()
        print(user_input)
        return user_input

    def menu_tournament(self):
        user_input = 0
        user_input = questionary.select(
            "------MENU TOURNOIS-----",
            choices=[
                "Ajouter un tournois",
                "Ajouter un joueur au tournoi",
                "Supprimer un joueur du tournoi",
                "Supprimer un tournoi",
                "Ajouter une description",
                "Retour",
                "Sortir",
            ],
        ).ask()
        return user_input

    def menu_begin_tournament(self, tournament_list):
        name_tournament = questionary.select(
            "-----Quel tournoi ? -----", choices=tournament_list
        ).ask()

        return name_tournament

    def menu_report(self):
        user_input = questionary.select(
            "----Quel rapport voulez vous ? ----",
            choices=[
                "Liste de tous les joueurs",
                "Informations tournoi",
                "Liste des joueurs dans un tournoi",
                "Liste des tours et matchs d'un tournoi",
                "Retour",
                "Sortir",
            ],
        ).ask()

        return user_input
