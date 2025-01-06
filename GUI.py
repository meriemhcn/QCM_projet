import json
import time
from datetime import datetime
import csv
import tkinter as tk
from tkinter import messagebox, ttk
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

    def create_login_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(expand=True)

        #tk.Label(frame, text="Bienvenue dans l'application QCM", font=("Arial", 16), fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)
        tk.Label(frame, text="Entrez votre nom d'utilisateur :", font=CUSTOM_FONT, fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)
        self.entry_username = tk.Entry(frame, width=20, fg=FG_COLOR, bg=BG_COLOR, font=CUSTOM_FONT, highlightthickness=0.5)
        self.entry_username.pack(pady=10)
        Button(frame, text="Continuer", command=self.handle_login, fg=FG_COLOR, bg=BUTTON_COLOR, font=CUSTOM_FONT, activeforeground=ACCENT_COLOR).pack(pady=10)

    def handle_login(self):
        username = self.entry_username.get().strip()
        if not username:
            messagebox.showerror("Erreur", "Veuillez entrer un nom d'utilisateur.")
            return

        self.utilisateur_actuel = username
        if username not in self.utilisateurs:
            self.utilisateurs[username] = {"historique": []}
            self.create_category_screen()
        else:
            self.show_user_options()
    def show_user_options(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(expand=True)

        tk.Label(frame, text=f"Bonjour, {self.utilisateur_actuel}", font=("Arial", 16), fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)

        Button(frame, text="Qcm", command=self.create_category_screen, fg=FG_COLOR, bg=BUTTON_COLOR, font=CUSTOM_FONT, activeforeground=ACCENT_COLOR).pack(pady=10)
        Button(frame, text="Historique", command=self.show_history, fg=FG_COLOR, bg=BUTTON_COLOR, font=CUSTOM_FONT, activeforeground=ACCENT_COLOR).pack(pady=10)
            
    def show_history(self):
            self.clear_screen()

            frame = tk.Frame(self.root, bg=BG_COLOR)
            frame.pack(expand=True)

            tk.Label(frame, text=f"Historique de {self.utilisateur_actuel}", font=("Arial", 16), fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)

            historique = self.utilisateurs[self.utilisateur_actuel]["historique"]
            if not historique:
                tk.Label(frame, text="Aucun historique disponible.", font=("Arial", 14), fg=FG_COLOR, bg=BG_COLOR).pack(pady=10)
            else:
                for entry in historique:
                    tk.Label(frame, text=f"Date: {entry['date']}, Catégorie: {entry['categorie']}, Score: {entry['score']}/{entry['total_questions']}", font=("Arial", 12), fg=FG_COLOR, bg=BG_COLOR, wraplength=500, justify="left").pack(pady=5)

            Button(frame, text="Retour", command=self.show_user_options, fg=FG_COLOR, bg=BUTTON_COLOR, font=CUSTOM_FONT, activeforeground=ACCENT_COLOR).pack(pady=20)
    def create_category_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(expand=True)

        tk.Label(frame, text=f"Bonjour, {self.utilisateur_actuel}", font=("Arial", 14), fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)
        tk.Label(frame, text="Choisissez une catégorie :", font=CUSTOM_FONT, fg=FG_COLOR, bg=BG_COLOR).pack()
        self.combo_category = ttk.Combobox(
            frame,
            values=["Python", "Reseau", "Algorithme"],
            font=CUSTOM_FONT,
            state="readonly",
            style="TCombobox"
        )
        self.combo_category.pack(pady=10)
        Button(frame, text="Commencer", command=self.start_quiz, fg=FG_COLOR, bg=BUTTON_COLOR, font=CUSTOM_FONT, activeforeground=ACCENT_COLOR).pack(pady=10)


    def start_quiz(self):
        self.categorie_selectionnee = self.combo_category.get().strip()  # Stockez la catégorie
        if not self.categorie_selectionnee:
            messagebox.showerror("Erreur", "Veuillez sélectionner une catégorie.")
            return

        self.questions = self.load_questions(self.categorie_selectionnee)
        if not self.questions:
            messagebox.showerror("Erreur", "Aucune question trouvée pour la catégorie sélectionnée.")
            return

        self.score = 0
        self.total_questions = len(self.questions)
        self.index_question = 0
        self.temps_restant = 60
        self.test_en_cours = True

        self.create_question_screen()
        self.update_timer()

    def load_questions(self, categorie):
        try:
            with open(self.fichier_questions, 'r', encoding='utf-8') as f:  # Ajout de encoding='utf-8'
                questions = json.load(f)
                return [q for q in questions if q.get("categorie", "").lower() == categorie.lower()]
        except Exception as e:
            print(f"Erreur lors du chargement des questions : {e}")
            return []


    def create_question_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(expand=True)

        if self.index_question < self.total_questions:
            question = self.questions[self.index_question]

            tk.Label(frame, text=f"Temps restant : {self.temps_restant} secondes", font=("Arial", 14), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=10)
            tk.Label(frame, text=f"Question {self.index_question + 1}/{self.total_questions}", font=("Arial", 14), fg=FG_COLOR, bg=BG_COLOR).pack()
            tk.Label(frame, text=question["question"], wraplength=400, fg=FG_COLOR, bg=BG_COLOR, font=("Arial", 11)).pack(pady=10)

            self.var_answer = tk.StringVar()
            for option in question["options"]:
                tk.Radiobutton(frame, text=option, variable=self.var_answer, value=option[0], fg=FG_COLOR, bg=BG_COLOR, selectcolor=ACCENT_COLOR, font=CUSTOM_FONT).pack(anchor="w")

            feedback_label = tk.Label(frame, text="", font=("Arial", 12), fg=ACCENT_COLOR, bg=BG_COLOR)
            feedback_label.pack(pady=10)

            def validate_and_provide_feedback():
                selected_answer = self.var_answer.get().strip().lower()
                if selected_answer == question["correcte"]:
                    feedback_label.config(text="Bonne réponse !", fg="green")
                    self.score += 1
                else:
                    feedback_label.config(text=f"Réponse incorrecte. La bonne réponse était : {question['correcte']}", fg="red")

                self.index_question += 1
                self.root.after(2000, self.create_question_screen)

            Button(frame, text="Valider", command=validate_and_provide_feedback, fg=FG_COLOR, bg=BUTTON_COLOR, font=CUSTOM_FONT, activeforeground=ACCENT_COLOR).pack(pady=10)
        else:
            self.test_en_cours = False
            self.show_results()
    def update_timer(self):
        if self.temps_restant > 0 and self.test_en_cours:
            self.temps_restant -= 1
            self.root.after(1000, self.update_timer)
        elif self.temps_restant <= 0 and self.test_en_cours:
            self.test_en_cours = False
            messagebox.showinfo("Temps écoulé", "Le temps est écoulé pour ce test.")
            self.show_results()
            
    def show_results(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(expand=True)

        tk.Label(frame, text="Résultats du test", font=("Arial", 16), fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)
        tk.Label(frame, text=f"Score : {self.score}/{self.total_questions}", font=("Arial", 14), fg=FG_COLOR, bg=BG_COLOR).pack(pady=10)

        self.utilisateurs[self.utilisateur_actuel]["historique"].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "categorie": self.categorie_selectionnee,  # Utilisez la catégorie sauvegardée
            "score": self.score,
            "total_questions": self.total_questions
        })
        sauvegarder_utilisateurs(self.fichier_utilisateurs, self.utilisateurs)
        exporter_resultats(self.utilisateur_actuel, self.utilisateurs[self.utilisateur_actuel]["historique"], self.fichier_csv)

        Button(frame, text="Retour", command=self.create_login_screen, fg=FG_COLOR, bg=BUTTON_COLOR, font=CUSTOM_FONT, activeforeground=ACCENT_COLOR).pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Appliquer un thème compatible
    style = ttk.Style()
    style.theme_use("clam")  # "clam" fonctionne bien sur macOS
    root.configure(bg=BG_COLOR)  # Set background color for the window
    app = QCMApp(root)
    root.mainloop()        