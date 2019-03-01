""" admin -- rufus.py """
import discord
import os
import re
import whois
import time
from cogs import runners
from cogs import uptime
from discord.ext import commands
import config as c


class DevCog(commands.Cog, name="Dev"):
    """ DevCog """

    def __init__(self, bot):
        self.bot = bot
        self.startTime = int(time.time())

    @commands.command(name='ping', aliases=['latency'])
    async def _ping(self, ctx):
        """ Ping the bot host.
        """
        await ctx.send(f'`` {int(float(round(self.bot.latency, 1))*1000)}ms ``: pong 🏓')

    @commands.command(name='uptime')
    async def _uptime(self, ctx):
        """ Shows the uptime of the bot.
        """
        current_time = int(time.time())
        upfor = uptime.ReadableTime(self.startTime, current_time)
        await ctx.send(f'I\'ve been up for *{upfor}*.')

    @commands.command(name='pwd')
    @commands.is_owner()
    async def _directory(self, ctx):
        """ Print Working Directory.
        """
        path = (os.path.dirname(os.path.realpath(__file__)))
        await ctx.send(path)

    @commands.command(name='whois', aliases=['lookup'])
    async def _whois(self, ctx, *, domains: str):
        domains = domains.split(', ')
        for dom in domains:
            domain = whois.query(dom)
            await ctx.send(domain.name, domain.registrar)

    @commands.command(name='bug')
    async def _bug(self, ctx):
        await ctx.send('Submit a bug: https://github.com/runarsf/rufus/issues/new')

    @commands.command(name='run', aliases=['runner'])
    @commands.is_owner()
    async def _runner(self, ctx, customLimit: int = 2):
        """ Run the most recent code block written by you.
            Custom limit may not exceed 50 messages.
        """
        counter = 0
        languages = ['python', 'py']
        if customLimit > 50:
            customLimit = 50
            await ctx.send('```Custom limit may not exceed 50 messages, reduced to 50.```')
        async for message in ctx.channel.history(limit=int(customLimit)):
            if message.content.startswith('```') and message.content.endswith('```') and message.author.id == ctx.message.author.id:
                lang = str(re.findall(r'^\w+[^\n]', message.content[3:-3])).strip('[\',]')
                if any(lin in lang for lin in languages):
                    if lang == 'python' or 'py':
                        build = runners.python(message)
                        await ctx.send(build)
                    return
                else:
                    await ctx.send('```No supported languages detected in header.```')
                    return
            counter += 1


def setup(bot):
    bot.add_cog(DevCog(bot))
