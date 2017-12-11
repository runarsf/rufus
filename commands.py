# pip install -r requirements.txt
""" . """
import random
import time
import requests
import config as c
import discord
from discord.ext import commands

BOT = discord.Client()
client = commands.Bot(description=c.description, command_prefix=c.prefix)

@client.command(pass_context=True)
async def ping(ctx):
    """ Pings the bot host """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.say('pong 🏓')