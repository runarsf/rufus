""" memes -- rufus.py """
"""import asyncio"""
import random
import os
import discord
from discord.ext import commands

from discord.ext import commands

class Memes(commands.Cog, name="Memes"):
    """ memes lol """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def kms(self, ctx):
        """ End it all.
        """
        await self.bot.send_file(ctx.message.channel, str("{}/../img/anoose.jpg".format(os.path.dirname(os.path.realpath(__file__)))))
        await self.bot.say('Come ' + ctx.message.author.mention +
                           '. *~~He?~~* She\'s waiting for you!')

    @commands.command(pass_context=True)
    async def lenny(self, ctx):
        """ Replaces user message with lennyface.
        """
        await self.bot.say('( ͡° ͜ʖ ͡°)')
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def kys(self, ctx, *, user: str):
        """ Please be cautious when using this command.
        """
        await self.bot.say('Hey ' + user + '. ' +
                           ctx.message.author.name + ' Is implying *he/she/it/social ' +
                           'construct* wants you to cease existing, however, ' +
                           'for their will to be fulfilled, ' +
                           'the death needs to be inflicted by yourself and yourself alone.')
        await self.bot.delete_message(ctx.message)

    #@commands.command(pass_context=True)
    #async def pooser(self, ctx):
    #    """ Why the actual f did I implement this?
    #    """
    #    await self.bot.send_file(ctx.message.channel, 'img/pooser.png')
    #    await self.bot.say('OwO wat dis?')
    #    asyncio.sleep(4)
    #    await self.bot.send_file(ctx.message.channel, 'img/poosna.png')
    #    await self.bot.say('It are his lips you porv.')
    #    asyncio.sleep(4)
    #    await self.bot.send_file(ctx.message.channel, 'img/ramboozled.png')
    #    await self.bot.say('jk it am the handees of the Re:0*GB* Ram')

    @commands.command(pass_context=True)
    async def tocch(self, ctx):
        """ DOON NOTT TOCCH S P A G O O T
        """
        await self.bot.add_reaction(ctx.message, '🍝')

    @commands.command()
    async def knuckles(self):
        """ DO YOU KNO DE WAE?
        """
        knuckles = ["ALL HEIL DE QUEEN BRUDDERS",
                    "*spit*",
                    "WE MUST PROTECC DE QUEEN",
                    "DO YOU KNO DE WAE?",
                    "WE MUST RETURN TO UGANDA",
                    "YOU MUST BOW DOWN TO DE QUEEN",
                    "I DON'T KNOW DE WAE",
                    "MY BRUDDERS THE QUEEN WILL MAKE A SPEECH",
                    "SPIT ON HIM",
                    "DO NOT DISRESPEC DE QUEEN",
                    "WHY AR U RUNNIN?"
					]
        await self.bot.say(random.choice(knuckles))

    @commands.command()
    async def owo(self, *, message: str = 'owo'):
        """ owo~ify something.
        """
        owolist = ['(・`ω´・)', ';;w;;', ';w;', 'owo', 'OwO', 'Owo', 'owO', 'uwu', 'UwU', '>w<', '^w^']
        message = message.replace('l', 'w').replace('L', 'W').replace('r', 'w').replace('R', 'W')
        message = message.replace(',', ' ' + random.choice(owolist)).replace('!', ' ' + random.choice(owolist)).replace('?', ' ' + random.choice(owolist))
        await self.bot.say('```{}```'.format(message))

    @commands.command()
    async def ss(self, *, message: str = ''):
        """ ss-ify something.
        """
        if message == '':
            message = 'ẞß'
        message = message.replace('ss', 'ß').replace('SS', 'ẞ').replace('sS', 'ß').replace('Ss', 'ẞ')
        await self.bot.say('```css\n{}```'.format(message))

    @commands.command()
    async def mock(self, *, string: str = ''):
        """ Convert string to mocking.
        """
        if string:
            i=1
            outstr=''
            for letter in string:
                if i % 2 == 0:
                    outstr+=letter.lower()
                else:
                    outstr+=letter.upper()
                i+=1
            await self.bot.say('*{}*'.format(outstr))

    @commands.command(pass_context=True)
    async def pat(self, ctx, user: discord.User = '', *, message: str = ''):
        """ Pat user uwu.
        """
        if user == '':
            await self.bot.say('uwu')
        else:
            if message == '':
                await self.bot.say('*{} patted {} and is probably a disgusting weeb!*'.format(ctx.message.author.name, user))
            else:
                await self.bot.say('*{} patted {} {}*'.format(ctx.message.author.name, user, message))

    @commands.command(pass_context=True)
    async def hug(self, ctx, *, user: str = ''):
        """ Hug user.
        """
        mcont = ctx.message.content
        if user == '':
            await self.bot.say('*{} tries to hug the air*'.format(ctx.message.author.name))
        elif user == 'me':
            await self.bot.say('*I hugged {}*'.format(ctx.message.author.name))
        elif user == '<@{}>'.format(ctx.message.author.id):
            await self.bot.say('Aaaaaaall by myseeeeeeeelf.')
        elif user == '<@{}>'.format(self.bot.user.id):
            await self.bot.say(' OwO wat dis? Am I being hugger?' +
                               ' Hmmmm... always be a mystery it will')
        else:
            await self.bot.say('{} hugged {} :hearts:'.format(ctx.message.author.name, user))

def setup(bot):
    """ defines setup """
    bot.add_cog(Memes(bot))
