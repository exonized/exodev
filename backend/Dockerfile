# Utilisez une image de base appropriée pour votre application FastAPI
FROM python:3.8

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installez les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le contenu du dossier app dans le conteneur

COPY main.py /app/main.py

# Exposez le port sur lequel FastAPI sera exécuté
EXPOSE 8081

# Commande de démarrage de l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]