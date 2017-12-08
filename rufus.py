# pip install -r requirements.txt
# unused import asyncio
import random
# unused import aiohttp
# unused import pickle
# unused import os
import requests
import discord
import config as c
# unused from lxml import html
from discord.ext import commands

btc_url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
data = requests.get(btc_url).json()
btc_usd = data['bpi']['USD']['rate']

bot = discord.Client()
client = commands.Bot(description=c.description, command_prefix=c.bot_prefix)

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
    """ Rolls a random number (0-100) """
    roll = random.randint(0, 100)
    if roll <= 0:
        await client.say('```' + ctx.message.author.name + ' rolls ' + str(roll) + ' point(s)' + '```')
        await client.say('You need to git gud, rolling isn\'t a joke -.-')
    elif roll == 100:
        await client.say('```' + ctx.message.author.name + ' rolls ' + str(roll) + ' point(s)' + '```')
        await client.say('GG!')
    else:
        await client.say('```' + ctx.message.author.name + ' rolls ' + str(roll) + ' point(s)' + '```')

@client.command(pass_context=True)
async def flip(ctx):
    """ Flips a coin """
    flip = random.choice(['Heads', 'Tails'])
    await client.say('```' + flip + '```')

@client.command(pass_context=True)
async def brainpower(ctx):
    """ OwO wat dis"""
    await client.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-')
    await client.say('A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A- JO-ooo-oo-oo-oo' + '\nEEEEO-A-AAA-AAAA')
    await client.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-' + '\nA-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-' + '\nJO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA')
    await client.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-' + '\nA-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-')
    await client.say('JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA-O----------')

@client.command(pass_context=True)
async def btc(ctx):
    """ Shows BitCoin price in USD """
    await client.say('``' + 'BTC price is currently at $' + btc_usd + ' USD' + '``')

@client.command(pass_context=True)
async def poke(ctx):
    """ >:c """
    await client.say('GRRR..')

@client.command(pass_context=True)
async def info(ctx):
    """ Shows information about the specified user. """
    await client.say('```Mention     ::      {}'.format(ctx.message.author.mention + '\nName        ::      {}'.format(ctx.message.author.name + '\nID          ::      {}'.format(ctx.message.author.id + '```'))))

@client.command(pass_context=True)
async def hug(ctx):
    """ <3 """
    await client.say(ctx.message.author.name + ' hugged ' + ctx.message.author.name)

client.run(c.token)
