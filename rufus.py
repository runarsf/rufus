# pip install -r requirements.txt
""" . """
# unused import asyncio
import random
import aiohttp
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
client = commands.Bot(description=c.description, command_prefix=c.prefix)

@client.event
async def on_ready():
    """ Returns true if bot is ready """
    print('Logged in as')
    print('Name :: {}'.format(client.user.name))
    print('ID :: {}'.format(client.user.id))
    print(discord.__version__)

    await client.change_presence(game=discord.Game(name=c.game))

@client.command(pass_context=True)
async def ping():
    """ Pings the bot host """
    await client.say('pong 🏓')

@client.command(pass_context=True)
async def roll(ctx):
    """ Rolls a random number (0-100) """
    droll = random.randint(0, 100)
    if droll <= 0:
        await client.say('```' + ctx.message.author.name +
                         ' rolls ' + str(droll) + ' point(s)' + '```')
        await client.say('You need to git gud, rolling isn\'t a joke -.-')
    elif droll == 100:
        await client.say('```' + ctx.message.author.name +
                         ' rolls ' + str(droll) + ' point(s)' + '```')
        await client.say('GG!')
    else:
        await client.say('```' + ctx.message.author.name +
                         ' rolls ' + str(droll) + ' point(s)' + '```')

@client.command(pass_context=True)
async def flip(ctx):
    """ Flips a coin """
    cflip = random.choice(['Heads', 'Tails'])
    #await client.say('```' + flip + '```')
    if cflip == 'Heads':
        await client.add_reaction(ctx.message, '🇭')
        await client.add_reaction(ctx.message, '🇪')
        await client.add_reaction(ctx.message, '🇦')
        await client.add_reaction(ctx.message, '🇩')
        await client.add_reaction(ctx.message, '🇸')
    else:
        await client.add_reaction(ctx.message, '🇹')
        await client.add_reaction(ctx.message, '🇦')
        await client.add_reaction(ctx.message, '🇮')
        await client.add_reaction(ctx.message, '🇱')
        await client.add_reaction(ctx.message, '🇸')

@client.command(pass_context=True)
async def brainpower():
    """ OwO wat dis"""
    await client.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-')
    await client.say('A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A- JO-ooo-oo-oo-oo' +
                     '\nEEEEO-A-AAA-AAAA')
    await client.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-' +
                     '\nA-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-' +
                     '\nJO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA')
    await client.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-' +
                     '\nA-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-')
    await client.say('JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA-O----------')

@client.command(pass_context=True)
async def btc():
    """ Shows BitCoin price in USD """
    await client.say('``' + 'BTC price is currently at $' + btc_usd + ' USD' + '``')

@client.command(pass_context=True)
async def poke(ctx):
    """ >:c """
    mcont = ctx.message.content
    if mcont == c.prefix + 'poke':
        await client.say('GRRR..')
    else:
        await client.say('*' + ctx.message.author.name + ' poked' + mcont.replace(c.prefix + 'poke', '*'))

@client.command(pass_context=True)
async def info(ctx):
    """ Shows information about the specified user. """
    mcont = ctx.message.content
    if mcont == str(c.prefix + 'info'):
        await client.say('Mention = {}'.format(ctx.message.author.mention))
    elif c.prefix + 'info <@' in mcont:
        await client.say('Mention = ' + mcont.replace(c.prefix + 'info', ''))
    else:
        await client.say('It would help if... you know.. the mention was valid...')

@client.command(pass_context=True)
async def hug(ctx):
    """ <3 """
    mcont = ctx.message.content
    if mcont <= c.prefix + 'hug':
        await client.say('*' + ctx.message.author.name + ' tries to hug the air*')
        await client.say('https://www.youtube.com/watch?v=CCVdQ8xXBfk')
        await client.say('*AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA*')
    elif mcont == c.prefix + 'hug <@387390496038977536>':
        await client.say('')
    else:
        await client.say(ctx.message.author.name + ' hugged' + mcont.replace(c.prefix + 'hug', '') + ' :hearts:')

@client.command(pass_context=True)
async def send(ctx):
    """ Sends the message specified by the user. """
    mcont = ctx.message.content
    await client.say(mcont.replace(c.prefix + 'send', ''))

@client.command(pass_context=True)
async def lenny():
    """ ( ͡° ͜ʖ ͡°) """
    await client.say('( ͡° ͜ʖ ͡°)')

@client.command(pass_context=True)
async def tocch(ctx):
    """ DOO NOTT TOUCH SPAGOOT """
    await client.add_reaction(ctx.message, '🍝')
    await client.send_file(ctx.message.channel, 'tocch.png')
    
@client.command(pass_context=True)
async def balls(ctx):
    """ ... """
    await client.send_file(ctx.message.channel, 'balls.png')

@client.command(pass_context=True)
async def drincc(ctx):
    """ i am DEHYDRATION """
    await client.send_file(ctx.message.channel, 'drincc.jpg')

@client.command(pass_context=True)
async def tangerine(ctx):
    """ tAnGeRiNe eS mIsSin atOM? """
    await client.send_file(ctx.message.channel, 'tangerine.png')

@client.command(pass_context=True)
async def addbtc(ctx, create_custom_emoji):
    """ Adds the BitCoin emoji """
    dserver = client.get_server_id()
    await create_custom_emoji(dserver, 'BitCoin', 'btc.png')
    await client.say('done')

client.run(c.token)
