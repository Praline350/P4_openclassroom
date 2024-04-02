import re
from tkinter import Tk
import os
import questionary
from models import Tournament

JSON_DATA_PLAYERS_PATH = "data\data_players.json"
JSON_DATA_TOURNAMENTS_PATH = "data\data_tournaments.json"


class Validator:

    def validate_input_str(self, prompt):
        while True:
            user_input = questionary.text(prompt).ask()
            if not user_input.replace(
                " ",
                "",
            ).isalpha():
                print("Doit contenir seulement des lettres")
            else:
                user_input = user_input.lower()
                return user_input

    def validate_date(self, prompt):
        pattern = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$"

        while True:
            user_input = questionary.text(prompt).ask()
            if re.match(pattern, user_input):
                return user_input
            else:
                print("Format invalide = > (JJ-MM-AAAA)")

    def validate_national_id(self, prompt):
        while True:
            user_input = questionary.text(prompt).ask()
            if (
                len(user_input) == 7
                and user_input[:2].isalpha()
                and user_input[2:].isdigit()
            ):
                user_input = user_input[:2].upper() + user_input[2:]
                return user_input
            else:
                print(
                    "Format d'ID national invalide. Veuillez entrer 2 lettres suivies de 5 chiffres."
                )

    def validate_int(self, prompt):
        while True:
            user_input = questionary.text(prompt).ask()
            if not user_input.isdigit():
                print("L'entrée doit être un chiffre")
            else:
                return user_input


class PromptForm:

    def __init__(self):
        self.validator = Validator()
        self.tournament = Tournament()

    def prompt_for_add_player(self):
        print("------AJOUTER UN JOUEUR------")

        surname = self.validator.validate_input_str("Entrez le nom : ")
        name = self.validator.validate_input_str("Entrez le prénom : ")
        birth_date = self.validator.validate_date(
            "Entrez la date de naissance (JJ-MM-AAAA): "
        )
        national_id = self.validator.validate_national_id("Entrez l'IDN : ")

        return surname, name, birth_date, national_id

    def prompt_for_add_tournament(self):
        print("------AJOUTER UN TOURNOIS------")

        name_tournament = self.validator.validate_input_str(
            "Entrez le nom du tournoi : "
        )
        localisation = self.validator.validate_input_str(
            "Entrez la localisation du tournoi : "
        )
        round = 4
        start_date = self.validator.validate_date(
            "Entrez la date de début (JJ-MM-AAAA) : "
        )
        end_date = self.validator.validate_date("Entrez la date de fin (JJ-MM-AAAA) : ")

        return name_tournament, localisation, round, start_date, end_date

    def tournament_add_player(self, tournament_list):
        print("---AJOUTER UN JOUEUR A UN TOURNOI---")

        name_tournament = questionary.select(
            "Quel Tournoi ?", choices=tournament_list
        ).ask()
        id_player = self.validator.validate_national_id(
            "Entrez l'ID National du joueur : "
        )

        return name_tournament, id_player

    def tournament_add_round(self, tournament_list):
        print("-----AJOUTER UN ROUND AU TOURNOI-----")
        name_tournament = questionary.select(
            "Quel tournoi ?", choices=tournament_list
        ).ask()
        return name_tournament

    def prompt_for_remove_tournament(self, tournament_list):
        print("-----SUPPRIMER UN TOURNOI-----")
        name_tournament = questionary.select(
            "Quel tournoi supprimé ?", choices=tournament_list
        ).ask()
        return name_tournament

    def prompt_continue_tournament(self):
        print("---Tournoi en cours---")
        user_input = questionary.select(
            "Passer au prochain Round ?", choices=["YES", "NO"]
        ).ask()
        return user_input

    def prompt_for_remove_player(self, tournament_list):
        print("-----Supprimer un joueur du tournoi-----")

        name_tournament = questionary.select(
            "De quel tournoi ?", choices=tournament_list
        ).ask()
        id_player = self.validator.validate_national_id(
            "Entrez l'ID du joueur à supprimé : "
        )
        return name_tournament, id_player

    def prompt_continue_add(self):
        user_input = questionary.select(
            "Ajouter un autre ?", choices=["YES", "NO"]
        ).ask()
        return user_input

    def prompt_export(self):
        user_input = questionary.select(
            "Voulez-vous exporter les fichier ?", choices=["YES", "NO"]
        ).ask()
        return user_input
    
    def prompt_data_tournament(self, tournament_list):
        name_tournament = questionary.select(
            "Info de quel tournoi ?",
            choices=tournament_list
        ).ask()
        return name_tournament
    
        

    

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
                "Commencer un tournoi",
                "Rapports",
                "Sortir",
            ],
        ).ask()
        print(user_input)
        return user_input

    def menu_player(self):
        user_input = 0
        user_input = questionary.select(
            "------MENU JOUEUR-----", choices=["Ajouter un joueur", "Retour", "Sortir"]
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
                "Ajouter un round au tournoi",
                "Supprimer un tournoi",
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
                "Liste de tous les tournois",
                "Liste des joueur dans le tournoi",
                "Liste des tour et matchs d'un tournoi",
                "Retour",
                "Sortir",
            ],
        ).ask()

        return user_input
