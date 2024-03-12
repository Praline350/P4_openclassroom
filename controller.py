from models import Player, DataJson, Tournament

from view import PromptForm, Menu
import os
import sys


data_json = DataJson()
form = PromptForm()
menu = Menu()
player = Player()
tournament = Tournament()

while True:
    user_input = menu.menu_index()

    match user_input:
        case "0":
            pass
        case "1":
            while True:
                user_input = menu.menu_player()

                match user_input:
                    case "1":
                        surname, name, birth_date, national_id = (
                            form.prompt_for_add_player()
                        )
                        player.write_player(surname, name, birth_date, national_id)
                        break
                    case "2":
                        user_input = input("Numéro D'ID : ")
                        player_data = player.find_player(user_input)
                        print(player_data)
                    case "4":
                        break

                    case "5":
                        sys.exit()

                    case _:
                        print("Choix invalide")
        case "2":
            while True:
                user_input = menu.menu_tournament()

                match user_input:
                    case "1":
                        name_tournament, localisation, round, start_date, end_date = (
                            form.prompt_for_add_tournament()
                        )
                        tournament.write_tournament(name_tournament, localisation, round, start_date, end_date)
                        break
                    case "2":
                        
                    

                    case "4":
                        break

                    case "5":
                        sys.exit()

        case "5":
            break
        case _:
            print("Choix invalide")
