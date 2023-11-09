#FROM ubuntu:latest
#LABEL authors="antoi"

#ENTRYPOINT ["top", "-b"]

FROM python:3.9-slim

# Définition du répertoire de travail
WORKDIR /transactions_service

# Copie du fichier des dépendances
COPY requirements.txt requirements.txt

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du code source dans le conteneur
COPY . .

ENV PYTHONPATH /:$PYTHONPATH

# Commande pour démarrer l'application
CMD ["python", "run.py"]