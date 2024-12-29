# Utiliser une image de base Python
FROM python:3.12-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Exécuter les tests unitaires avec Pytest
RUN pytest test_app.py

# Exposer le port de l'application
EXPOSE 8501

# Commande pour lancer l'application
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
