import config as c

import os
import re
import whois
import time
import datetime

from pytz import timezone
from datetime import timezone
from cogs.utils import checks
from cogs.utils import runners
from cogs.utils import uptime

import discord
from discord.ext import commands


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

    @commands.command(name='echo', aliases=['say', 'print', 'printf'])
    @checks.is_dev()
    async def _echo(self, ctx, *, phrase: str):
        """ Make the bot say something.
        """
        await ctx.message.delete()
        await ctx.send(phrase)

    @commands.command(name='pwd')
    @checks.is_dev()
    async def _directory(self, ctx):
        """ Print Working Directory.
        """
        path = (os.path.dirname(os.path.realpath(__file__)))
        await ctx.send(path)

    @commands.command(name='friend', hidden=True)
    @checks.is_dev()
    async def _friend_me(self, ctx, *, member: discord.Member = ''):
        """ Send an outbound friend request to message author.
            This won't work unless it's a self-bot, which is prohibited by the TOS, this is purely for testing purposes.
        """
        if not member:
            member = ctx.message.author
        await member.send_friend_request()
        await ctx.send(f'Friend request sent to ``{member.name}``')

    @commands.command(name='whois', aliases=['lookup'])
    @checks.is_dev()
    async def _whois(self, ctx, *, domains: str):
        domains = domains.split(', ')
        for dom in domains:
            domain = whois.query(dom)
            await ctx.send(domain.name, domain.registrar)

    @commands.command(name='msgtime')
    async def _msgtime(self, ctx, id: int):
        """ Message creation date.
        """
        msg = await ctx.get_message(id)
        await ctx.send(f'Message was created at ``{msg.created_at}`` UTC')

    @commands.command(name='bug')
    async def _bug(self, ctx):
        await ctx.send('Submit a bug: https://github.com/runarsf/rufus/issues/new')

    @commands.command(name='old_runner', aliases=['runner'])
    @checks.is_dev()
    async def _old_runner(self, ctx, customLimit: int = 2):
        """ Run the most recent code block written by you.
            Custom limit may not exceed 50 messages.
        """
        await ctx.send('command runneded')
        return
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
