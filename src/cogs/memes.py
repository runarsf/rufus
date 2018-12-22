""" memes -- rufus.py """
"""import asyncio"""
import random
import os.path

from discord.ext import commands

class Memes:
    """ memes lol """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def kms(self, ctx):
        """ End it all.
        """
        await self.bot.send_file(ctx.message.channel, 'img/anoose.jpg')
        await self.bot.say('Come ' + ctx.message.author.mention +
                           '. *~~She~~* He\'s waiting for you!')

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

def setup(bot):
    """ defines setup """
    bot.add_cog(Memes(bot))
