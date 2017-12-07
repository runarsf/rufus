import asyncio
import random
import pickle
import aiohttp
import os
import lxml.html as l
import discord
from discord.ext import commands
from config import token

# https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html

bot_prefix = '>'
description = 'Descropt'

bot = discord.Client()
client = commands.Bot(description=description, command_prefix=bot_prefix)

@client.event
async def on_ready():
    """ Returns true if bot is ready """
    print('Logged in')
    print('Name :: {}'.format(client.user.name))
    print('ID :: {}'.format(client.user.id))
    print(discord.__version__)

    await client.change_presence(game=discord.Game(name='>help for help'))

@client.command(pass_context=True)
async def ping(ctx):
    """ Pings the bot host """
    await client.say('pong')

@client.command(pass_context=True)
async def roll(ctx):
    """ Rolls a dice """
    roll = random.choice(['1', '2', '3', '4', '5', '6'])
    await client.say('```' + client.user.name + ' rolled ' + roll + '```')

@client.command(pass_context=True)
async def flip(ctx):
    """ Flips a coin """
    flip = random.choice(['Heads', 'Tails'])
    await client.say('```' + flip + '```')

client.run(token)
