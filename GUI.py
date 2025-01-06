import json
import time
from datetime import datetime
import csv
import tkinter as tk

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