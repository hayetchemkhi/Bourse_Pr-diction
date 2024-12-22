import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import tensorflow as tf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configurer le style de la page
st.set_page_config(
    page_title="Dashboard Boursière",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Chargement des modèles h5
MODELS = {
    "AAPL": tf.keras.models.load_model("models/AAPL_stock_price_lstm_model.h5"),
    "AMZN": tf.keras.models.load_model("models/AMZN_stock_price_lstm_model.h5"),
    "GOOGL": tf.keras.models.load_model("models/GOOGL_stock_price_lstm_model.h5"),
    "TSLA": tf.keras.models.load_model("models/TSLA_stock_price_lstm_model.h5"),
    "NFLX": tf.keras.models.load_model("models/NFLX_stock_price_lstm_model.h5"),
}

# Fonction pour obtenir les données réelles des actions
@st.cache_data(ttl=60)
def get_stock_data(ticker, days=30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    data = yf.download(ticker, start=start_date, end=end_date, interval="1h")
    return data

# Fonction pour effectuer des prédictions
def predict_stock_price(model, recent_data):
    scaled_data = recent_data / np.max(recent_data)  # Normalisation simple
    scaled_data = scaled_data.reshape(1, -1, 1)  # Reshape pour le modèle
    prediction = model.predict(scaled_data)
    return prediction[0][0] * np.max(recent_data)  # Denormalisation

# Charger les prédictions sauvegardées
def load_predictions():
    try:
        return pd.read_csv("predictions.csv", index_col=0)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Stock", "Predicted_Price"])

# Sauvegarder les nouvelles prédictions
def save_prediction(stock, predicted_price):
    predictions = load_predictions()
    new_entry = pd.DataFrame([[datetime.now(), stock, predicted_price]], columns=["Date", "Stock", "Predicted_Price"])
    predictions = pd.concat([predictions, new_entry], ignore_index=True)
    predictions.to_csv("predictions.csv", index=False)

# Sidebar
st.sidebar.title("Configuration")
selected_stock = st.sidebar.selectbox("Sélectionnez une action", ["AAPL", "AMZN", "GOOGL", "TSLA", "NFLX"])
num_days = st.sidebar.slider("Nombre de jours d'historique", 7, 90, 30)
show_predictions = st.sidebar.checkbox("Afficher les prédictions", value=True)

# Ajouter un bouton pour afficher les prédictions passées
page = st.sidebar.radio("Choisissez une page", ["Dashboard", "Prédictions Passées"])

# Titre principal
st.title("💹 Dashboard Boursière en Temps Réel")
st.write(f"Visualisez les données et prédictions des actions boursières pour **{selected_stock}**.")

if page == "Dashboard":
    # Obtenir les données
    stock_data = get_stock_data(selected_stock, days=num_days)

    # Vérification des données
    if stock_data.empty:
        st.error("Impossible de récupérer les données pour cette action. Essayez une autre.")
    else:
        # Graphique des prix historiques
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data["Close"], mode="lines", name="Prix de clôture"))
        fig.update_layout(
            title=f"Prix de clôture de {selected_stock} sur les {num_days} derniers jours",
            xaxis_title="Date",
            yaxis_title="Prix",
            template="plotly_dark",
            legend=dict(x=0, y=1.0, bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Prédiction si activée
        if show_predictions:
            recent_data = stock_data["Close"].values[-50:]  # Dernières 50 valeurs pour prédiction
            prediction = predict_stock_price(MODELS[selected_stock], recent_data)

            st.markdown("### 📈 Prédiction du prochain prix")
            st.metric(
                label=f"Prix estimé pour {selected_stock} (prochaine période)",
                value=f"${prediction:.2f}",
                delta=f"${prediction - recent_data[-1]:.2f}",
            )

            st.write("**Note :** Les prédictions sont basées sur un modèle simple et peuvent ne pas refléter avec précision les fluctuations réelles du marché.")

            # Enregistrer la prédiction
            save_prediction(selected_stock, prediction)

        # Table des données récentes
        st.markdown("### 🗂️ Données Récentes")
        st.dataframe(stock_data.tail(10))

elif page == "Prédictions Passées":
    st.subheader("Historique des Prédictions")
    
    # Calendrier pour sélectionner une date spécifique
    date_selected = st.date_input("Sélectionnez une date", datetime.now())
    predictions = load_predictions()

    # Filtrer les prédictions par date sélectionnée
    predictions["Date"] = pd.to_datetime(predictions["Date"])
    filtered_predictions = predictions[predictions["Date"].dt.date == date_selected]


    if not filtered_predictions.empty:
        st.dataframe(filtered_predictions)
    else:
        st.write("Aucune prédiction pour cette date.")

# Footer
st.markdown(
    """
    ---
    **📊 Dashboard créé avec [Streamlit](https://streamlit.io)**  
    Auteur : *Hayet Chemkhi*  
    """
)
