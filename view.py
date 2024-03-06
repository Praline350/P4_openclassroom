class View:

    def prompt_for_player(self):
        surname = input("Entrez le nom : ")
        name = input("Entrez le prénom : ")
        birth_date = input("Entrez la date de naissance : ")
        national_id = input("Entrez le IDN : ")
        return surname, name, birth_date, national_id
