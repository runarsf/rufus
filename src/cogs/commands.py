""" commands -- rufus.py """
import random
import config as c
import requests
import os.path
import time

from discord.ext import commands


class Commands:
    """ commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def len(self, *, string: str):
        """ Find length of string.
        """
        await self.bot.say('``' + str(len(str(string))) + '``')

    @commands.command()
    async def chars(self, *, string: str):
        """ Find amount of characters in a string, excludes spaces.
        """
        await self.bot.say('``' + str(len(str(string).replace(' ', '').replace('　', ''))) + '``')

    @commands.command(pass_context=True)
    async def roll(self, *, max: int):
        """ Rolls a random number. Default: 0-100.
        """
        if max <= 0:
            max = 100;
        droll = random.randint(0, max)
        if droll == 1:
            suffix = ''
        else:
            suffix = 's'
        if droll <= 0:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point' + str(suffix) + '```')
            await self.bot.say('You need to git gud, rolling isn\'t a joke -.-')
        elif droll == 100:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point' + str(suffix) + '```')
            await self.bot.say('GG!')
        else:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point' + str(suffix) + '```')

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """ Flip a coin.
        """
        cflip = random.choice(['Heads', 'Tails'])
        if cflip == 'Heads':
            await self.bot.add_reaction(ctx.message, '⚪')
            await self.bot.add_reaction(ctx.message, '🇭')
            # await self.bot.add_reaction(ctx.message, '🇪')
            # await self.bot.add_reaction(ctx.message, '🇦')
            # await self.bot.add_reaction(ctx.message, '🇩')
            # await self.bot.add_reaction(ctx.message, '🇸')
        elif cflip == 'Tails':
            await self.bot.add_reaction(ctx.message, '⚫')
            await self.bot.add_reaction(ctx.message, '🇹')
            # await self.bot.add_reaction(ctx.message, '🇦')
            # await self.bot.add_reaction(ctx.message, '🇮')
            # await self.bot.add_reaction(ctx.message, '🇱')
            # await self.bot.add_reaction(ctx.message, '🇸')

    @commands.command()
    async def btc(self):
        """ Show BitCoin price in USD.
        """
        BTC_URL = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        DATA = requests.get(BTC_URL).json()
        BTC_USD = DATA['bpi']['USD']['rate']
        await self.bot.say('```' + 'BTC price is currently at $' + BTC_USD + ' USD' + '```')

    @commands.command(pass_context=True)
    async def poke(self, ctx, *, user: str):
        """ Poke user.
        """
        if user == '':
            await self.bot.say('GRRR..')
        elif user.startswith(':'):
            await self.bot.say('*{} poked {}*'.format(ctx.message.author.name, user))
            await self.bot.delete_message(ctx.message)
        else:
            await self.bot.say('No user named {}.'.format(user))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def hug(self, ctx, *, user: str):
        """ Hug user.
        """
        mcont = ctx.message.content
        if user == '':
            await self.bot.say('*' + ctx.message.author.name + ' tries to hug the air*')
        elif user == '<@{}>'.format(ctx.message.author.id):
            await self.bot.say('Aaaaaaall by myseeeeeeeelf.')
        elif user == '<@{}>'.format(self.bot.user.id):
            await self.bot.say(' OwO wat dis? Am I being hugger?' +
                               ' Hmmmm... always be a mystery it will')
        else:
            await self.bot.say('{} hugged {} :hearts:'.format(ctx.message.author.name, user))

    @commands.command()
    async def timer(self, *, seconds: int):
        """ Starts a countdown timer.
        """
        os = seconds
        msg = await self.bot.say('`` {} ``'.format(seconds))
        while seconds > 0:
            time.sleep(1)
            seconds -= 1
            await self.bot.edit_message(msg, '`` {} ``'.format(seconds))
        await self.bot.edit_message(msg, '`` Timer expired. ``')
        await self.bot.say('Time is up! {} seconds have passed.'.format(os))

    @commands.command(pass_context=True)
    async def invbot(self, ctx, *, userToInvite: str = message.author):
        invite = 'https://discordapp.com/oauth2/authorize?client_id=387390496038977536&scope=bot&permissions=2146958591'
        await self.bot.send_message(ctx.message.server.get_member_named(userToInvite), invite)
        await self.bot.say('Invite link sent to **{}**.'.format(ctx.message.server.get_member_named(userToInvite)))
"""
    @commands.command(pass_context=True)
    async def info(self, ctx, *, userMentioned: str = ''):
        \""" Shows information about the specified user.
        \"""
        try:
            await self.bot.say(userMentioned)
        except:
            await self.bot.say('It would help if, you know, the mention was.. VALID...')
"""

def setup(bot):
    """ defines setup """
    bot.add_cog(Commands(bot))
