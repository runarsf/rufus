# pip install -r requirements.txt
""" . """
import random
import time
import commands as cmd
import requests
import config as c
import discord
from discord.ext import commands

BTC_URL = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
DATA = requests.get(BTC_URL).json()
BTC_USD = DATA['bpi']['USD']['rate']
"""
class MyClass():
    def log(ctx):
        print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)

CON = MyClass()
"""
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

@client.command(pass_context=True)
async def test(ctx):
    """ You probably shouldn't use this... """
    CON.log
    await client.say(client.user.id)

@client.command(pass_context=True)
async def ping(ctx):
    """ Pings the bot host """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.say('pong 🏓')

@client.command(pass_context=True)
async def roll(ctx):
    """ Rolls a random number (0-100) """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
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
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    cflip = random.choice(['Heads', 'Tails'])
    if cflip == 'Heads':
        await client.add_reaction(ctx.message, '🇭')
        await client.add_reaction(ctx.message, '🇪')
        await client.add_reaction(ctx.message, '🇦')
        await client.add_reaction(ctx.message, '🇩')
        await client.add_reaction(ctx.message, '🇸')
    elif cflip == 'Tails':
        await client.add_reaction(ctx.message, '🇹')
        await client.add_reaction(ctx.message, '🇦')
        await client.add_reaction(ctx.message, '🇮')
        await client.add_reaction(ctx.message, '🇱')
        await client.add_reaction(ctx.message, '🇸')

@client.command(pass_context=True)
async def brainpower(ctx):
    """ OwO wat dis"""
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
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
async def btc(ctx):
    """ Shows BitCoin price in USD """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.say('``' + 'BTC price is currently at $' + BTC_USD + ' USD' + '``')

@client.command(pass_context=True)
async def poke(ctx):
    """ >:c """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    mcont = ctx.message.content
    if mcont == c.prefix + 'poke':
        await client.say('GRRR..')
    else:
        await client.say('*' + ctx.message.author.name +
                         ' poked' + mcont.replace(c.prefix + 'poke', '*'))
        await client.delete_message(ctx.message)

@client.command(pass_context=True)
async def hug(ctx):
    """ <3 """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    mcont = ctx.message.content
    if mcont <= c.prefix + 'hug':
        await client.say('*' + ctx.message.author.name + ' tries to hug the air*')
        await client.say('https://www.youtube.com/watch?v=CCVdQ8xXBfk')
        await client.say('*AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA*')
    elif mcont == c.prefix + 'hug <@' + client.user.id + '>':
        await client.say(' OwO wat dis? Am I being hugger? Hmmmm... always be a mystery it will')
    else:
        await client.say(ctx.message.author.name + ' hugged'
                         + mcont.replace(c.prefix + 'hug', '') + ' :hearts:')
        await client.delete_message(ctx.message)

@client.command(pass_context=True)
async def send(ctx):
    """ Sends the message specified by the user. """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    mcont = ctx.message.content
    await client.say(mcont.replace(c.prefix + 'send', ''))
    await client.delete_message(ctx.message)

@client.command(pass_context=True)
async def lenny(ctx):
    """ ( ͡° ͜ʖ ͡°) """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.say('( ͡° ͜ʖ ͡°)')

@client.command(pass_context=True)
async def tocch(ctx):
    """ DOON NOTT TOUCH SPAGOOT """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.add_reaction(ctx.message, '🍝')
    await client.send_file(ctx.message.channel, 'img/tocch.png')

@client.command(pass_context=True)
async def balls(ctx):
    """ ... """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.send_file(ctx.message.channel, 'img/balls.png')

@client.command(pass_context=True)
async def drincc(ctx):
    """ i am DEHYDRATION """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.send_file(ctx.message.channel, 'img/drincc.jpg')

@client.command(pass_context=True)
async def tangerine(ctx):
    """ tAnGeRiNe eS mIsSin atOM? """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.send_file(ctx.message.channel, 'img/tangerine.png')

@client.command(pass_context=True)
async def kms(ctx):
    """ hey bows do the kys pleas """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.send_file(ctx.message.channel, 'img/anoose.jpg')
    await client.say('Come ' + ctx.message.author.mention + '. *~~She~~* He\'s waiting for you!')

@client.command(pass_context=True)
async def kys(ctx):
    """ yes pelase """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    mcont = ctx.message.content
    if mcont == str(c.prefix + 'kys'):
        await client.delete_message(ctx.message)
        print('command.kys :: no argument')
    else:
        await client.say('Hey' + mcont.replace(c.prefix + 'kys', '') + '. ' +
                         ctx.message.author.name + ' Is implying *he/she/it/social construct* ' +
                         'wants you to cease existing, however, for their argument to apply, ' +
                         'the death needs to be inflicted by yourself and yourself alone.')
        await client.delete_message(ctx.message)

@client.command(pass_context=True)
async def chuchu(ctx):
    """ Kanna is waifu, cuz age is just a number. """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.say('YEA!')

@client.command(pass_context=True)
async def pooser(ctx):
    """ Why the fuq did I implement this? """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.send_file(ctx.message.channel, 'img/pooser.png')
    await client.say('OwO wat dis?')
    time.sleep(4)
    await client.send_file(ctx.message.channel, 'img/poosna.png')
    await client.say('It are his lips you porv.')
    time.sleep(4)
    await client.send_file(ctx.message.channel, 'img/ramboozled.png')
    await client.say('jk it am the handees of the Re:0*GB* Ram')

@client.command(pass_context=True)
async def deathnote(ctx):
    """ kys """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    await client.say('Say hello')
    await client.waiting(author=ctx.message.author, content='hello')
    await client.say(ctx.message.channel, 'Hello.')

@client.command(pass_context=True)
async def purge(ctx):
    """ Deletes the messages of the specified user. """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    mcont = ctx.message.content
    if mcont == str(c.prefix + 'purge'):
        await client.delete_message(ctx.message)
        print('command.purge :: no argument')
    elif mcont == c.prefix + 'purge all':
        await client.send_message(ctx.message.channel, 'Clearing messages...')
        time.sleep(2)
        async for msg in client.logs_from(ctx.message.channel):
            await client.delete_message(msg)
    else:
        print('purge error.else')

@client.command(pass_context=True)
async def info(ctx):
    """ Shows information about the specified user. """
    print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
    mcont = ctx.message.content
    userid = str(mcont.replace(c.prefix + 'info <@', '').replace('>', ''))

    embed = discord.Embed(title="Tile", description="Desc", color=0x3b4d7c)
    embed.add_field(name="Fiel1", value="hi", inline=False)
    embed.add_field(name="Field2", value="hi2", inline=False)

    print(userid)
    if mcont == str(c.prefix + 'info'):
        await client.say('Mention = {}'.format(ctx.message.author.mention) +
                         '\nID = ' + ctx.message.author.id)
        await client.say(ctx.message.channel, embed=embed)
    elif mcont == c.prefix + 'info <@' + client.user.id + '>':
        print('suh')
    elif c.prefix + 'info <@' in mcont:
        await client.say('Mention = ' + mcont.replace(c.prefix + 'info', '') + '\nID = ' + userid)

    else:
        await client.say('It would help if... you know.. the mention was. VALID...')

client.run(c.token)
