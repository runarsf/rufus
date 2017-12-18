""" commands -- rufus.py """
import random
import asyncio
import math
# import subprocess
# import sys
import config as c
import requests

# unused import discord
from discord.ext import commands

BTC_URL = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
DATA = requests.get(BTC_URL).json()
BTC_USD = DATA['bpi']['USD']['rate']

class Commands:
    """ commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """ Pings the bot host. """
        print(ctx.message.author.name + ' ' + ctx.message.author.mention + ' :: ' + ctx.message.content)
        await self.bot.say('pong 🏓')

    @commands.command()
    async def add(self, left: float, right: float):
        """ Adds two numbers together. """
        await self.bot.say(left + right)

    @commands.command()
    async def div(self, left: float, right: float):
        """ Divides two numbers together. """
        try:
            await self.bot.say(left / right)
        except ZeroDivisionError:
            await self.bot.say('GRRR..')

    @commands.command(pass_context=True)
    async def roll(self, ctx):
        """ Rolls a random number (0-100) """
        droll = random.randint(0, 100)
        if droll <= 0:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point(s)' + '```')
            await self.bot.say('You need to git gud, rolling isn\'t a joke -.-')
        elif droll == 100:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point(s)' + '```')
            await self.bot.say('GG!')
        else:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point(s)' + '```')

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """ Flips a coin """
        cflip = random.choice(['Heads', 'Tails'])
        if cflip == 'Heads':
            await self.bot.add_reaction(ctx.message, '🇭')
            await self.bot.add_reaction(ctx.message, '🇪')
            await self.bot.add_reaction(ctx.message, '🇦')
            await self.bot.add_reaction(ctx.message, '🇩')
            await self.bot.add_reaction(ctx.message, '🇸')
        elif cflip == 'Tails':
            await self.bot.add_reaction(ctx.message, '🇹')
            await self.bot.add_reaction(ctx.message, '🇦')
            await self.bot.add_reaction(ctx.message, '🇮')
            await self.bot.add_reaction(ctx.message, '🇱')
            await self.bot.add_reaction(ctx.message, '🇸')

    @commands.command()
    async def brainpower(self):
        """ OwO wat dis"""
        await self.bot.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-')
        await self.bot.say('A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A- JO-ooo-oo-oo-oo' +
                           '\nEEEEO-A-AAA-AAAA')
        await self.bot.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-' +
                           '\nA-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-' +
                           '\nJO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA')
        await self.bot.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-' +
                           '\nA-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-')
        await self.bot.say('JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA-O----------')

    @commands.command()
    async def btc(self):
        """ Shows BitCoin price in USD """
        await self.bot.say('```' + 'BTC price is currently at $' + BTC_USD + ' USD' + '```')

    @commands.command(pass_context=True)
    async def poke(self, ctx):
        """ >:c """
        mcont = ctx.message.content
        if mcont == c.prefix + 'poke':
            await self.bot.say('GRRR..')
        else:
            await self.bot.say('*' + ctx.message.author.name +
                               ' poked' + mcont.replace(c.prefix + 'poke', '*'))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def hug(self, ctx):
        """ <3 """
        mcont = ctx.message.content
        if mcont <= c.prefix + 'hug':
            await self.bot.say('*' + ctx.message.author.name + ' tries to hug the air*')
            await self.bot.say('https://www.youtube.com/watch?v=CCVdQ8xXBfk')
            await self.bot.say('*AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA*')
        elif mcont == c.prefix + 'hug <@' + self.bot.user.id + '>':
            await self.bot.say(' OwO wat dis? Am I being hugger?' +
                               'Hmmmm... always be a mystery it will')
        else:
            await self.bot.say(ctx.message.author.name + ' hugged'
                               + mcont.replace(c.prefix + 'hug', '') + ' :hearts:')
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def send(self, ctx):
        """ Sends the message specified by the user. """
        mcont = ctx.message.content
        await self.bot.say(mcont.replace(c.prefix + 'send', ''))
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def lenny(self, ctx):
        """ ( ͡° ͜ʖ ͡°) """
        await self.bot.say('( ͡° ͜ʖ ͡°)')
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def kms(self, ctx):
        """ hey bows do the kys pleas """
        await self.bot.send_file(ctx.message.channel, 'img/anoose.jpg')
        await self.bot.say('Come ' + ctx.message.author.mention +
                           '. *~~She~~* He\'s waiting for you!')

    @commands.command(pass_context=True)
    async def kys(self, ctx):
        """ yes pelase """
        mcont = ctx.message.content
        if mcont == str(c.prefix + 'kys'):
            await self.bot.delete_message(ctx.message)
            print('command.kys :: no argument')
        else:
            await self.bot.say('Hey' + mcont.replace(c.prefix + 'kys', '') +
                               '. ' + ctx.message.author.name + ' Is implying *he/she/it/social' +
                               'construct* wants you to cease existing, however,' +
                               'for their argument to apply, ' +
                               'the death needs to be inflicted by yourself and yourself alone.')
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def chuchu(self):
        """ Kanna is waifu, cuz age is just a number. """
        await self.bot.say('*YEA!*')

    @commands.command(pass_context=True)
    async def pooser(self, ctx):
        """ Why the fuq did I implement this? """
        await self.bot.send_file(ctx.message.channel, 'img/pooser.png')
        await self.bot.say('OwO wat dis?')
        asyncio.sleep(4)
        await self.bot.send_file(ctx.message.channel, 'img/poosna.png')
        await self.bot.say('It are his lips you porv.')
        asyncio.sleep(4)
        await self.bot.send_file(ctx.message.channel, 'img/ramboozled.png')
        await self.bot.say('jk it am the handees of the Re:0*GB* Ram')

    @commands.command()
    async def sqrt(self, bold: float):
        """ Sends the square root of the stated number. """
        await self.bot.say(math.sqrt(bold))

    @commands.command(pass_context=True)
    async def infuh(self, ctx):
        """ Shows information about the specified user. """
        mcont = ctx.message.content
        userid = str(mcont.replace(c.prefix + 'info <@', '').replace('>', ''))

        print(userid)
        if mcont == str(c.prefix + 'info'):
            await self.bot.say('Mention = {}'.format(ctx.message.author.mention) +
                               '\nID = ' + ctx.message.author.id)
        elif mcont == c.prefix + 'info <@' + self.bot.user.id + '>':
            print('suh')
        elif c.prefix + 'info <@' in mcont:
            await self.bot.say('Mention = ' + mcont.replace(c.prefix + 'info', '')
                               + '\nID = ' + userid)

        else:
            await self.bot.say('It would help if... you know.. the mention was. VALID...')

    @commands.command(pass_context=True)
    async def info(self, ctx, infm: str):
        """ Shows information about the specified user. """
        userid = infm.replace('<@', '').replace('>', '')
        raise Exception('*Not enough arguments*')



def setup(bot):
    """ defines setup """
    bot.add_cog(Commands(bot))
