""" commands -- rufus.py """
import random
import config as c
import requests
import os.path
import time

from discord.ext import commands

BTC_URL = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
DATA = requests.get(BTC_URL).json()
BTC_USD = DATA['bpi']['USD']['rate']


class Commands:
    """ commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def len(self, *, msg: str):
        """ Finds length of string.
            >len <string>
        """
        await self.bot.say('``' + str(len(str(msg))) + '``')

    @commands.command()
    async def chars(self, *, msg: str):
        """ Finds amount of characters in a string. Excludes spaces.
            >chars <string>
        """
        await self.bot.say('``' + str(len(str(msg).replace(' ', '').replace('　', ''))) + '``')

    @commands.command(pass_context=True)
    async def roll(self, *, max: int):
        """ Rolls a random number. (0-100)
            >roll
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
        """ Flips a coin.
            >flip
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
        elif mcont == c.prefix + 'hug <@' + ctx.message.author.id + '>':
            await self.bot.say('Aaaaaaall by myseeeeeeeelf.')
        elif mcont == c.prefix + 'hug <@' + self.bot.user.id + '>':
            await self.bot.say(' OwO wat dis? Am I being hugger?' +
                               ' Hmmmm... always be a mystery it will')
        else:
            #await self.bot.delete_message(ctx.message)
            await self.bot.say(ctx.message.author.name + ' hugged'
                               + mcont.replace(c.prefix + 'hug', '') + ' :hearts:')

    @commands.command(pass_context=True)
    async def invite(self):
        await self.bot.say('https://discord.me/shindeiru/')

    @commands.command(pass_context=True)
    async def img(self, ctx, *, img: str):
        """ Send an image to a channel
            >img <root_path_to_img>
        """
        try:
            if os.path.exists('img/' + img + '.jpg'):
                await self.bot.send_file(ctx.message.channel, 'img/' + img + '.jpg')
            elif os.path.exists('img/' + img + '.png'):
                await self.bot.send_file(ctx.message.channel, 'img/' + img + '.png')
        except:
            await self.bot.say('No image named {}.'.format(img))

    @commands.command(pass_context=True)
    async def info(self, ctx, *, userMentioned: str):
        """ Shows information about the specified user.
            >info <Username#XXXX>
        """
        mend = ctx.message.server.get_member_named(userMentioned)
        try:
            mend = ctx.message.server.get_member_named(userMentioned)
            await self.bot.say(ctx.message.Object.created_at(userMentioned))
            await self.bot.say(str(userMentioned))
        except:
            await self.bot.say('It would help if... you know.. the mention was. VALID...')

    @commands.command()
    async def timer(self, *, s: int):
        """ Starts a countdown timer.
            >timer <seconds>
        """
        os = s
        msg = await self.bot.say('`` {} ``'.format(s))
        while s > 0:
            time.sleep(1)
            s -= 1
            await self.bot.edit_message(msg, '`` {} ``'.format(s))
        await self.bot.edit_message(msg, '`` Timer expired. ``')
        await self.bot.say('Time is up! {} seconds have passed.'.format(os))

    @commands.command()
    async def cur(self, *, inp: str):
        """ Converts one currency to another.
            >cur <amount><currency> to <currency>
        """
        r = requests.get('https://google.com/#q=' + inp.replace(" ", "+"))
        await self.bot.say(r.status_code)
        await self.bot.say(r.text)
        await self.bot.say(r.json())





def setup(bot):
    """ defines setup """
    bot.add_cog(Commands(bot))
