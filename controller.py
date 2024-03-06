from models.models import Player
from view import View

JSON_DATA_FILE_PATH = "D:\openclassroom\projets\Projet 4\programmation\data.json"

view = View()

surname, name, birth_date, national_id = view.prompt_for_player()

player = Player(surname, name, birth_date, national_id)
player.inscription()
