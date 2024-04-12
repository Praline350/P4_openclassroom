from .validator import Validator
import questionary
from questionary import Choice


class PromptForm:

    def __init__(self):
        self.validator = Validator()
        self.retour = Choice(title="retour")

    def prompt_national_id(self):
        national_id = self.validator.validate_national_id("Entrez l'IDN : ")
        return national_id

    def prompt_for_add_player(self):
        print("------AJOUTER UN JOUEUR------")

        surname = self.validator.validate_input_str("Entrez le nom : ")
        name = self.validator.validate_input_str("Entrez le prénom : ")
        birth_date = self.validator.validate_date(
            "Entrez la date de naissance (JJ-MM-AAAA): "
        )

        return surname, name, birth_date

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

    def prompt_for_add_description(self):
        description = questionary.text("Ajouter une description ?").ask()
        return description

    def prompt_for_begin_tournament(self):
        user_input = questionary.select(
            "Débuter le tournoi ou reprendre une sauvegarde ?",
            choices=["Commencer le tournoi", "Backup", "Retour"],
        ).ask()
        return user_input

    def prompt_for_backup(self, backup_list):
        choices = [Choice(title=backup) for backup in backup_list]
        choices.append(Choice(title="Retour"))
        backup_name = questionary.select("Quel backup ?",
                                         choices=choices).ask()
        return backup_name

    def prompt_for_play(self):
        user_input = questionary.select(
            "Commencer le tournoi ?", choices=["YES", "No"]
        ).ask()
        return user_input

    def prompt_continue_tournament(self):
        print("---Tournoi en cours---")
        user_input = questionary.select(
            "Passer au prochain Round ?", choices=["YES", "NO"]
        ).ask()
        return user_input

    def prompt_play_round(self, round_index):
        print(f"----DEBUT ROUND {round_index}-----")
        user_input = questionary.select("Jouer le round ?",
                                        choices=["YES", "NO"]
                                        ).ask()
        return user_input

    def prompt_for_get_winner(self, player_list):
        results = []
        for game in player_list:
            player1, player2 = game
            choices = [
                Choice(title=player1),
                Choice(title=player2),
                Choice(title="Match nul"),
            ]
            print(f"{player1} VS {player2} ! ")
            user_input = questionary.select(
                "Qui a remporté le match? ", choices=choices
            ).ask()
            results.append(user_input)
        return results

    def promp_for_play_auto(self):
        user_input = questionary.select(
            "-----Jouer les match automatiquement ?-----",
            choices=["YES", "NO"]
        ).ask()
        return user_input

    def prompt_for_save(self):
        user_input = questionary.select(
            "---Voulez effectuer une backup ?", choices=["YES", "NO"]
        ).ask()
        return user_input

    def prompt_for_remove_player_in_tournament(self, tournament_list):
        print("-----Supprimer un joueur du tournoi-----")

        name_tournament = questionary.select(
            "De quel tournoi ?", choices=tournament_list
        ).ask()
        return name_tournament

    def prompt_continue_add(self):
        user_input = questionary.select(
            "Un autre ?", choices=["YES", "NO"]
            ).ask()
        return user_input

    def prompt_export(self):
        user_input = questionary.select(
            "Voulez-vous exporter les fichier ?", choices=["YES", "NO"]
        ).ask()
        return user_input

    def prompt_data_tournament(self, tournament_list):
        choices = [Choice(title=tournament) for tournament in tournament_list]
        choices.append(Choice(title="Retour"))
        name_tournament = questionary.select("quel tournoi ?",
                                             choices=choices
                                             ).ask()
        return name_tournament

    def prompt_check_player(self):
        user_input = questionary.select(
            "Aucun joueur dans le tournoi. Voulez vous ajouter des joueurs ?",
            choices=["YES", "NO"],
        ).ask()
        return user_input

    def prompt_tournament_open(self, tournament_list):
        choices = [Choice(title=tournament) for tournament in tournament_list]
        choices.append(Choice(title="Créer un tournoi"))
        choices.append(Choice(title="Retour"))
        name_tournament = questionary.select(
            "Quel tournoi voulez vous commencer ?", choices=choices
        ).ask()
        return name_tournament

    def prompt_secure(self):
        user_input = questionary.select(
            "Vous êtes sûre ? ", choices=["YES", "NO"]
        ).ask()
        return user_input
