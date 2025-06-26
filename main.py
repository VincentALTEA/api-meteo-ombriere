from flask import Flask, jsonify
import pandas as pd

df = pd.read_csv("donnees_meteo_communes.csv")

app = Flask(__name__)

@app.route("/")
def home():
    return "API Météo pour dimensionnement d'ombrières photovoltaïques."

@app.route("/commune/<nom_commune>")
def get_infos_commune(nom_commune):
    match = df[df["commune"].str.lower() == nom_commune.lower()]
    if match.empty:
        return jsonify({"erreur": "Commune non trouvée"}), 404
    ligne = match.iloc[0]
    return jsonify({
        "commune": ligne["commune"],
        "code_postal": ligne["code_postal"],
        "zone_neige": ligne["zone_neige"],
        "zone_vent": ligne["zone_vent"],
        "altitude": ligne["altitude"],
        "hors_gel": ligne["hors_gel"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
