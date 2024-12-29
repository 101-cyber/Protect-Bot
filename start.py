import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ajout du chemin de base pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Debug : Vérifiez si le chemin est correctement ajouté
print(f"Chemin absolu du projet ajouté à sys.path : {project_root}")
print(f"Chemins dans sys.path : {sys.path}")

# Import des modules
try:
    from script.discordbot.CAF.config import bot
    from script.discordbot.CAF.keep_alive import keep_alive
    from script.discordbot.CAF.commands import *  # Charge les commandes
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(f"Erreur lors de l'import des modules : {e}")

# Charger les variables d'environnement
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Vérifiez que le token est disponible
token = os.getenv('DISCORD_TOKEN')
if not token:
    raise ValueError("Le token Discord est introuvable. Vérifiez le fichier .env et la variable DISCORD_TOKEN.")

# Garder le bot en ligne
keep_alive()

# Lancer le bot
try:
    bot.run(token)
except Exception as e:
    raise RuntimeError(f"Erreur lors du lancement du bot : {e}")
