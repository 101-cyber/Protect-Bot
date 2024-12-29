import discord
from discord.ext import commands
import random

# Commande: +giveaway
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

class GiveawayView(discord.ui.View):
    def __init__(self, author_id, num_winners, prize, duration_seconds):
        super().__init__(timeout=duration_seconds)
        self.author_id = author_id
        self.num_winners = num_winners
        self.prize = prize
        self.participants = []

    @discord.ui.button(label="Participer 🎟️", style=discord.ButtonStyle.blurple)
    async def join_giveaway(self, interaction: discord.Interaction, button: discord.ui.Button):
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
async def reroll(ctx):
    """Tire un gagnant au hasard parmi les participants d'un giveaway actif."""
    await ctx.send("🎉 Fonctionnalité de reroll en cours de mise à jour !")

# Commande: +list
async def list(ctx):
    """Affiche la liste des commandes disponibles."""
    embed = discord.Embed(
        title="📜 Liste des commandes disponibles",
        description="""Voici la liste des commandes que vous pouvez utiliser :

        **+giveaway [gagnants] [lot] [durée en minutes]** : Lance un giveaway.
        **+reroll** : Tire un gagnant supplémentaire pour un giveaway.
        **+lock** : Verrouille le salon pour que seuls les membres avec un rôle spécifique puissent parler.
        **+unlock** : Déverrouille le salon pour que tout le monde puisse parler.
        **+bl [utilisateur]** : Banni l'utilisateur de façon permanente.
        **+wl [utilisateur]** : Déban l'utilisateur.
        **+reset** : Supprime tous les messages d'un salon.
        """,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# Commande: +lock
async def lock(ctx):
    """Verrouille le salon, empêchant les membres sans le rôle spécifié de parler."""
    role = discord.utils.get(ctx.guild.roles, name="+")
    if role:
        await ctx.channel.set_permissions(role, send_messages=True)
        for member in ctx.guild.members:
            if role not in member.roles:
                await ctx.channel.set_permissions(member, send_messages=False)
        await ctx.send(f"Le salon a été verrouillé. Seuls les membres avec le rôle `{role.name}` peuvent parler.")
    else:
        await ctx.send("Le rôle spécifié n'existe pas dans ce serveur.")

# Commande: +unlock
async def unlock(ctx):
    """Déverrouille le salon, permettant à tous de parler."""
    for member in ctx.guild.members:
        await ctx.channel.set_permissions(member, send_messages=True)
    await ctx.send("Le salon a été déverrouillé. Tout le monde peut maintenant parler.")

# Commande: +bl
async def bl(ctx, member: discord.Member):
    """Ban permanent l'utilisateur mentionné."""
    await member.ban(reason="Ban permanent")
    await ctx.send(f"{member.mention} a été banni de manière permanente.")

# Commande: +wl
async def wl(ctx, member: discord.Member):
    """Déban l'utilisateur mentionné."""
    await ctx.guild.unban(member)
    await ctx.send(f"{member.mention} a été débanni.")

# Commande: +reset
async def reset(ctx):
    """Supprime tous les messages d'un salon."""
    await ctx.channel.purge()
    await ctx.send("🧹 Tous les messages du salon ont été supprimés !")
