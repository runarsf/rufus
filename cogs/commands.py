""" commands -- rufus.py """
import random
import asyncio
import math
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
        """ Pings the bot host.
            >ping
        """
        await self.bot.say('pong 🏓')

    @commands.command(pass_context=True)
    async def len(self, ctx):
        """ Finds length of string.
            >len <string>
        """
        mcont = ctx.message.content
        delta = mcont.replace(c.prefix + 'len ', '')
        await self.bot.say('``' + str(len(delta)) + '``')

    @commands.command(pass_context=True)
    async def roll(self, ctx):
        """ Rolls a random number. (0-100)
            >roll
        """
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
        """ Flips a coin.
            >flip
        """
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
    async def btc(self):
        """ Shows BitCoin price in USD.
            >btc
        """
        await self.bot.say('```' + 'BTC price is currently at $' + BTC_USD + ' USD' + '```')

    @commands.command(pass_context=True)
    async def poke(self, ctx):
        """ >:c
            >poke <@user> :message
        """
        mcont = ctx.message.content
        if mcont == c.prefix + 'poke':
            await self.bot.say('GRRR..')
        elif c.prefix + 'poke :' in mcont:
            await self.bot.say('*' + ctx.message.author.name +
                               ' poked' + mcont.replace(c.prefix + 'poke', '*').replace(':', ''))
            await self.bot.delete_message(ctx.message)
        else:
            await self.bot.say('*' + ctx.message.author.name +
                               ' poked' + mcont.replace(c.prefix + 'poke', '*'))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def hug(self, ctx):
        """ <3
            >hug <@user>
        """
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
    async def lenny(self, ctx):
        """ Sends lennyface to the current channel.
            >lenny
        """
        await self.bot.say('( ͡° ͜ʖ ͡°)')
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def infuh(self, ctx):
        """ Shows information about the specified user.
            >info <@user>
        """
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
    async def info(self, infm: str):
        """ Shows information about the specified user.
            >info <@user>
        """
        userid = infm.replace('<@', '').replace('>', '')
        raise Exception('*Not enough arguments*')

    @commands.command()
    async def genius(self, *, this):
        """ Search Genius for lyrics
        """
        await self.bot.say ('https://genius.com/search?q=' + this.replace(' ', '%20'))
		

def setup(bot):
    """ defines setup """
    bot.add_cog(Commands(bot))
