import json
import time
from datetime import datetime
import csv


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

# Main application
def application_qcm():
    fichier_utilisateurs = "utilisateurs.json"
    fichier_questions = "questions.json"
    fichier_csv = "resultats.csv"

    utilisateurs = charger_utilisateurs(fichier_utilisateurs)
    utilisateur = input("Entrez votre nom d'utilisateur : ").strip()

    if utilisateur not in utilisateurs:
        print("Nouvel utilisateur. Création de profil...")
        utilisateurs[utilisateur] = {"historique": []}
    else:
        afficher_historique(utilisateur, utilisateurs)

    categorie = input("Choisissez une catégorie (Python, Réseaux, Algorithmes) ou laissez vide pour toutes les catégories : ").strip()
    questions = charger_questions(fichier_questions, categorie)
    if not questions:
        return

    limite_temps_total = 30  # Temps fixe à 30 secondes

    print("\nLe test commence maintenant !\n")
    score, total = poser_questions(questions, limite_temps_total)

    print(f"Votre score final : {score}/{total}")

    # Mise à jour de l'historique
    utilisateurs[utilisateur]["historique"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "categorie": categorie,
        "score": score,
        "total_questions": total
    })
    sauvegarder_utilisateurs(fichier_utilisateurs, utilisateurs)

    # Exportation automatique des résultats
    exporter_resultats(utilisateur, utilisateurs[utilisateur]["historique"], fichier_csv)

    print("\nHistorique mis à jour avec succès !")

if __name__ == "__main__":
    application_qcm()



