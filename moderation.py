import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio

def setup_moderation(bot):
    # Cache pour les messages supprimés
    if not hasattr(bot, "deleted_messages"):
        bot.deleted_messages = {}

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

    @bot.command()
    async def snipe(ctx):
        """Affiche le dernier message supprimé du canal, s'il a été supprimé récemment."""
        channel_id = ctx.channel.id
        if channel_id not in bot.deleted_messages:
            await ctx.send("❌ Aucun message supprimé trouvé récemment dans ce canal.")
            return

        # Vérification de l'heure du message
        sniped_message = bot.deleted_messages[channel_id]
        time_diff = datetime.utcnow() - sniped_message["time"]
        if time_diff > timedelta(seconds=30):
            await ctx.send("❌ Aucun message supprimé trouvé récemment dans ce canal.")
            del bot.deleted_messages[channel_id]
            return

        # Afficher le message supprimé
        embed = discord.Embed(
            title="🕵️ Message supprimé récupéré",
            description=sniped_message["content"],
            color=discord.Color.orange(),
            timestamp=sniped_message["time"]
        )
        embed.set_author(name=str(sniped_message["author"]), icon_url=sniped_message["author"].avatar.url)
        embed.set_footer(text="Message supprimé il y a moins de 30 secondes.")
        await ctx.send(embed=embed)
