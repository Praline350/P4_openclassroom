import re
import questionary


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
                    "Format d'ID national invalide."
                    "Veuillez entrer 2 lettres suivies de 5 chiffres."
                )

    def validate_int(self, prompt):
        while True:
            user_input = questionary.text(prompt).ask()
            if not user_input.isdigit():
                print("L'entrée doit être un chiffre")
            else:
                return user_input