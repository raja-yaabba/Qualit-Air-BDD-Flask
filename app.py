from flask import Flask, render_template
import sqlite3
import os
import pandas as pd

# Déclaration d'application Flask
app = Flask(__name__)

# Configuration pour servir les fichiers statiques
app.static_folder = 'static'

# Nom de la base de données SQLite
DATABASE = "mesuresbdd.db"

# Chemin relatif vers la base de données
db_path = os.path.join(os.path.dirname(__file__), 'bdd', 'mesures_bdd.db')
def requete_sql(requete):
    """Renvoie le résultat d'une requete sql passée en paramètre"""
    conn = sqlite3.connect(db_path)
    resultat = pd.read_sql_query(requete, conn)
    conn.close()
    return resultat

# Route pour la page d'accueil
@app.route('/')
def accueil():
    # recupérer la liste des organismes
    requete = "SELECT nomOrganisme AS 'Organismes :' FROM Organisme"
    orgas = requete_sql(requete)
    # afficher la page
    return render_template('index.html', orgas=orgas)

@app.route("/zone/<echelle>/<zone_id>", methods=['POST', 'GET'])
def zone(echelle, zone_id):
    if echelle == "Organisme":
        noms = {"sous_zone": "Zas", "zone_id": "nomOrganisme", "nom_zone": "nomOrganisme"}
        requete = f"SELECT * FROM {noms['sous_zone']} WHERE {noms['zone_id']} = '{zone_id}'"

    elif echelle == "Zas":
        noms = {"sous_zone": "Site", "zone_id": "codeZas", "nom_zone": "nomZas"}
        requete = f"SELECT * FROM {noms['sous_zone']} WHERE {noms['zone_id']} = '{zone_id}'"

    elif echelle == "Site":
        noms = {"sous_zone": "Mesure", "zone_id": "codeSite", "nom_zone": "nomSite"}
        requete = f"SELECT fin AS Date, valeur AS Valeur, unite AS Unité, nomPolluant AS 'Polluant'  FROM {noms['sous_zone']} WHERE {noms['zone_id']} = '{zone_id}'"

    # on récupère la liste des sous-zones dans la zone
    sous_zones = requete_sql(requete)

    return render_template("zone.html", sous_zones=sous_zones, sous_echelle=noms["sous_zone"], echelle=echelle, zone_id=zone_id)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
