import discord
from discord.ext import commands
import os
from config import TOKEN
from commands import (
    giveaway,
    reroll,
    list,
    lock,
    unlock,
    bl,
    wl,
    reset,
)
from keep_alive import keep_alive

# Intents et bot
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.command()
async def test(ctx):
    """Commande pour tester si le bot répond."""
    await ctx.send("Le bot fonctionne !")

@bot.command()
async def giveaway(ctx, num_winners: int, prize: str, duration: int):
    await giveaway(ctx, num_winners, prize, duration)

@bot.command()
async def reroll(ctx):
    await reroll(ctx)

@bot.command()
async def list(ctx):
    await list(ctx)

@bot.command()
async def lock(ctx):
    await lock(ctx)

@bot.command()
async def unlock(ctx):
    await unlock(ctx)

@bot.command()
async def bl(ctx, member: discord.Member):
    await bl(ctx, member)

@bot.command()
async def wl(ctx, member: discord.Member):
    await wl(ctx, member)

@bot.command()
async def reset(ctx):
    await reset(ctx)

keep_alive()
bot.run(TOKEN)
