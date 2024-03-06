from models import Player, DataJson, Tournament

from view import PromptForm, Menu
import os


data_json = DataJson()
view = PromptForm()
menu = Menu()

while True:
    user_input = menu.prompt_index()
    print(user_input)
    match user_input:
        case "1":
            surname, name, birth_date, national_id = view.prompt_for_add_player()
            player = Player(surname, name, birth_date, national_id)
            player.add_player(surname, name)
        case "2":
            name_tournament, localisation, round, date = view.prompt_for_add_tournament()
            tournament = Tournament(name_tournament, localisation, round, date)
            tournament.add_tournament(name_tournament, date)
        case "5":
            break

        case _:
            print("Choix invalide")


    