from models_GUI import PlayerForm
import os
import tkinter as tk

if not os.path.exists("data"):
    os.makedirs("data")

root = tk.Tk()  # Crée une nouvelle fenêtre principale
player_form = PlayerForm(root)  # Instancie PlayerForm avec la fenêtre principale
root.mainloop()
