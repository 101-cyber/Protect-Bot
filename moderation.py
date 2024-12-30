import discord
from discord.ext import commands
from datetime import datetime, timedelta
import re

def setup_moderation(bot):
    # Cache pour les messages supprimés
    if not hasattr(bot, "deleted_messages"):
        bot.deleted_messages = {}
    
    # Cache pour le suivi des messages envoyés
    if not hasattr(bot, "message_cache"):
        bot.message_cache = {}

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return  # Ignorer les bots

        # Vérifier si l'utilisateur peut bypass
        if any(role.permissions.administrator for role in message.author.roles):
            return  # Les administrateurs sont exemptés des restrictions

        # Anti-spam : Ban si 5 messages en 5 secondes
        user_id = message.author.id
        now = datetime.utcnow()
        bot.message_cache.setdefault(user_id, []).append(now)

        # Nettoyer les messages envoyés il y a plus de 5 secondes
        bot.message_cache[user_id] = [
            msg_time for msg_time in bot.message_cache[user_id]
            if now - msg_time <= timedelta(seconds=5)
        ]

        if len(bot.message_cache[user_id]) >= 5:
            await message.author.ban(reason="Anti-spam : Envoi de 5 messages en moins de 5 secondes.")
            await message.channel.send(f"{message.author.mention} a été banni pour spam.")
            return

        # Anti-mention excessive : Ban si @everyone est mentionné
        if "@everyone" in message.content:
            await message.author.ban(reason="Anti-mention excessive : Mention de @everyone.")
            await message.channel.send(f"{message.author.mention} a été banni pour mention excessive.")
            return

        # Anti-lien : Ban si un lien est détecté
        if re.search(r'https?://', message.content):
            await message.author.ban(reason="Anti-lien : Envoi de lien détecté.")
            await message.channel.send(f"{message.author.mention} a été banni pour envoi de lien.")
            return

        # Transmettre l'événement on_message aux commandes si nécessaires
        await bot.process_commands(message)

    @bot.event
    async def on_message_delete(message):
        """Capture les messages supprimés."""
        if message.author.bot:
            return

        # Ajout du message supprimé dans le cache
        bot.deleted_messages[message.channel.id] = {
            "author": message.author,
            "content": message.content,
            "time": datetime.utcnow()
        }
