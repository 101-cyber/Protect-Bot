from collections import defaultdict
import discord
from discord.ext import commands

# Configuration du bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.members = True

bot = commands.Bot(command_prefix='+', intents=intents)

# Variables globales pour l'anti-spam
message_logs = defaultdict(list)
