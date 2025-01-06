import json

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