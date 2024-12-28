import os
from config import bot
from commands import *

# Démarrage du bot
bot.run(os.getenv('DISCORD_TOKEN'))
