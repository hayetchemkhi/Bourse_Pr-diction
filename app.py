import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import tensorflow as tf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import os

# Configurer le style de la page
st.set_page_config(
    page_title="Dashboard Boursière",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS pour l'image de fond
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("http://www.itespresso.fr/wp-content/uploads/2011/09/bourse-%C3%A9conomie-ipo-entreprise-%C2%A9-2jenn-Fotolia-com.jpg");
    background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Fonction de hachage de mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Charger ou créer un fichier utilisateur
def load_users():
    try:
        return pd.read_csv("users.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["username", "password"])

# Sauvegarder un nouvel utilisateur
def save_user(username, password):
    users = load_users()
    if username in users["username"].values:
        return False
    new_user = pd.DataFrame([[username, hash_password(password)]], columns=["username", "password"])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv("users.csv", index=False)
    return True

# Vérifier les identifiants
def authenticate(username, password):
    users = load_users()
    hashed_password = hash_password(password)
    user = users[(users["username"] == username) & (users["password"] == hashed_password)]
    return not user.empty

# Initialisation de session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

# Interface de connexion et d'enregistrement
if not st.session_state.authenticated:
    st.sidebar.title("🔐 Connexion")
    choice = st.sidebar.radio("Choisissez une option", ["Se connecter", "S'inscrire"])

    if choice == "Se connecter":
        username = st.sidebar.text_input("Nom d'utilisateur")
        password = st.sidebar.text_input("Mot de passe", type="password")
        if st.sidebar.button("Se connecter"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.sidebar.success("Connexion réussie ✅")
            else:
                st.sidebar.error("Identifiants incorrects ❌")

    elif choice == "S'inscrire":
        new_username = st.sidebar.text_input("Nom d'utilisateur")
        new_password = st.sidebar.text_input("Mot de passe", type="password")
        confirm_password = st.sidebar.text_input("Confirmez le mot de passe", type="password")
        if st.sidebar.button("Créer un compte"):
            if new_password == confirm_password:
                if save_user(new_username, new_password):
                    st.sidebar.success("Compte créé avec succès 🎉")
                else:
                    st.sidebar.error("Nom d'utilisateur déjà pris ❌")
            else:
                st.sidebar.error("Les mots de passe ne correspondent pas ❌")
    st.stop()

# --- CONTENU DU DASHBOARD SI CONNECTÉ ---

MODELS = {
    "AAPL": tf.keras.models.load_model("models/AAPL_stock_price_lstm_model.h5"),
    "AMZN": tf.keras.models.load_model("models/AMZN_stock_price_lstm_model.h5"),
    "GOOGL": tf.keras.models.load_model("models/GOOGL_stock_price_lstm_model.h5"),
    "TSLA": tf.keras.models.load_model("models/TSLA_stock_price_lstm_model.h5"),
    "NFLX": tf.keras.models.load_model("models/NFLX_stock_price_lstm_model.h5"),
}

@st.cache_data(ttl=60)
def get_stock_data(ticker, days=30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    data = yf.download(ticker, start=start_date, end=end_date, interval="1h")
    return data

def predict_stock_price(model, recent_data):
    scaled_data = recent_data / np.max(recent_data)
    scaled_data = scaled_data.reshape(1, -1, 1)
    prediction = model.predict(scaled_data)
    return prediction[0][0] * np.max(recent_data)

def save_prediction(ticker, prediction):
    if not os.path.exists("predictions.csv"):
        pd.DataFrame(columns=["Date", "Stock", "Prediction"]).to_csv("predictions.csv", index=False)

    new_entry = pd.DataFrame([[datetime.now(), ticker, prediction]], columns=["Date", "Stock", "Prediction"])
    df = pd.read_csv("predictions.csv")
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv("predictions.csv", index=False)

# Sidebar
st.sidebar.title(f"Bienvenue {st.session_state.username} 👋")
selected_stock = st.sidebar.selectbox("Sélectionnez une action", ["AAPL", "AMZN", "GOOGL", "TSLA", "NFLX"])
num_days = st.sidebar.slider("Nombre de jours d'historique", 7, 60, 30)
show_predictions = st.sidebar.checkbox("Afficher les prédictions", value=True)
show_history = st.sidebar.button("📅 Voir l'historique")

if show_history:
    #st.title("📜 Historique des Prédictions")
    st.markdown(
     """
     <div style="
         background-color: black;
         padding: 20px;
         border-radius: 10px;
         text-align: center;
         margin-bottom: 30px;
         box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
     ">
         <h1 style="color: white; margin: 0;">
            📜  Historique des Prédictions
         </h1>
     </div>
     """,
     unsafe_allow_html=True,
)
    df = pd.read_csv("predictions.csv")
    st.dataframe(df)
    st.stop()

st.markdown(
    """
    <div style="
        background-color: black;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
    ">
        <h1 style="color: white; margin: 0;">
            Dashboard Boursière en Temps Réel
        </h1>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write(f"Visualisez les données et prédictions pour **{selected_stock}**.")


if st.sidebar.button("Se déconnecter"):
    st.session_state.authenticated = False
    st.experimental_rerun()

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
        legend=dict(x=0, y=1.0),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Prédiction si activée
    if show_predictions:
        recent_data = stock_data["Close"].values[-50:]
        prediction = predict_stock_price(MODELS[selected_stock], recent_data)
        st.metric(label=f"Prix estimé pour {selected_stock}", value=f"${prediction:.2f}")
        st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 30px;
        ">
            <div style="
                background-color: black;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
            ">
                <h2 style="color: white; font-size: 60px; margin: 0;">
                    ${prediction:.2f}
                </h2>
                <p style="font-size: 20px; color: grey; text-align: center; margin: 10px 0 0;">
                    Prix estimé pour {selected_stock}
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(stock_data.tail(10))
    st.markdown(
    """
    <style>
    .stDataFrame {
        width: 100% !important;
        max-width: 100%;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

