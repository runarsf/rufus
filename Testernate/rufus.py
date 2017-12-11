import config as c
import discord

from discord.ext import commands
from commands import Commands

BOT = discord.Client()
client = commands.Bot(description=c.description, command_prefix=c.prefix)

@client.event
async def on_ready():
    """ Returns true if bot is ready """
    print('Logged in as')
    print('Name :: {}'.format(client.user.name))
    print('ID :: {}'.format(client.user.id))
    print(discord.__version__)
    await client.change_presence(game=discord.Game(name=c.game))

commands.Commands

client.run(c.token)
