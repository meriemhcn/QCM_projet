import json
import time
from datetime import datetime
import csv
import tkinter as tk
from tkmacosx import Button
from PIL import Image, ImageTk 

# Couleurs et polices
BG_COLOR = "#C2E9FB"
FG_COLOR = "#205072"
ACCENT_COLOR = "#6cbcbf"
BUTTON_COLOR = "#C2E9FB"  # Couleur des boutons
BUTTON_ACTIVE_COLOR = "#6cbcbf"  # Couleur des boutons lorsqu'ils sont actifs
CUSTOM_FONT = ("Courier", 16)  # Police personnalisée

# Gestion des utilisateurs
def charger_utilisateurs(fichier):
    try:
        with open(fichier, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def sauvegarder_utilisateurs(fichier, utilisateurs):
    with open(fichier, 'w') as f:
        json.dump(utilisateurs, f, indent=4)

def exporter_resultats(utilisateur, historique, fichier_csv):
    try:
        with open(fichier_csv, 'a', newline='') as csvfile:  # Append mode
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:  # Écrire l'en-tête uniquement si le fichier est vide
                writer.writerow(["Utilisateur", "Date", "Catégorie", "Score", "Total Questions"])
            for entree in historique:
                writer.writerow([utilisateur, entree["date"], entree.get("categorie", "Non spécifiée"), entree["score"], entree["total_questions"]])
        print(f"Résultats exportés avec succès dans '{fichier_csv}'.")
    except Exception as e:
        print(f"Erreur lors de l'exportation : {e}")

class QCMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application QCM")

        # Définir la taille et centrer la fenêtre
        window_width = 1000
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculer les coordonnées pour centrer la fenêtre
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Appliquer la géométrie de la fenêtre
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        
        self.fichier_utilisateurs = "utilisateurs.json"
        self.fichier_questions = "questions.json"
        self.fichier_csv = "resultats.csv"

        self.utilisateurs = charger_utilisateurs(self.fichier_utilisateurs)
        self.utilisateur_actuel = None
        self.questions = []
        self.score = 0
        self.total_questions = 0
        self.index_question = 0
        self.temps_restant = 30
        self.test_en_cours = False

        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(expand=True)

        # Titre de bienvenue
        tk.Label(frame, text="Bienvenue dans l'application QCM", font=("Arial", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(pady=10)

        # Charger une image comme logo
        try:
            image = Image.open("logob.png")  # Remplacez par le chemin de votre image
            image = image.resize((200, 100), Image.Resampling.LANCZOS)  # Utilisez Image.Resampling.LANCZOS
            logo = ImageTk.PhotoImage(image)
            tk.Label(frame, image=logo, bg=BG_COLOR).pack(pady=10)
            self.root.logo = logo  # Référence pour éviter que l'image soit supprimée par le garbage collector
        except Exception as e:
            print(f"Erreur lors du chargement du logo : {e}")

        # Bouton Start
        Button(frame, text="Start", command=self.create_login_screen, fg=FG_COLOR, bg=BUTTON_COLOR, font=("Arial", 16), activeforeground=ACCENT_COLOR).pack(pady=20)
