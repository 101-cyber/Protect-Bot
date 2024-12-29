import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import time

from config import bot, message_logs

# Événement: Ban automatique si un lien est envoyé ou si quelqu'un fait du spam
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Anti-spam: Si un utilisateur envoie plus de 3 messages en 5 secondes
    now = time.time()
    message_logs[message.author.id].append(now)
    message_logs[message.author.id] = [
        timestamp for timestamp in message_logs[message.author.id] if now - timestamp <= 5
    ]

    if len(message_logs[message.author.id]) > 3:
        await message.guild.ban(message.author, reason="Spam détecté")
        await message.channel.send(f"🚫 {message.author.mention} a été banni pour spam.")
        return

    # Ban si un utilisateur mentionne @everyone sans permission admin
    if "@everyone" in message.content and not message.author.guild_permissions.administrator:
        await message.delete()
        await message.guild.ban(message.author, reason="Mention non autorisée de @everyone")
        await message.channel.send(f"🚫 {message.author.mention} a été banni pour mention non autorisée de @everyone.")
        return

    # Ban automatique pour l'envoi de liens
    if "http://" in message.content or "https://" in message.content:
        await message.delete()
        await message.guild.ban(message.author, reason="Envoi de lien interdit")
        await message.channel.send(f"{message.author.mention} a été banni pour avoir envoyé un lien.")
        return

    await bot.process_commands(message)

# Commande: +giveaway
@bot.command()
@commands.has_permissions(manage_messages=True)
async def giveaway(ctx, num_winners: int, prize: str, duration: int):
    """Lance un giveaway directement en précisant [gagnants] [lot] [durée (en minutes)]."""
    if num_winners <= 0 or duration <= 0:
        await ctx.send("❌ Le nombre de gagnants et la durée doivent être des nombres positifs.")
        return

    duration_seconds = duration * 60  # Conversion des minutes en secondes

    embed = discord.Embed(
        title="🎉 Giveaway !",
        description=f"**Récompense** : {prize}\n"
                    f"**Nombre de gagnants** : {num_winners}\n"
                    f"**Durée** : {duration} minute(s)\n\n"
                    f"Cliquez sur le bouton pour participer !",
        color=discord.Color.gold(),
    )
    embed.set_footer(text="Bonne chance à tous !")

    view = GiveawayView(ctx.author.id, num_winners, prize, duration_seconds)
    view.message = await ctx.send(embed=embed, view=view)

class GiveawayView(View):
    def __init__(self, author_id, num_winners, prize, duration_seconds):
        super().__init__(timeout=duration_seconds)
        self.author_id = author_id
        self.num_winners = num_winners
        self.prize = prize
        self.participants = []

    @discord.ui.button(label="Participer 🎟️", style=discord.ButtonStyle.blurple)
    async def join_giveaway(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id in self.participants:
            await interaction.response.send_message("⚠️ Vous êtes déjà inscrit !", ephemeral=True)
        else:
            self.participants.append(interaction.user.id)
            await interaction.response.send_message("✅ Vous avez été inscrit avec succès !", ephemeral=True)

    async def on_timeout(self):
        if len(self.participants) == 0:
            await self.message.edit(content="🎉 Giveaway terminé ! Aucun participant. 😢", view=None)
            return

        winners = [
            f"<@{winner}>" for winner in random.sample(self.participants, k=min(len(self.participants), self.num_winners))
        ]
        result_message = (
            f"🎉 Le giveaway est terminé !\n\n**Récompense** : {self.prize}\n"
            f"**Gagnants** : {', '.join(winners)}\n\nFélicitations !"
        )
        await self.message.edit(content=result_message, embed=None, view=None)

# Commande: +reroll
@bot.command()
@commands.has_permissions(manage_messages=True)
async def reroll(ctx):
    """Tire un gagnant au hasard parmi les participants d'un giveaway actif."""
    # À compléter si vous avez un système de suivi des giveaways actifs
    await ctx.send("🎉 Fonctionnalité de reroll en cours de mise à jour !")

# Commande: +list
@bot.command()
async def list(ctx):
    """Affiche la liste des commandes disponibles."""
    embed = discord.Embed(
        title="📜 Liste des commandes disponibles",
        description="""Voici la liste des commandes que vous pouvez utiliser :

        **+giveaway [gagnants] [lot] [durée en minutes]** : Lance un giveaway.
        **+reroll** : Tire un gagnant supplémentaire pour un giveaway.
        """,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)
