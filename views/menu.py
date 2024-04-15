from .validator import Validator
import questionary


class Menu:

    def __init__(self):
        self.validator = Validator()

    def menu_index(self):
        """Choix utilisateur du menu principal"""

        user_input = 0
        user_input = questionary.select(
            "------MENU------",
            choices=[
                "Menu joueur",
                "Menu tournois",
                "Jouer un tournoi",
                "Jouer un tournoi d'une sauvegarde",
                "Rapports",
                "Sortir",
            ],
        ).ask()
        return user_input

    def menu_player(self):
        """Choix utilisateur du menu Joueur"""

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
        return user_input

    def menu_tournament(self):
        """Choix utilisateur du menu tournoi"""

        user_input = 0
        user_input = questionary.select(
            "------MENU TOURNOIS-----",
            choices=[
                "Ajouter un tournois",
                "Ajouter un joueur au tournoi",
                "Supprimer un joueur du tournoi",
                "Supprimer un tournoi",
                "Ajouter une description",
                "Faire une sauvegarde du tournoi",
                "Retour",
                "Sortir",
            ],
        ).ask()
        return user_input

    def menu_begin_tournament(self, tournament_list):
        """Permet de selectionné un tournoi dans la liste des tournoi"""

        name_tournament = questionary.select(
            "-----Quel tournoi ? -----", choices=tournament_list
        ).ask()

        return name_tournament

    def menu_report(self):
        """Choix utilisateur du menu rapports"""

        user_input = questionary.select(
            "----Quel rapport voulez vous ? ----",
            choices=[
                "Liste de tous les joueurs",
                "Informations tournoi",
                "Liste des joueurs dans un tournoi",
                "Liste des tours et matchs d'un tournoi",
                "Rapport complet d'un tournoi",
                "Retour",
                "Sortir",
            ],
        ).ask()

        return user_input
