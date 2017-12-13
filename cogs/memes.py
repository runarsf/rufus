""" memes -- rufus.py """
import asyncio
# unused import subprocess
# unused import sys
# unused import os
import config as c

# unused import discord
from discord.ext import commands

class Memes:
    """ memes lol """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def meme(self, ctx, meem: str):
        """
        '>help memes' for meme list

        ::tocch
        ::balls
        ::drincc
        ::tangerine
        ::obliterate
        ::swivel
        ::nick
        ::improvise
        ::sipp
        ::shockening
        ::cucc
        ::dipp
        ::disgois
        ::encontlepedie
        ::frot
        ::frotiverse
        ::knowlage
        ::meet
        ::onion
        ::rubix
        ::shanpe
        ::sitt
        ::sooc
        ::vegetables
        ::vegetal
        ::ballad
        ::sippu
        ::babsooc
        ::angery
        ::coak
        """
        reacts = []
        try:
            if meem == 'tocch':
                await self.bot.add_reaction(ctx.message, '🍝')
                await self.bot.send_file(ctx.message.channel, 'img/memes/tocch.png')
            elif meem == 'balls':
                await self.bot.send_file(ctx.message.channel, 'img/memes/balls.png')
            elif meem == 'drincc':
                await self.bot.send_file(ctx.message.channel, 'img/memes/drincc.jpg')
            elif meem == 'tangerine':
                await self.bot.send_file(ctx.message.channel, 'img/memes/tangerine.png')
            elif meem == 'obliterate':
                await self.bot.send_file(ctx.message.channel, 'img/memes/obliterate.png')
            elif meem == 'swivel':
                await self.bot.send_file(ctx.message.channel, 'img/memes/swivel.png')
            elif meem == 'nick':
                await self.bot.send_file(ctx.message.channel, 'img/memes/nick.jpg')
            elif meem == 'improvise':
                await self.bot.send_file(ctx.message.channel, 'img/memes/improvise.jpg')
            elif meem == 'sipp':
                await self.bot.send_file(ctx.message.channel, 'img/memes/sipp.png')
            elif meem == 'shockening':
                await self.bot.send_file(ctx.message.channel, 'img/memes/shockening.png')
            elif meem == 'cucc':
                await self.bot.send_file(ctx.message.channel, 'img/memes/cucc.png')
            elif meem == 'dipp':
                await self.bot.send_file(ctx.message.channel, 'img/memes/dipp.jpg')
            elif meem == 'disgois':
                await self.bot.send_file(ctx.message.channel, 'img/memes/disgois.png')
            elif meem == 'encontlepedie':
                await self.bot.send_file(ctx.message.channel, 'img/memes/encontlepedie.png')
            elif meem == 'frot':
                await self.bot.send_file(ctx.message.channel, 'img/memes/frot.png')
            elif meem == 'frotiverse':
                await self.bot.send_file(ctx.message.channel, 'img/memes/frotiverse.png')
            elif meem == 'knowlage':
                await self.bot.send_file(ctx.message.channel, 'img/memes/knowlage.png')
            elif meem == 'meet':
                await self.bot.send_file(ctx.message.channel, 'img/memes/meet.png')
            elif meem == 'onion':
                await self.bot.send_file(ctx.message.channel, 'img/memes/onion.jpg')
            elif meem == 'rubix':
                await self.bot.send_file(ctx.message.channel, 'img/memes/rubix.jpg')
            elif meem == 'shanpe':
                await self.bot.send_file(ctx.message.channel, 'img/memes/shanpe.png')
            elif meem == 'sitt':
                await self.bot.send_file(ctx.message.channel, 'img/memes/sitt.png')
            elif meem == 'sooc':
                await self.bot.send_file(ctx.message.channel, 'img/memes/sooc.jpg')
            elif meem == 'vegetables':
                await self.bot.send_file(ctx.message.channel, 'img/memes/vegetables.png')
            elif meem == 'vegetal':
                await self.bot.send_file(ctx.message.channel, 'img/memes/vegetal.jpg')
            elif meem == 'ballad':
                await self.bot.send_file(ctx.message.channel, 'img/memes/ballad.png')
            elif meem == 'sippu':
                await self.bot.send_file(ctx.message.channel, 'img/memes/sippu.jpg')
            elif meem == 'babsooc':
                await self.bot.send_file(ctx.message.channel, 'img/memes/babsooc.png')
            elif meem == 'angery':
                await self.bot.send_file(ctx.message.channel, 'img/memes/angery.jpg')
            elif meem == 'coak':
                await self.bot.send_file(ctx.message.channel, 'img/memes/coak.jpg')
            else:
                await self.bot.say('GRRR.. ' + meem + ' IS NOT A MEEM')
        except:
            self.bot.say('wondering wHY yuou no typey Th MeEEm nam?')

def setup(bot):
    """ defines setup """
    bot.add_cog(Memes(bot))
