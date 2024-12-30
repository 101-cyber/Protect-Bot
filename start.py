import discord
from discord.ext import commands
import os
from config import TOKEN
from commands import (
    giveaway as giveaway_command,
    reroll as reroll_command,
    list as list_command,
    lock as lock_command,
    unlock as unlock_command,
    bl as bl_command,
    wl as wl_command,
    reset as reset_command,
)
import moderation
from keep_alive import keep_alive

# Intents et bot
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="+", intents=intents)

moderation.setup_moderation(bot)  # Appel de setup_moderation

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.command()
async def test(ctx):
    """Commande pour tester si le bot répond."""
    await ctx.send("Le bot fonctionne !")

@bot.command()
async def giveaway(ctx, num_winners: int, prize: str, duration: int):
    await giveaway_command(ctx, num_winners, prize, duration)

@bot.command()
async def reroll(ctx):
    await reroll_command(ctx)

@bot.command()
async def list(ctx):
    await list_command(ctx)

@bot.command()
async def lock(ctx):
    await lock_command(ctx)

@bot.command()
async def unlock(ctx):
    await unlock_command(ctx)

@bot.command()
async def bl(ctx, user_id: int):
    await bl_command(ctx, user_id)

@bot.command()
async def wl(ctx, user_id: int):
    await wl_command(ctx, user_id)

@bot.command()
async def reset(ctx):
    await reset_command(ctx)

keep_alive()
bot.run(TOKEN)
