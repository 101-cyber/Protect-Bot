import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ajout du chemin de base pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from script.discordbot.CAF.config import bot
from script.discordbot.CAF.keep_alive import keep_alive
from script.discordbot.CAF.commands import *  # Charge les commandes

# Charger les variables d'environnement
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)
token = os.getenv('DISCORD_TOKEN')

if not token:
    raise ValueError("Le token Discord est introuvable. Vérifiez le fichier .env et la variable DISCORD_TOKEN.")

# Garder le bot en ligne
keep_alive()

# Lancer le bot
bot.run(token)
