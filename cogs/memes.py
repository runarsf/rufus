""" memes -- rufus.py """
import asyncio
# unused import subprocess
# unused import sys
# unused import os
import random
import config as c

# unused import discord
from discord.ext import commands

class Memes:
    """ memes lol """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def meme(self, ctx, meem: str):
        """*>help meme* for meme list
            >meme <meme>
			tocch, balls, drincc, tangerine, obliterate, swivel, nick, improvise, sipp, shockening, cucc, dipp, disgois, encontlepedie, frot, frotiverse, knowlage, meet, onion, rubix, shanpe, sitt, sooc, vegetables, vegetal, ballad, sippu, babsooc, angery, coak 
        """
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

    @commands.command()
    async def brainpower(self):
        """ OwO wat dis?
            >brainpower
        """
        await self.bot.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-')
        await self.bot.say('A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A- JO-ooo-oo-oo-oo' +
                           '\nEEEEO-A-AAA-AAAA')
        await self.bot.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-' +
                           '\nA-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-' +
                           '\nJO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA')
        await self.bot.say('O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-' +
                           '\nA-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-')
        await self.bot.say('JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA-O----------')

    @commands.command(pass_context=True)
    async def kms(self, ctx):
        """ End it all.
            >kms
        """
        await self.bot.send_file(ctx.message.channel, 'img/anoose.jpg')
        await self.bot.say('Come ' + ctx.message.author.mention +
                           '. *~~She~~* He\'s waiting for you!')

    @commands.command(pass_context=True)
    async def kys(self, ctx, *, user: str):
        """ Please be cautious when using this command.
            >kys <@user>
        """
        await self.bot.say('Hey ' + user + '. ' +
                           ctx.message.author.name + ' Is implying *he/she/it/social ' +
                           'construct* wants you to cease existing, however, ' +
                           'for their will to be fulfilled, ' +
                           'the death needs to be inflicted by yourself and yourself alone.')
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def chuchu(self):
        """ Kanna is waifu, cuz age is just a number.
            >chuchu
        """
        await self.bot.say('*YEA!*')

    @commands.command(pass_context=True)
    async def pooser(self, ctx):
        """ Why the fuq did I implement this?
            >pooser
        """
        await self.bot.send_file(ctx.message.channel, 'img/pooser.png')
        await self.bot.say('OwO wat dis?')
        asyncio.sleep(4)
        await self.bot.send_file(ctx.message.channel, 'img/poosna.png')
        await self.bot.say('It are his lips you porv.')
        asyncio.sleep(4)
        await self.bot.send_file(ctx.message.channel, 'img/ramboozled.png')
        await self.bot.say('jk it am the handees of the Re:0*GB* Ram')

    @commands.command()
    async def tocch(self):
        """ DOON NOTT TOCCH S P A G O O T
        """
        await self.bot.say('https://www.youtube.com/watch?v=cE1FrqheQNI DOON NOTT')

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
