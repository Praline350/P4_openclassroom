from views.menu import Menu
from views.prompt_form import PromptForm
from views.display_message import DisplayMessage
from models.game import Game
from models.tournament import Tournament
from models.round import Round
from controller.controller_menu import ControllerMenu
import time


class ControllerGame:
    def __init__(self):
        self.menu = Menu()
        self.tournament = Tournament()
        self.round = Round()
        self.game = Game()
        self.form = PromptForm()
        self.display = DisplayMessage()
        self.controller = ControllerMenu()
        self.tournament_finished = False

    def begin_tournament(self):
        while not self.tournament_finished:

            tournament_list = self.tournament.get_tournament_open()
            name_tournament = self.form.prompt_tournament_open(tournament_list)
            if name_tournament == "Retour":
                break
            if name_tournament == "Créer un tournoi":
                self.controller.menu_add_tournament()
                break
            check_player = self.tournament.check_player_in_tournament(
                name_tournament
                )
            if check_player is True:
                user_input = self.form.prompt_check_player()
                if user_input == "YES":
                    self.controller.menu_add_player_in_tournament()
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
                    backup_list = self.tournament.get_name_backup()
                    backup_name = self.form.prompt_for_backup(backup_list)
                    user_input = self.form.prompt_secure()
                    if user_input == "YES":
                        name_tournament = self.tournament.restore_backup(
                            backup_name
                            )
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
        while not self.tournament_finished:
            tournament_list = self.tournament.get_name_tournaments()
            backup_list = self.tournament.get_name_backup()
            name_tournament = self.form.prompt_data_tournament(tournament_list)
            if name_tournament == "Retour":
                break
            backup_name = self.form.prompt_for_backup(backup_list)
            user_input = self.form.prompt_secure()
            if user_input == "YES":
                name_tournament = self.tournament.restore_backup(backup_name)
                user_input = self.form.prompt_for_play()
                if user_input == "YES":
                    self.play_round_manual(name_tournament)
                else:
                    break
            else:
                break

    def play_round(self, name_tournament):
        while True:
            round_index = self.tournament.get_round_index(name_tournament) + 1
            user_input = self.form.prompt_play_round(round_index)
            if user_input == "YES":
                round_index = self.round.add_round(name_tournament)
                self.game.make_game(name_tournament, round_index)
                result_list = self.game.play_game(name_tournament, round_index)
                for result in result_list:
                    if result[0] == "win":
                        self.display.display_win_result(result[1], result[2])
                        time.sleep(0.5)
                    elif result[0] == "draw":
                        self.display.display_draw_result(result[1], result[2])
                        time.sleep(0.5)
                self.game.end_game(name_tournament, round_index)
                self.game.sorted_score(name_tournament)
                bool = self.tournament.check_for_end(name_tournament)
                if bool is True:
                    self.end_of_tournament(name_tournament)
                    break
            else:
                break

    def play_round_manual(self, name_tournament):
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
        winner = self.tournament.end_tournament(name_tournament)
        self.display.display_end_tournament(winner)
        self.tournament_finished = True
        return self.tournament_finished


if __name__ == "__main__":
    pass
