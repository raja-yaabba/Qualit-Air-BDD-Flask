import sqlite3
import os

# Chemin correct du fichier de base de données en utilisant une raw string pour éviter les problèmes d'échappement
chemin_db = r"C:\Users\but-info\OneDrive - UPEC\Documents\BUT Info\BUT1\Semestre 1\SAE 1.01 - 1.04 Projet\bdd\mesures_bdd.db"

# Check if the file exists
if os.path.exists(chemin_db):
    try:
        # If the file exists, delete it
        os.remove(chemin_db)
        print("Base de données supprimée")
    except OSError as e:
        print("Erreur en supprimant la bdd: {e}")

# Connexion à la base de données SQLite de manière sécurisée
try:
    conn = sqlite3.connect(chemin_db)
    cur = conn.cursor()

    # Définition du schéma de la table Site
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Site (
        codeSite TEXT PRIMARY KEY,
        nomSite TEXT,
        typeImplantation TEXT,
        typeInfluence TEXT,
        codeZas TEXT REFERENCES Zas(codeZas)
        );
    ''')

    # Définition du schéma de la table Zas
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Zas (
            codeZas TEXT PRIMARY KEY,
            nomZas TEXT,
            nomOrganisme TEXT REFERENCES Organisme(nomOrganisme)
        );
    ''')

    # Définition du schéma de la table Organisme
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Organisme (
            nomOrganisme TEXT PRIMARY KEY
        );
    ''')

    # Définition du schéma de la table Polluant
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Polluant (
            nomPolluant TEXT PRIMARY KEY
        );
    ''')

    # Définition du schéma de la table Mesure
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Mesure (
            debut DATETIME,
            fin DATETIME,
            codeSite TEXT REFERENCES Site(codeSite),
            nomPolluant TEXT REFERENCES Polluant(nomPolluant),
            discriminant TEXT,
            reglementaire TEXT,
            typeEvaluation TEXT,
            procedureMesure TEXT,
            typeValeur TEXT,
            valeur REAL,
            valeurBrute REAL,
            unite TEXT,
            tauxSaisie TEXT,
            couvertureTemporelle TEXT,
            couvertureDonnees TEXT,
            codeQualite TEXT,
            validite INTEGER
        );
    ''')

    # Valider les changements
    conn.commit()
    print("Base de données créée")
except sqlite3.Error as e:
    print(f"Une erreur s'est produite lors de la connexion à la base de données: {e}")
finally:
    # Fermer la connexion de manière sécurisée
    if conn:
        conn.close()