from .validator import Validator
import questionary


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
        end_date = self.validator.validate_date(
            "Entrez la date de fin (JJ-MM-AAAA) : "
            )

        return name_tournament, localisation, round, start_date, end_date

    def tournament_add_player(self):
        print("---AJOUTER UN JOUEUR A UN TOURNOI---")

        id_player = self.validator.validate_national_id(
            "Entrez l'ID National du joueur : "
        )

        return id_player

    def prompt_for_id_list(self, players_ids):
        id_player = questionary.select("Liste des joueurs",
                                       choices=players_ids
                                       ).ask()
        return id_player

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
            "quel tournoi ?", choices=tournament_list
        ).ask()
        return name_tournament
