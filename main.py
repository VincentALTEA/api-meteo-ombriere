from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Chargement du fichier CSV une seule fois au démarrage
try:
    data = pd.read_csv("donnees_meteo_communes.csv", encoding='utf-8')
except Exception as e:
    print(f"Erreur lors du chargement du CSV : {e}")
    data = pd.DataFrame()

# Fonction de nettoyage des noms de commune
def normaliser_nom(nom):
    return str(nom).strip().lower().replace("-", " ").replace("’", "'").replace("é", "e").replace("è", "e")

# Route racine
@app.route('/')
def accueil():
    return "API Météo pour dimensionnement d'ombrières photovoltaïques."

# Route de requête par commune
@app.route('/commune/<nom_commune>')
def obtenir_donnees(nom_commune):
    if data.empty:
        return jsonify({"error": "Fichier CSV non chargé"}), 500

    nom_recherche = normaliser_nom(nom_commune)
    data['nom_normalise'] = data['commune'].apply(normaliser_nom)

    result = data[data['nom_normalise'] == nom_recherche]

    if result.empty:
        return jsonify({"error": f"Commune '{nom_commune}' introuvable dans la base."}), 404

    ligne = result.iloc[0]
    return jsonify({
        "commune": ligne["commune"],
        "code_postal": ligne["code_postal"],
        "zone_neige": ligne["zone_neige"],
        "zone_vent": ligne["zone_vent"],
        "altitude": ligne["altitude"],
        "hors_gel": ligne["hors_gel"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
