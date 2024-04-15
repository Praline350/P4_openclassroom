import questionary
from datetime import datetime


class Validator:

    def validate_input_str(self, prompt):
        """Validateur entrée avec seulement des lettres"""

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
        """Validateur pour entrées date correct"""

        while True:
            user_input = questionary.text(prompt).ask()
            try:
                datetime.strptime(user_input, '%d-%m-%Y')
                return user_input
            except ValueError:
                print("Format invalide => (JJ-MM-AAAA)")

    def validate_national_id(self, prompt):
        """Validateur pour le format de L'ID"""

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
                    "Format d'ID national invalide."
                    "Veuillez entrer 2 lettres suivies de 5 chiffres."
                )

    def validate_id_or_list(self, prompt):
        """validateur pour le format ID, retourne False si aucune entrées"""
        while True:
            user_input = questionary.text(prompt).ask()
            if len(user_input) == 0:
                return False
            elif (
                len(user_input) == 7
                and user_input[:2].isalpha()
                and user_input[2:].isdigit()
            ):
                user_input = user_input[:2].upper() + user_input[2:]
                return user_input
            else:
                print(
                    "Format d'ID national invalide."
                    "Veuillez entrer 2 lettres suivies de 5 chiffres."
                )

    def validate_int(self, prompt):
        """Validateur pour entrée seulement des chiffres"""

        while True:
            user_input = questionary.text(prompt).ask()
            if not user_input.isdigit():
                print("L'entrée doit être un chiffre")
            else:
                return user_input
