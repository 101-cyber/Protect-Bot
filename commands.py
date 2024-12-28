import discord
from discord.ext import commands
from config import bot, message_logs
import time

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

# Commande: +lock
@bot.command()
@commands.has_permissions(manage_roles=True)
async def lock(ctx):
    role_name = "+"
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role_name)

    if role is None:
        await ctx.send(f"Le rôle `{role_name}` n'existe pas.")
        return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
        role: discord.PermissionOverwrite(send_messages=True),
    }

    for channel in guild.channels:
        await channel.set_permissions(target=guild.default_role, overwrite=overwrites[guild.default_role])
        await channel.set_permissions(target=role, overwrite=overwrites[role])

    await ctx.send("🔒 Salon verrouillé pour les utilisateurs sans le rôle `+`.")

# Commande: +unlock
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unlock(ctx):
    guild = ctx.guild

    for channel in guild.channels:
        await channel.set_permissions(target=guild.default_role, overwrite=None)

    await ctx.send("🔓 Salon débloqué pour tout le monde.")

# Commande: +ban
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🚫 {member.mention} a été banni définitivement. Raison : {reason}")
    except discord.Forbidden:
        await ctx.send("❌ Je n'ai pas les permissions nécessaires pour bannir cet utilisateur.")
    except discord.HTTPException as e:
        await ctx.send(f"⚠ Une erreur est survenue lors du bannissement : {e}")

# Commande: +reset
@bot.command()
@commands.has_permissions(manage_messages=True)
async def reset(ctx):
    try:
        await ctx.channel.purge()
        await ctx.send("🧹 Tous les messages de ce salon ont été supprimés.", delete_after=5)
    except discord.Forbidden:
        await ctx.send("❌ Je n'ai pas les permissions nécessaires pour supprimer les messages.")
    except discord.HTTPException as e:
        await ctx.send(f"⚠ Une erreur est survenue lors de la suppression : {e}")
