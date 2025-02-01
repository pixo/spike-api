# Utiliser une image Python optimisée
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8080 pour Fly.io
EXPOSE 8080

# Commande pour démarrer le serveur Flask
CMD ["python", "server.py"]