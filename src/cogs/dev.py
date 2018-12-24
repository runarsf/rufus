""" admin -- rufus.py """
from discord.ext import commands
import getpass
import config as c
import os


class Dev:
    """ dev stuff """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self):
        """ Ping the bot host.
        """
        await self.bot.say('pong 🏓')

    @commands.command(pass_context=True)
    async def pwd(self, ctx):
        """ Print Working Directory.
        """
        if str(ctx.message.author.id) in str(c.owner_id) or str(c.dev_id):
            path = (os.path.dirname(os.path.realpath(__file__)))
            await self.bot.say(path)
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def clear(self, ctx):
        """ Clears the console.
            Windows only. Deprecated.
        """
        if str(ctx.message.author.id) in str(c.owner_id) or str(c.dev_id):
            clear = lambda: os.system('cls')
            clear()
            print('Console cleared by {}'.format(ctx.message.author.name))
            await self.bot.delete_message(ctx.message)
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def cogs(self, ctx):
        """ Lists out all existing cogs.
        """
        cogger=''
        if str(ctx.message.author.id) in str(c.owner_id) or str(c.dev_id):
            for file in os.listdir('./cogs'):
                if not file == 'uptime.py' and file.endswith('.py'):
                    cogger += (file+' ')
            self.bot.say('```{}```'.format(cogger))
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command()
    async def bug(self):
        """ Submit a bug.
        """
        await self.bot.say('Submit a bug: https://github.com/runarsf/rufus/issues/new')

def setup(bot):
    """ defines setup """
    bot.add_cog(Dev(bot))
