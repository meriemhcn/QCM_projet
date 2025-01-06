import json
import time


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

def poser_questions(questions, limite_temps_total=None):
    score = 0
    total = len(questions)
    debut_test = time.time()

    for index, question in enumerate(questions, 1):
        temps_restant = int(limite_temps_total - (time.time() - debut_test))
        if temps_restant <= 0:
            print("Temps total écoulé pour le test !")
            break

        print(f"Temps restant : {temps_restant} secondes")
        print(f"Question {index}: {question['question']}")
        for option in question['options']:
            print(option)
        reponse = input("Votre réponse : ").strip().lower()

        temps_restant = int(limite_temps_total - (time.time() - debut_test))
        if temps_restant <= 0:
            print("\nTemps total écoulé pour le test !")
            break

        if reponse == question['correcte']:
            print("Bonne réponse !")
            score += 1
        else:
            print(f"Mauvaise réponse. La bonne réponse était : {question['correcte']}")
        print("-" * 30)
    return score, total


def afficher_historique(utilisateur, utilisateurs):
    historique = utilisateurs.get(utilisateur, {}).get("historique", [])
    if not historique:
        print("Aucun historique disponible.")
    else:
        print("Historique de {} :".format(utilisateur))
        for entree in historique:
            categorie = entree.get("categorie", "Non spécifiée")  # Valeur par défaut si la clé est absente
            print("- Date: {}, Catégorie: {}, Score: {}/{}".format(
                entree["date"], categorie, entree["score"], entree["total_questions"]
            ))