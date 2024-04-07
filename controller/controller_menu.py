from views.prompt_form import PromptForm
from views.display_message import DisplayMessage
from models.player import Player
from models.tournament import Tournament
from models.report import Report


class ControllerMenu:
    def __init__(self):
        self.report = Report()
        self.tournament = Tournament()
        self.player = Player()
        self.display = DisplayMessage()
        self.form = PromptForm()

    def menu_report_player(self):
        while True:
            data = self.report.player_report()
            bool = self.display.display_data_list(data)
            if bool:
                user_input = self.form.prompt_export()
            if user_input == "YES":
                bool = self.report.export_players_to_file(data)
                self.display.display_success(bool)
                break
            else:
                break

    def menu_report_tournament(self):
        while True:
            tournament_list = self.tournament.get_name_tournaments()
            name_tournament = self.form.prompt_data_tournament(tournament_list)
            data = self.report.tournament_report(name_tournament)
            bool = self.display.display_simple_message(data)
            if bool:
                user_input = self.form.prompt_export()
            if user_input == "YES":
                bool = self.report.export_tournament_to_file(data)
                self.display.display_success(bool)
                break
            else:
                break

    def menu_report_player_in_tournament(self):
        while True:
            tournament_list = self.tournament.get_name_tournaments()
            name_tournament = self.form.prompt_data_tournament(tournament_list)
            data = self.report.player_in_tournament_report(name_tournament)
            bool = self.display.display_data_list(data)
            if bool:
                user_input = self.form.prompt_export()
            if user_input == "YES":
                self.report.export_player_in_tournament(name_tournament, data)
                break
            else:
                break

    def menu_report_round(self):
        while True:
            tournament_list = self.tournament.get_name_tournaments()
            name_tournament = self.form.prompt_data_tournament(tournament_list)
            data = self.report.round_report(name_tournament)
            bool = self.display.display_simple_message(data)
            if bool:
                user_input = self.form.prompt_export()
            if user_input == "YES":
                self.report.export_round_to_file(name_tournament, data)
                break
            else:
                break

    def menu_add_player(self):
        while True:
            surname, name, birth_date = self.form.prompt_for_add_player()
            national_id = self.form.prompt_national_id()
            national_id = self.player.write_player(
                surname, name, birth_date, national_id
            )
            bool = self.player.player_exists(national_id)
            if bool:
                self.display.display_success(bool)
                break
            pass

    def menu_remove_player(self):
        while True:
            national_id = self.player.get_all_player_id()
            id_player = self.form.prompt_for_id_list(national_id)
            user_input = self.form.prompt_secure()
            if user_input == "YES":
                bool = self.player.remove_player(id_player)
            else:
                break
            if bool:
                self.display.display_success(bool)
                break

    def menu_add_tournament(self):
        while True:
            (name_tournament, localisation, round, start_date, end_date) = (
                self.form.prompt_for_add_tournament()
            )
            self.tournament.write_tournament(
                name_tournament, localisation, round, start_date, end_date
            )
            break

    def menu_add_player_in_tournament(self):
        while True:
            players_ids = self.player.get_all_player_id()
            tournament_list = self.tournament.get_name_tournaments()
            name_tournament = self.form.prompt_data_tournament(tournament_list)
            national_id = self.form.prompt_national_id()
            bool = self.player.player_exists(national_id)
            if not bool:
                self.display.display_player_exist(bool)
                national_id = self.form.prompt_for_id_list(players_ids)
                bool, message = self.tournament.add_player_in_tournament(
                    name_tournament, national_id
                )
            else:
                bool, message = self.tournament.add_player_in_tournament(
                    name_tournament, national_id
                )
            if bool is True:
                self.display.display_success(bool)
                self.display.display_simple_message(message)
            else:
                self.display.display_success(bool)
                self.display.display_simple_message(message)
            user_input = self.form.prompt_continue_add()
            if user_input == "YES":
                pass
            if user_input == "NO":
                break

    def menu_remove_tournament(self):
        while True:
            tournament_list = self.tournament.get_name_tournaments()
            name_tournament = self.form.prompt_for_remove_tournament(tournament_list)
            user_input = self.form.prompt_secure()
            if user_input == "YES":
                self.tournament.remove_tournament(name_tournament)
            else:
                break

    def menu_remove_player_in_tournament(self):
        while True:
            tournament_list = self.tournament.get_name_tournaments()
            name_tournament = self.form.prompt_for_remove_player_in_tournament(
                tournament_list
            )
            players_ids = self.tournament.get_ids_in_tournament(name_tournament)
            national_id = self.form.prompt_national_id()
            bool = self.tournament.find_player_in_tournament(
                name_tournament, national_id
            )

            if not bool:
                self.display.display_player_exist(bool)
                national_id = self.form.prompt_for_id_list(players_ids)
                user_input = self.form.prompt_secure()
                if user_input == "YES":
                    bool = self.tournament.remove_player_in_tournament(
                        name_tournament, national_id
                    )
                else:
                    break

            else:
                user_input = self.form.prompt_secure()
                if user_input == "YES":
                    bool = self.tournament.remove_player_in_tournament(
                        name_tournament, national_id
                    )
                else:
                    break
            if bool is True:
                self.display.display_success(bool)
            else:
                self.display.display_success(bool)
            user_input = self.form.prompt_continue_add()
            if user_input == "YES":
                pass
            if user_input == "NO":
                break

    def menu_save_tournament(self):
        tournament_list = self.tournament.get_name_tournaments()
        name_tournament = self.form.prompt_data_tournament(tournament_list)
        bool = self.tournament.save_in_backup(name_tournament)
        if bool:
            self.display.display_success(bool)
        else:
            self.display.display_success(bool)

    def menu_add_description(self):
        tournament_list = self.tournament.get_name_tournaments()
        name_tournament = self.form.prompt_data_tournament(tournament_list)
        description = self.form.prompt_for_add_description()
        bool = self.tournament.add_description(name_tournament, description)
        if bool:
            self.display.display_success(bool)
        else:
            self.display.display_success(bool)
