import json
import logging
import os
import requests
import streamlit as st
import numpy as np

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Récupération de l'URL de l'API MLflow depuis les variables d'environnement
MLFLOW_API_URL = os.getenv('MLFLOW_API_URL', 'http://localhost:8000')
logging.info(f"MLFLOW_API_URL: {MLFLOW_API_URL}")

# Configuration de la page
st.set_page_config(
    page_title="Prédicteur de Prix Immobilier",
    page_icon="🏠",
    layout="wide"
)

# Titre de l'application
st.title("🏠 Prédicteur de Prix Immobilier")

# Création de colonnes pour organiser le layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Caractéristiques de la propriété")
    
    # Informations générales
    overall_qual = st.slider("Qualité générale (1-10)", 1, 10, 5)
    overall_cond = st.slider("Condition générale (1-10)", 1, 10, 7)
    year_built = st.number_input("Année de construction", 1800, 2024, 1961)
    
    # Surface et dimensions
    gr_liv_area = st.number_input("Surface habitable (pieds carrés)", 500, 10000, 1710)
    lot_area = st.number_input("Surface du terrain (pieds carrés)", 1000, 50000, 9600)
    lot_frontage = st.number_input("Façade du terrain (pieds)", 20, 200, 80)
    
    # Premier et deuxième étage
    first_flr_sf = st.number_input("Surface 1er étage (pieds carrés)", 0, 5000, 856)
    second_flr_sf = st.number_input("Surface 2ème étage (pieds carrés)", 0, 5000, 854)
    
    # Pièces
    total_rooms = st.number_input("Nombre total de pièces", 1, 20, 7)
    bedrooms = st.number_input("Nombre de chambres", 1, 10, 3)
    full_bath = st.number_input("Nombre de salles de bain complètes", 0, 5, 1)
    half_bath = st.number_input("Nombre de demi-salles de bain", 0, 5, 0)

with col2:
    st.subheader("Caractéristiques supplémentaires")
    
    # Garage
    garage_cars = st.number_input("Places de garage", 0, 5, 2)
    garage_area = st.number_input("Surface du garage (pieds carrés)", 0, 2000, 500)
    garage_yr_built = st.number_input("Année construction garage", 1800, 2024, 1961)
    
    # Sous-sol
    bsmt_fin_sf_1 = st.number_input("Surface finie sous-sol 1 (pieds carrés)", 0, 2000, 700)
    bsmt_fin_sf_2 = st.number_input("Surface finie sous-sol 2 (pieds carrés)", 0, 2000, 0)
    bsmt_unf_sf = st.number_input("Surface non finie sous-sol (pieds carrés)", 0, 2000, 150)
    total_bsmt_sf = st.number_input("Surface totale sous-sol (pieds carrés)", 0, 3000, 850)
    bsmt_full_bath = st.number_input("Salles de bain complètes au sous-sol", 0, 3, 1)
    bsmt_half_bath = st.number_input("Demi-salles de bain au sous-sol", 0, 3, 0)
    
    # Autres caractéristiques
    fireplaces = st.number_input("Nombre de cheminées", 0, 5, 2)
    wood_deck_sf = st.number_input("Surface du patio en bois (pieds carrés)", 0, 1000, 210)
    open_porch_sf = st.number_input("Surface du porche ouvert (pieds carrés)", 0, 500, 0)

# Bouton pour lancer la prédiction
if st.button("Prédire le prix"):
    # Préparation des données pour l'API
    input_data = {
        "dataframe_records": [{
            "Order": 1,
            "PID": 5286,
            "MS SubClass": 20,
            "Lot Frontage": lot_frontage,
            "Lot Area": lot_area,
            "Overall Qual": overall_qual,
            "Overall Cond": overall_cond,
            "Year Built": year_built,
            "Year Remod/Add": year_built,
            "Mas Vnr Area": 0.0,
            "BsmtFin SF 1": bsmt_fin_sf_1,
            "BsmtFin SF 2": bsmt_fin_sf_2,
            "Bsmt Unf SF": bsmt_unf_sf,
            "Total Bsmt SF": total_bsmt_sf,
            "1st Flr SF": first_flr_sf,
            "2nd Flr SF": second_flr_sf,
            "Low Qual Fin SF": 0,
            "Gr Liv Area": np.log1p(gr_liv_area),  # Apply same transformation as training
            "Bsmt Full Bath": bsmt_full_bath,
            "Bsmt Half Bath": bsmt_half_bath,
            "Full Bath": full_bath,
            "Half Bath": half_bath,
            "Bedroom AbvGr": bedrooms,
            "Kitchen AbvGr": 1,
            "TotRms AbvGrd": total_rooms,
            "Fireplaces": fireplaces,
            "Garage Yr Blt": garage_yr_built,
            "Garage Cars": garage_cars,
            "Garage Area": garage_area,
            "Wood Deck SF": wood_deck_sf,
            "Open Porch SF": open_porch_sf,
            "Enclosed Porch": 0,
            "3Ssn Porch": 0,
            "Screen Porch": 0,
            "Pool Area": 0,
            "Misc Val": 0,
            "Mo Sold": 5,
            "Yr Sold": 2010
        }]
    }
    
    try:
        logging.info("Tentative de connexion à l'API MLflow...")
        url = f"{MLFLOW_API_URL}/invocations"
        headers = {"Content-Type": "application/json"}
        
        logging.info(f"Données envoyées : {json.dumps(input_data, indent=2)}")
        response = requests.post(url, headers=headers, data=json.dumps(input_data))
        
        logging.info(f"Code de statut : {response.status_code}")
        
        if response.status_code == 200:
            prediction = response.json()
            logging.info(f"Réponse brute : {prediction}")
            
            # Apply inverse log transformation using expm1
            predicted_value = np.expm1(prediction['predictions'][0])
            predicted_price = "${:,.2f}".format(predicted_value)
            
            st.success(f"Prix estimé : {predicted_price}")
        else:
            logging.error(f"Erreur lors de la prédiction. Code : {response.status_code}")
            logging.error(f"Réponse : {response.text}")
            st.error("Une erreur s'est produite lors de la prédiction. Consultez les logs pour plus de détails.")
            
    except Exception as e:
        logging.error(f"Erreur de connexion à l'API : {str(e)}")
        logging.exception("Détails de l'erreur :")
        st.error("Une erreur s'est produite. Consultez les logs pour plus de détails.")

# Ajout d'informations supplémentaires
st.markdown("---")
st.markdown("""
### À propos de ce prédicteur
Ce modèle utilise des techniques d'apprentissage automatique pour prédire les prix immobiliers
en fonction des caractéristiques de la propriété. Les prédictions sont basées sur des données
historiques de ventes immobilières.

#### Notes importantes :
- Les prédictions sont données à titre indicatif
- Le modèle prend en compte de nombreuses caractéristiques de la propriété
- Les résultats peuvent varier en fonction du marché actuel
""")