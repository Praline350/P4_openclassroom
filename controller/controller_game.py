from views.menu import Menu
from views.prompt_form import PromptForm
from views.display_message import DisplayMessage
from models.game import Game
from models.tournament import Tournament
from models.round import Round
from models.report import Report
from controller.controller_menu import ControllerMenu


class ControllerGame:
    def __init__(self):
        self.menu = Menu()
        self.tournament = Tournament()
        self.round = Round()
        self.game = Game()
        self.report = Report()
        self.form = PromptForm()
        self.display = DisplayMessage()
        self.controller = ControllerMenu()

    def begin_tournament(self):
        """Logique de début de tournoi"""

        while True:
            tournament_list = self.tournament.get_name_tournaments()
            name_tournament = self.form.prompt_data_tournament(tournament_list)
            if name_tournament == "Retour":
                break
            check_closed = self.tournament.check_tournament_closes(
                name_tournament
                )
            if check_closed is True:
                self.display.display_closed_tournament()
                continue
            elif name_tournament == "Créer un tournoi":
                self.controller.menu_add_tournament()
                continue
            check_player = self.tournament.check_player_in_tournament(
                name_tournament
                )
            if check_player == 1:
                self.display.display_no_player()
                break
            elif check_player == 2:
                self.display.display_impair()
                break
            user_input = self.form.prompt_for_begin_tournament()
            match user_input:
                case "Commencer le tournoi":
                    user_input = self.form.prompt_for_save()
                    if user_input == "YES":
                        self.tournament.save_in_backup(name_tournament)
                        user_input = self.form.prompt_for_play()
                        if user_input == "YES":
                            self.play_round_manual(name_tournament)
                        else:
                            break
                    user_input = self.form.prompt_for_play()
                    if user_input == "YES":
                        self.play_round_manual(name_tournament)
                    else:
                        break
                case "Backup":
                    backup_list = self.tournament.get_backup_from_name(
                        name_tournament
                        )
                    backup_name = self.form.prompt_for_backup(backup_list)
                    if backup_name == "Retour":
                        break
                    user_input = self.form.prompt_secure()
                    if user_input == "YES":
                        name_tournament = self.tournament.restore_backup(
                            backup_name
                            )
                        check = self.tournament.check_tournament_closes(
                            name_tournament
                            )
                        if check is True:
                            self.display.display_closed_tournament()
                            break
                        if check_player == 1:
                            self.display.display_no_player()
                            break
                        elif check_player == 2:
                            self.display.display_impair()
                            break
                        user_input = self.form.prompt_for_play()
                        if user_input == "YES":
                            self.play_round_manual(name_tournament)
                        else:
                            break
                    else:
                        break
                case "Retour":
                    break

    def play_from_backup(self):
        """Permet de jouer un tournoi d'une backup"""

        while True:
            tournament_list = self.tournament.get_name_tournaments()
            name_tournament = self.form.prompt_data_tournament(tournament_list)
            backup_list = self.tournament.get_backup_from_name(name_tournament)
            if name_tournament == "Retour":
                break
            backup_name = self.form.prompt_for_backup(backup_list)
            user_input = self.form.prompt_secure()
            if user_input == "YES":
                name_tournament = self.tournament.restore_backup(backup_name)
                check = self.tournament.check_tournament_closes(
                    name_tournament
                    )
                if check is True:
                    self.display.display_closed_tournament()
                    continue
                check_player = self.tournament.check_player_in_tournament(
                    name_tournament
                    )
                if check_player == 1:
                    self.display.display_no_player()
                    break
                elif check_player == 2:
                    self.display.display_impair()
                    break
                user_input = self.form.prompt_for_play()
                if user_input == "YES":
                    self.play_round_manual(name_tournament)
                else:
                    break
            else:
                break

    def play_round_manual(self, name_tournament):
        """Logique de rounds, distribution des match en fonction des points"""

        while True:
            round_index = self.tournament.get_round_index(name_tournament) + 1
            user_input = self.form.prompt_play_round(round_index)
            if user_input == "YES":
                round_index = self.round.add_round(name_tournament)
                self.game.make_game(name_tournament, round_index)
                player_list = self.game.get_game_player(
                    name_tournament,
                    round_index
                    )
                results = self.form.prompt_for_get_winner(player_list)
                self.game.update_scores(name_tournament, round_index, results)
                self.game.end_game(name_tournament, round_index)
                self.game.sorted_score(name_tournament)
                bool = self.tournament.check_for_end(name_tournament)
                if bool is True:
                    self.end_of_tournament(name_tournament)
                    break
            else:
                break

    def end_of_tournament(self, name_tournament):
        """Fin de tournoi, défini le vaiqueur"""

        winner = self.tournament.end_tournament(name_tournament)
        self.display.display_end_tournament(winner)
        user_input = self.form.prompt_export()
        if user_input == "YES":
            data = self.report.all_report(name_tournament)
            self.report.export_all(data)


if __name__ == "__main__":
    pass
