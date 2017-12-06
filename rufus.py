#import asyncio
""" Import asyncio """
import random
import pickle
import os
import aiohttp
import discord
from discord.ext import commands
import lxml.html as l
from config import token

bot_prefix = '>'
description = 'Descropt'

client = discord.Client()
bot = commands.Bot(command_prefix='>', description='Lol')

@client.event
async def on_ready():
    """ Returns true if bot is ready """
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------')
    await client.change_presence(game=discord.Game(name='>help for help'))

@client.event
async def on_message(message):
    """ All on_message functions """
	# Ping
    if message.content.startswith('>ping'):
        await client.send_message(message.channel, 'pong')

	# Rolls a dice
    if message.content.startswith('>roll'):
        roll = random.choice(['1', '2', '3', '4', '5', '6'])
        await client.send_message(message.channel, roll)

	# Add quote to quotes.pk1
    if message.content.startswith('>addquote'):
        if not os.path.isfile('quotes.pk1'):
            quote_list = []
        else:
            with open('quotes.pk1', 'rb') as quotes:
                quote_list = pickle.load(quotes)
        quote_list.append(message.content[9:])
        with open('quotes.pk1', 'wb') as quotes:
            pickle.dump(quote_list, quotes)

	# Get random quote from quotes.pk1
    if message.content.startswith('>quote'):
        with open('quotes.pk1', 'rb') as quotes:
            quote_list = pickle.load(quotes)
        await client.send_message(message.channel, random.choice(quote_list))

    # Help command
    if message.content.startswith('>help'):
        await client.send_message(message.channel, 'No contents')

    # Poke bot host
    if message.content.startswith('>poke'):
        await client.send_message(message.channel, 'GRRR..')

client.run(token)
