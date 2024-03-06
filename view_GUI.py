import re
from tkinter import *

FONT = "Arial"
BACKGROUND = "#f0eaff"
FONT_COLOR = "Black"


class Validator:

    def validate_input_str(self, prompt):
        while True:
            user_input = input(prompt)
            if not user_input.replace(
                " ",
                "",
            ).isalpha():
                print("Doit contenir seulement des lettres")
            else:
                return user_input

    def validate_date(self, prompt):
        pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(\d{4})$"

        while True:
            user_input = input(prompt)
            if re.match(pattern, user_input):
                return True
            else:
                print("Format invalide = > (JJ/MM/AAAA)")

    def validate_national_id(self, prompt):
        while True:
            user_input = input(prompt)
            if (
                len(user_input) == 7
                and user_input[:2].isalpha()
                and user_input[2:].isdigit()
            ):
                return user_input
            else:
                print(
                    "Format d'ID national invalide. Veuillez entrer 2 lettres suivies de 5 chiffres."
                )

    def validate_int(self, prompt):
        while True:
            user_input = input(prompt)
            if not user_input.isdigit():
                print("L'entrée doit être un chiffre")
            else:
                return user_input


class Window(Tk):
    def __init__(self):
        super().__init__()

        self.title("My application")
        self.geometry("720x480")
        self.minsize(480, 360)
        self.iconbitmap("logo.ico")
        self.config(background=BACKGROUND)

    def close_window(self):
        self.destroy()

    def get_input(self):
        pass

    def label_title(self, frame, title):
        self.title = title
        self.frame = frame
        label_title = Label(
            self.frame,
            text=title,
            font=(FONT, 40),
            bg=BACKGROUND,
            fg=FONT_COLOR,
        )
        label_title.pack()

    def button(self, frame, text, command):
        self.text = text
        self.frame = frame
        player_button = Button(
            self.frame,
            text=text,
            relief=GROOVE,
            command=command,
        )
        player_button.pack(pady=25, fill=X)

    def form(self, frame, *args):
        self.entries = []
        row = 0
        self.frame = frame

        for question in args:
            label_question = Label(
                self.frame, text=question, font=(FONT, 12), bg=BACKGROUND, fg=FONT_COLOR
            )
            label_question.grid(row=row, column=0, padx=10, pady=10)

            # Champ de saisie pour la réponse
            entry_response = Entry(self.frame)
            entry_response.grid(row=row, column=1, padx=10, pady=10)
            self.entries.append(entry_response)
            row += 1

        submit_button = Button(
            self.frame, text="Soumettre", relief=GROOVE, command=self.submit_response
        )
        submit_button.grid(row=row, column=0, padx=10, pady=10)

        self.frame.pack(expand=YES)
        row = 0
        print(self.entries)

    def submit_response(self):
        responses = []
        # Récupérer la réponse de l'utilisateur
        for self.entry_response in self.entries:
            response = self.entry_response.get()
            responses.append(response)

        # Faire quelque chose avec la réponse (par exemple, l'afficher)
        print(responses)
        return responses


class Menu:

    def __init__(self):
        self.validator = Validator()
        self.window = Window()

    def prompt_index(self):
        self.frame = Frame(self.window, bg=BACKGROUND)
        self.window.label_title(self.frame, "Bienvenue sur l'app")
        self.window.button(self.frame, "Ajouter un jouer", self.prompt_for_add_player)
        self.window.button(self.frame, "Ajouter un tournois", self.prompt_for_add_tournament)
        self.frame.pack()
        self.window.mainloop()

    def prompt_for_add_player(self):
        self.frame.pack_forget()
        self.frame = Frame(self.window, bg=BACKGROUND)
        self.window.form(
            self.frame,
            "Entrez le nom : ",
            "Entrez le prénom : ",
            "Entrez la date de naissance (JJ/MM/AAAA): ",
            "Entrez l'IDN : ",
        )

    def prompt_for_add_tournament(self):
        name_tournament = self.validator.validate_input_str(
            "Entrez le nom du tournoi : "
        )
        localisation = self.validator.validate_input_str(
            "Entrez la localisation du tournoi : "
        )
        round = 4
        date = self.validator.validate_date("Entrez la date du tournoi (JJ/MM/AAAA) : ")

        return name_tournament, localisation, round, date
