import random
import os
import re
import discord
import asyncio
from discord.ext import commands

class MemesCog(commands.Cog, name="Memes"):
    """ MemesCog """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kms')
    async def _self_kill(self, ctx):
        """ End it all.
        """
        await ctx.send(file=discord.File(f'{str(os.path.dirname(os.path.realpath(__file__)))}/../img/anoose.jpg'))
        await ctx.send(f'Come {ctx.message.author.mention}. *~~He?~~* She\'s waiting for you!')

    @commands.command(name='lenny')
    async def _lennyface(self, ctx):
        """ Replaces user message with lennyface.
        """
        await ctx.send('( ͡° ͜ʖ ͡°)')
        await ctx.message.delete()

    @commands.command(name='kys')
    async def _member_kill(self, ctx, *, member: discord.Member = ''):
        """ Please be cautious when using this command.
        """
        await ctx.message.delete()
        await ctx.send(f'Hey {member}. {ctx.message.author.name} is implying *he/she/it/social construct*' +
                        'wants you to cease existing, however,' +
                        'for their will to be fulfilled,' +
                        'the death needs to be inflicted by yourself and yourself alone.')

    @commands.command(name='tocch', aliases=['touch'])
    async def _touch_spaghetti(self, ctx):
        """ DOON NOTT TOCCH S P A G O O T
        """
        channel = ctx.message.channel
        await ctx.message.add_reaction('🍝')
        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '🍝'
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.message.remove_reaction('🍝', self.bot.user)
        else:
            await channel.send('***DOON NOTT TOCCH S P A G O O T***')
            await ctx.message.remove_reaction('🍝', user)

    @commands.command(name='knuckles')
    async def _ugandan_knuckles(self, ctx):
        """ DO YOU KNO DE WAE?
        """
        knuckles = ['ALL HEIL DE QUEEN BRUDDERS',
                    '*spit*',
                    'WE MUST PROTECC DE QUEEN',
                    'DO YOU KNO DE WAE?',
                    'WE MUST RETURN TO UGANDA',
                    'YOU MUST BOW DOWN TO DE QUEEN',
                    'I DON\'T KNOW DE WAE',
                    'MY BRUDDERS THE QUEEN WILL MAKE A SPEECH',
                    'SPIT ON HIM',
                    'DO NOT DISRESPEC DE QUEEN',
                    'WHY AR U RUNNIN?'
		    ]
        await ctx.send(random.choice(knuckles))

    @commands.command(name='owo', aliases=['uwu'])
    async def _owo(self, ctx, *, message: str = 'owo'):
        """ owo~ify text.
        """
        owolist = ['(・`ω´・)', ';;w;;', ';w;', 'owo', 'OwO', 'Owo', 'owO', 'uwu', 'UwU', '>w<', '^w^']
        replacers = [',', '.', '!', '?']
        message = message.replace('l', 'w').replace('L', 'W').replace('r', 'w').replace('R', 'W')
        newmessage = message
        for index, letter in enumerate(str(message)):
            if letter in replacers:
                if str(message)[index-1:index] == ' ':
                    newmessage = newmessage.replace(letter, random.choice(owolist), 1)
                else:
                    newmessage = newmessage.replace(letter, f' {random.choice(owolist)}', 1)
        await ctx.send(f'```{newmessage}```')

    @commands.command(name='mock')
    async def _mock(self, ctx, *, string: str = ''):
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
            await ctx.send(f'```{outstr}```')

    @commands.command(name='pat')
    async def _pat(self, ctx, member: discord.Member = '', *, message: str = ''):
        """ Pat  uwu.
        """
        if member == '':
            await ctx.send('uwu')
        else:
            if message == '':
                await ctx.send(f'*{ctx.message.author.name} patted {member} and is probably a disgusting weeb!*')
            else:
                await self.bot.say(f'*{ctx.message.author.name} patted {member} {message}*')

    @commands.command(name='hug')
    async def _hug(self, ctx, *, member: discord.Member = ''):
        """ Hug user.
        """
        mcont = ctx.message.content
        if member == '':
            await ctx.send(f'*{ctx.message.author.name} tries to hug the air*')
        elif member == ctx.message.author:
            await ctx.send(random.choice(['Aaaaaaall by myseeeeeeeelf.', '*hugs you*']))
        elif member == self.bot.user:
            await ctx.send('OwO wat dis? Am I being hugger?')
        else:
            await ctx.send(f'{ctx.message.author.name} hugged {member} :hearts:')

def setup(bot):
    bot.add_cog(MemesCog(bot))
