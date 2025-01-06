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
        
# Gestion des questions
def charger_questions(fichier, categorie=None):
    try:
        with open(fichier, 'r') as f:
            questions = json.load(f)
            if not questions:
                raise ValueError("Le fichier des questions est vide.")
            if categorie:
                categorie = categorie.lower()  # Rendre la catégorie insensible à la casse
                categories_disponibles = {q.get("categorie", "").lower() for q in questions}
                if categorie not in categories_disponibles:
                    print(f"Catégorie invalide. Catégories disponibles : {categories_disponibles}")
                    return []
                questions = [q for q in questions if q.get("categorie", "").lower() == categorie]
                if not questions:
                    raise ValueError("Aucune question trouvée pour la catégorie choisie.")
            return questions
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Erreur : {e}")
        print("Veuillez vérifier le fichier '{}' et réessayer.".format(fichier))
        return []
