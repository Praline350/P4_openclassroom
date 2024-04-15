from .validator import Validator
import questionary
from questionary import Choice


class PromptForm:

    def __init__(self):
        self.validator = Validator()
        self.retour = Choice(title="retour")

    def prompt_national_id(self):
        """Entrée pour ID"""

        national_id = self.validator.validate_national_id("Entrez l'IDN : ")
        return national_id

    def prompt_id_or_list(self):
        """Entrée pour ID , renvoie False si aucune entrées"""

        national_id = self.validator.validate_id_or_list("Entrez l'IDN : ")
        return national_id

    def prompt_for_add_player(self):
        """Entrées pour ajouter un joueur"""

        print("------AJOUTER UN JOUEUR------")

        surname = self.validator.validate_input_str("Entrez le nom : ")
        name = self.validator.validate_input_str("Entrez le prénom : ")
        birth_date = self.validator.validate_date(
            "Entrez la date de naissance (JJ-MM-AAAA): "
        )

        return surname, name, birth_date

    def prompt_for_add_tournament(self):
        """Entrées pour ajouter un tournoi"""

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
        """Permet de selectionner un joueur depuis la liste des ID"""

        id_player = questionary.select("Liste des joueurs",
                                       choices=players_ids
                                       ).ask()
        return id_player

    def tournament_add_round(self, tournament_list):
        """Permet d'ajouté un round manuelement"""

        print("-----AJOUTER UN ROUND AU TOURNOI-----")
        name_tournament = questionary.select(
            "Quel tournoi ?", choices=tournament_list
        ).ask()
        return name_tournament

    def prompt_for_remove_tournament(self, tournament_list):
        """Permet de selectionner un tournoi a suppr dans la liste"""

        print("-----SUPPRIMER UN TOURNOI-----")
        name_tournament = questionary.select(
            "Quel tournoi supprimé ?", choices=tournament_list
        ).ask()
        return name_tournament

    def prompt_for_add_description(self):
        """Entrée pour ajouter une description"""

        description = questionary.text("Ajouter une description ?").ask()
        return description

    def prompt_for_begin_tournament(self):
        """Entrées du début de tournoi"""

        user_input = questionary.select(
            "Débuter le tournoi ou reprendre une sauvegarde ?",
            choices=["Commencer le tournoi", "Backup", "Retour"],
        ).ask()
        return user_input

    def prompt_for_backup(self, backup_list):
        """Entrée pour choisir une backup dans la liste"""

        choices = [Choice(title=backup) for backup in backup_list]
        choices.append(Choice(title="Retour"))
        backup_name = questionary.select("Quel backup ?",
                                         choices=choices).ask()
        return backup_name

    def prompt_for_play(self):
        """Validation pour commencer un tournoi"""

        user_input = questionary.select(
            "Commencer le tournoi ?", choices=["YES", "No"]
        ).ask()
        return user_input

    def prompt_continue_tournament(self):
        """Valisation pour passer au prochain round"""

        print("---Tournoi en cours---")
        user_input = questionary.select(
            "Passer au prochain Round ?", choices=["YES", "NO"]
        ).ask()
        return user_input

    def prompt_play_round(self, round_index):
        """Validation pour jouer le round en cours"""

        print(f"----DEBUT ROUND {round_index}-----")
        user_input = questionary.select("Jouer le round ?",
                                        choices=["YES", "NO"]
                                        ).ask()
        return user_input

    def prompt_for_get_winner(self, player_list):
        """Entrées pour choisir le gagnant(ou match nul) des matchs en cours"""

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
        """(dev) Pour jouer les matchs auto"""

        user_input = questionary.select(
            "-----Jouer les match automatiquement ?-----",
            choices=["YES", "NO"]
        ).ask()
        return user_input

    def prompt_for_save(self):
        """Entrée pour sauvegarder le tournoi"""

        user_input = questionary.select(
            "---Voulez effectuer une backup ?", choices=["YES", "NO"]
        ).ask()
        return user_input

    def prompt_for_remove_player_in_tournament(self, tournament_list):
        """Entrée pour supprimer un joueur du tournoi"""

        print("-----Supprimer un joueur du tournoi-----")

        name_tournament = questionary.select(
            "De quel tournoi ?", choices=tournament_list
        ).ask()
        return name_tournament

    def prompt_continue_add(self):
        """Entrée pour ajouter un autre joueur"""

        user_input = questionary.select(
            "Un autre ?", choices=["YES", "NO"]
            ).ask()
        return user_input

    def prompt_export(self):
        """Entrée pour exporter un rapport"""

        user_input = questionary.select(
            "Voulez-vous exporter le rapport ?", choices=["YES", "NO"]
        ).ask()
        return user_input

    def prompt_data_tournament(self, tournament_list):
        """Entrée pour selectionner un tournoi dans la liste"""

        choices = [Choice(title=tournament) for tournament in tournament_list]
        choices.append(Choice(title="Retour"))
        name_tournament = questionary.select("Quel tournoi ?",
                                             choices=choices
                                             ).ask()
        return name_tournament

    def prompt_check_player(self):
        """Entrée pour ajouter des joueur au tournoi si il n'en contient pas"""

        user_input = questionary.select(
            "Aucun joueur dans le tournoi. Voulez vous ajouter des joueurs ?",
            choices=["YES", "NO"],
        ).ask()
        return user_input

    def prompt_tournament_open(self, tournament_list):
        """Choisir dans la liste des tournoi ouvert"""

        choices = [Choice(title=tournament) for tournament in tournament_list]
        choices.append(Choice(title="Créer un tournoi"))
        choices.append(Choice(title="Retour"))
        name_tournament = questionary.select(
            "Quel tournoi voulez vous commencer ?", choices=choices
        ).ask()
        return name_tournament

    def prompt_no_tournament(self):
        user_input = questionary.select('Aucun tournoi, en créer un ?',
                                        choices=["YES", "NO"]).ask()
        return user_input

    def prompt_secure(self):
        """Valisation de sécurité"""

        user_input = questionary.select(
            "Vous êtes sûre ? ", choices=["YES", "NO"]
        ).ask()
        return user_input
