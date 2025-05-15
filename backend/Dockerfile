FROM python:3.9-slim

WORKDIR /app

# Copier uniquement le fichier des dépendances d'abord pour profiter du cache Docker
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu du backend dans le conteneur
COPY . .

# Exposer le port que l'application utilise
EXPOSE 8000

# Commande pour lancer l'application avec rechargement automatique (utile pour dev)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
