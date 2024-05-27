import sqlite3
import requests
import io
import csv

def dateToDB(date):
    '''
    Insère les données des sites dans la base de données pour une date donnée.
    date (str): Date du fichier CSV au format YYYY-MM-DD.
    '''
    # URL du fichier CSV
    url_base = "https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/2023/"
    file_name = f"FR_E2_{date}.csv"
    url_file = url_base + file_name

    # Téléchargement du fichier CSV
    response = requests.get(url_file)
    if response.status_code != 200:
        print(f"Erreur lors du téléchargement du fichier : Statut HTTP {response.status_code}")
        return

    # Chemin de la base de données
    chemin_db = r"C:\Users\but-info\OneDrive - UPEC\Documents\BUT Info\BUT1\Semestre 1\SAE 1.01 - 1.04 Projet\bdd\mesures_bdd.db"
    # Lecture du contenu du fichier CSV
    content_string = response.content.decode('utf-8')
    csv_file = io.StringIO(content_string)
    lecteur = csv.DictReader(csv_file, delimiter=';')

    # Connexion à la base de données SQLite
    conn = sqlite3.connect(chemin_db)
    cur = conn.cursor()

    c = 0

    for el in lecteur:
        print(f"ligne {c} insérée")
        c+=1

        code_site = el["code site"]
        # Vérifier si le site existe déjà dans la base de données
        cur.execute("SELECT 1 FROM Site WHERE codeSite = ?", (code_site,))
        if not cur.fetchone():
            # Si le site n'existe pas, l'insérer
            try:
                cur.execute('''
                    INSERT INTO Site (codeSite, nomSite, typeImplantation, typeInfluence, codeZas)
                    VALUES (?, ?, ?, ?, ?);
                ''', (el["code site"], el["nom site"], el["type d'implantation"], el["type d'influence"], el["code zas"]))
            except sqlite3.Error as e:
                print(f"Erreur SQLite lors de l'insertion du site {code_site}: {e}")
                continue
        # Vérifier si le site existe déjà dans la base de données
# Insérer dans la table Organisme
        cur.execute("SELECT 1 FROM Organisme WHERE NomOrganisme = ?", (el["Organisme"],))
        if not cur.fetchone():
            try:
                cur.execute('''
                    INSERT INTO Organisme (nomOrganisme)
                    VALUES (?);
                ''', (el["Organisme"],))
            except sqlite3.Error as e:
                print(f"Erreur SQLite lors de l'insertion de l'organisme {el['Organisme']}: {e}")

        # Insérer dans la table Polluant
        cur.execute("SELECT 1 FROM Polluant WHERE nomPolluant = ?", (el["Polluant"],))
        if not cur.fetchone():
            try:
                cur.execute('''
                    INSERT INTO Polluant (nomPolluant)
                    VALUES (?);
                ''', (el["Polluant"],))
            except sqlite3.Error as e:
                print(f"Erreur SQLite lors de l'insertion du polluant {el['Polluant']}: {e}")

        # Insérer dans la table ZAS
        cur.execute("SELECT 1 FROM ZAS WHERE CodeZAS = ?", (el["code zas"],))
        if not cur.fetchone():
            try:
                cur.execute('''
                    INSERT INTO ZAS (codeZas, nomZas, nomOrganisme)
                    VALUES (?, ?, ?);
                ''', (el["code zas"], el["Zas"], el["Organisme"]))
            except sqlite3.Error as e:
                print(f"Erreur SQLite lors de l'insertion du ZAS {el['code zas']}: {e}")

        # Insérer dans la table Mesure
        # Assurez-vous que toutes les clés dans el sont exactement les noms des champs dans votre fichier CSV
        try:
            cur.execute('''
                INSERT INTO Mesure (debut, fin, codeSite, nomPolluant, discriminant, reglementaire, typeEvaluation, procedureMesure, typeValeur, valeur, valeurBrute, unite, tauxSaisie, couvertureTemporelle, couvertureDonnees, codeQualite, validite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', (
                el["\ufeffDate de début"],
                el["Date de fin"],
                el["code site"],
                el["Polluant"],
                el["discriminant"],
                el["Réglementaire"],
                el["type d'évaluation"],
                el["procédure de mesure"],
                el["type de valeur"],
                el["valeur"],
                el["valeur brute"],
                el["unité de mesure"],
                el["taux de saisie"],
                el["couverture temporelle"],
                el["couverture de données"],
                el["code qualité"],
                el["validité"]
            ))
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de l'insertion de la mesure pour le site {el['code site']}: {e}")

    # Valider les changements dans la base de données
    conn.commit()

    # Fermer la connexion à la base de données
    conn.close()

dateToDB("2023-01-01")