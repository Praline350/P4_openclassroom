import re
from tkinter import Tk
import os


class Validator:

    def validate_input_str(self, prompt):
        while True:
            user_input = input(prompt)
            if not user_input.replace(
                " ",
                "",
            ).isalpha():
                print("Doit contenir seulement des lettres")
            else:
                return user_input

    def validate_date(self, prompt):
        pattern = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$"

        while True:
            user_input = input(prompt)
            if re.match(pattern, user_input):
                return user_input
            else:
                print("Format invalide = > (JJ-MM-AAAA)")

    def validate_national_id(self, prompt):
        while True:
            user_input = input(prompt)
            if (
                len(user_input) == 7
                and user_input[:2].isalpha()
                and user_input[2:].isdigit()
            ):
                return user_input
            else:
                print(
                    "Format d'ID national invalide. Veuillez entrer 2 lettres suivies de 5 chiffres."
                )

    def validate_int(self, prompt):
        while True:
            user_input = input(prompt)
            if not user_input.isdigit():
                print("L'entrée doit être un chiffre")
            else:
                return user_input


class PromptForm:

    def __init__(self):
        self.validator = Validator()

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
    
    def tournament_add_player(self):
        print('---AJOUTER UN JOUEUR A UN TOURNOI---')
        for tournament in os.listdir('data\data_tournaments'):
            print(tournament)
        name_tournament = self.validator.validate_input_str("Entrez le nom du tournoi(sans la date) : ")
        id_player = self.validator.validate_national_id("Entrez l'ID National du joueur : ")

        return name_tournament, id_player


class Menu:

    def __init__(self):
        self.validator = Validator()

    def menu_index(self):
        user_input = 0
        print("------MENU------\nMenu Joueurs : 1 \nMenu Tournois : 2 \nSORTIR : 5")
        user_input = self.validator.validate_int("Votre choix : ")
        return user_input

    def menu_player(self):
        user_input = 0
        print("------MENU JOUEUR-----\nAjouter un joueur : 1 \nRetour : 4 \nSORTIR : 5")
        user_input = self.validator.validate_int("Votre choix : ")
        return user_input

    def menu_tournament(self):
        user_input = 0
        print(
            "------MENU TOURNOIS-----\nAjouter un tournois : 1 \nAjouter un joueur au tournoi : 2 \nRetour : 4 \nSORTIR : 5"
        )
        user_input = self.validator.validate_int("Votre choix : ")
        return user_input
