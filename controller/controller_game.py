from views.menu import Menu
from views.prompt_form import PromptForm
from views.display_message import DisplayMessage
from models.game import Game
from models.tournament import Tournament
from models.round import Round
import time


class ControllerGame:
    def __init__(self):
        self.menu = Menu()
        self.tournament = Tournament()
        self.round = Round()
        self.game = Game()
        self.form = PromptForm()
        self.display = DisplayMessage()

    def begin_tournament(self):
        user_input = self.form.prompt_for_begin_tournament()
        match user_input:
            case "Commencer/Continuer":
                tournament_list = self.tournament.get_name_tournaments()
                name_tournament = self.menu.menu_begin_tournament(tournament_list)
                self.tournament.save_in_backup(name_tournament)
                self.play_round(name_tournament)
            case "Backup":
                backup_list = self.tournament.get_name_backup()
                backup_name = self.form.prompt_for_backup(backup_list)
                print(backup_name)
                user_input = self.form.prompt_secure()
                if user_input == "YES":
                    name_tournament = self.tournament.restore_backup(backup_name)
                    self.play_round(name_tournament)

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

    def end_of_tournament(self, name_tournament):
        winner = self.tournament.end_tournament(name_tournament)
        self.display.display_end_tournament(winner)
