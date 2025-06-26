from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import uvicorn

app = FastAPI()

# Charger les données météo
try:
    data = pd.read_csv("donnees_meteo_communes.csv")
except FileNotFoundError:
    data = pd.DataFrame(columns=["commune", "code_postal", "zone_neige", "zone_vent", "altitude", "hors_gel"])

@app.get("/")
def home():
    return {"message": "API Météo pour dimensionnement d'ombrières photovoltaïques."}

@app.get("/commune/{nom_commune}")
def get_donnees_meteo(nom_commune: str):
    # Met en minuscule pour la recherche
    nom_commune_normalise = nom_commune.lower()

    # Création d'une colonne temporaire en minuscule pour recherche
    data["commune_temp"] = data["commune"].str.lower()

    # Recherche
    ligne = data[data["commune_temp"] == nom_commune_normalise]

    if ligne.empty:
        return JSONResponse(status_code=404, content={"erreur": f"Commune '{nom_commune}' introuvable"})

    resultat = ligne.iloc[0][["zone_neige", "zone_vent", "altitude", "hors_gel"]].to_dict()
    return resultat

# Optionnel : exécuter localement
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
