# config.py

import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupère le token du bot depuis les variables d'environnement
TOKEN = os.getenv("DISCORD_TOKEN")
