""" admin -- rufus.py """
from discord.ext import commands
import getpass
import config as c
import os


class dev:
    """ dev stuff """

    def __init__(self, bot):
        self.bot = bot
        self.startTime = int(time.time())

    @commands.command()
    async def ping(self):
        """ Ping the bot host.
        """
        await self.bot.say('pong 🏓')

    @commands.command(pass_context=True)
    async def pwd(self, ctx):
        """ Print Working Directory.
        """
        if ctx.message.author.id in str(c.owner_id) or str(c.dev_id):
            path = (os.path.dirname(os.path.realpath(__file__)))
            await self.bot.say(path)
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def clear(self, ctx):
        """ Clears the console.
            Windows only. Deprecated.
        """
        if ctx.message.author.id in str(c.owner_id) or str(c.dev_id):
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
        if ctx.message.author.id in str(c.owner_id) or str(c.dev_id):
            for file in os.listdir('./cogs/'):
                if file.endswith('.py'):
                    await self.bot.say('' + file + '')
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command()
    async def bug(self):
        """ Submit a bug.
        """
        await self.bot.say('Submit a bug: https://github.com/runarsf/rufus/issues/new')

    @commands.command(pass_context=True)
    async def uptime(self):
        """ Shows the uptime of the bot.
        """
        current_time = int(time.time())
        uptime = ReadableTime(self.startTime, current_time)
        await self.bot.say('I\'ve been up for *{}*.'.format(uptime))

def setup(bot):
    """ defines setup """
    bot.add_cog(dev(bot))

def ReadableTime(first, last):
    readTime = int(last-first)
    weeks   = int(readTime/604800)
    days    = int((readTime-(weeks*604800))/86400)
    hours   = int((readTime-(days*86400 + weeks*604800))/3600)
    minutes = int((readTime-(hours*3600 + days*86400 + weeks*604800))/60)
    seconds = int(readTime-(minutes*60 + hours*3600 + days*86400 + weeks*604800))
    msg = ''
    if weeks > 0:
        msg += '1 week, ' if weeks == 1 else '{:,} weeks, '.format(weeks)
    if weeks > 0:
        msg += "1 week, " if weeks == 1 else "{:,} weeks, ".format(weeks)
    if days > 0:
        msg += "1 day, " if days == 1 else "{:,} days, ".format(days)
    if hours > 0:
        msg += "1 hour, " if hours == 1 else "{:,} hours, ".format(hours)
    if minutes > 0:
        msg += "1 minute, " if minutes == 1 else "{:,} minutes, ".format(minutes)
    if seconds > 0:
        msg += "1 second, " if seconds == 1 else "{:,} seconds, ".format(seconds)
    if msg == "":
        return "0 seconds"
    else:
        return msg[:-2]
