# Utilisation de l'image Python
FROM python:3.9

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers dans le conteneur
COPY . /app

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposition du port Streamlit
EXPOSE 8501

# Commande pour exécuter l'application
CMD ["streamlit", "run", "app.py"]
