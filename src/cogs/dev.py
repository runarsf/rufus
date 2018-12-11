""" admin -- rufus.py """
from discord.ext import commands
import getpass
import config as c
import os


class dev:
    """ dev stuff """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self):
        """ Pings the bot host.
            >ping
        """
        await self.bot.say('pong 🏓')

    @commands.command(pass_context=True)
    async def pwd(self, ctx):
        """ current osu! skin
        """
        userid = ctx.message.author.id
        if userid in str(c.owner_id) or str(c.dev_id) or str(c.admin_id):
            path = (os.path.dirname(os.path.realpath(__file__)))
            await self.bot.say(path)
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def clear(self, ctx):
        """ Clears the console.
            >clear
        """
        userid = ctx.message.author.id
        if userid in str(c.owner_id) or str(c.dev_id) or str(c.admin_id):
            clear = lambda: os.system('cls')
            clear()
            print('console cleared by {}'.format(ctx.message.author.name))
            await self.bot.delete_message(ctx.message)
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def cogs(self, ctx):
        """ Lists out all existing cogs
            >cogs
        """
        userid = ctx.message.author.id
        if userid in str(c.owner_id) or str(c.dev_id) or str(c.admin_id):
            for file in os.listdir('./cogs/'):
                if file.endswith('.py'):
                    await self.bot.say('' + file + '')
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command()
    async def bug(self):
        """ Submit a bug.
            >bug
        """
        await self.bot.say('Submit a bug: https://github.com/runarsf/rufus/issues/new')

def setup(bot):
    """ defines setup """
    bot.add_cog(dev(bot))
