import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import asyncio

from config import bot

# Commande: +giveaway
@bot.command()
@commands.has_permissions(manage_messages=True)
async def giveaway(ctx, num_winners: str, prize: str, duration: str):
    """Lance un giveaway directement en précisant [gagnants] [lot] [durée (en minutes)]."""
    # Vérification des arguments
    try:
        num_winners = int(num_winners)
        duration = int(duration)
    except ValueError:
        await ctx.send("❌ Les arguments doivent être des nombres valides : `[gagnants] [lot] [durée en minutes]`.")
        return

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

    @discord.ui.button(label="Nouvelle Reroll 🎉", style=discord.ButtonStyle.green)
    async def reroll(self, interaction: discord.Interaction, button: Button):
        """Tire un gagnant supplémentaire (reroll) parmi les participants."""
        if len(self.participants) == 0:
            await interaction.response.send_message("⚠️ Il n'y a pas de participants pour effectuer un reroll.", ephemeral=True)
            return
        
        winner = random.choice(self.participants)
        await interaction.response.send_message(f"🎉 Nouveau gagnant du reroll : <@{winner}> !", ephemeral=True)

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
    # Vérifiez si un giveaway actif est en cours (vous pouvez améliorer cette logique selon votre implémentation)
    giveaway_view = GiveawayView.get_active_giveaway(ctx.guild)  # Supposons que vous ayez une méthode pour récupérer un giveaway actif
    if not giveaway_view or len(giveaway_view.participants) == 0:
        await ctx.send("❌ Aucun giveaway actif ou aucun participant pour effectuer un reroll.")
        return
    
    winner = random.choice(giveaway_view.participants)
    await ctx.send(f"🎉 Nouveau gagnant du reroll : <@{winner}> !")
