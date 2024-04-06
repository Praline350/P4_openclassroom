
class DisplayMessage:

    def __init__(self):
        pass

    def display_simple_message(self, data):
        if data:
            print(data)
            return True
        else:
            print("Données inéxistantes")
            return False

    def display_data_list(self, data):
        if data:
            for d in data:
                print(d)
            return True
        else:
            print("Données inéxistantes")
            return False

    def display_success(self, bool):
        if bool:
            print("Opération réussi avec succès")
            return True
        else:
            print("Opération impossible")
            return False
        
    def display_player_exist(self, bool):
        if bool is False:
            print("Joueur inéxistant, Veuillez choisir dans la liste")
            
    def display_win_result(self, winner_name, loser_name):
        print(f"{winner_name} a gagné contre {loser_name}")

    def display_draw_result(self, player1_name, player2_name):
        print(f"Match nul entre {player1_name} et {player2_name}")
    
    def display_end_tournament(self, winner):
        print(f"TOURNOI TERMINER \n Gagnant : {winner}")

