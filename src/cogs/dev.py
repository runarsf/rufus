import config as c

import os
import re
import whois
import time
import datetime

from pytz import timezone
from datetime import timezone
from cogs.utils import checks
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
        await ctx.send(f'pong 🏓 ``{self.bot.ws.latency * 1000:.0f}ms``')

    @commands.command(name='date', aliases=['time'])
    async def _datetime(self, ctx):
        """ Get datetetime.
        """
        await ctx.send(f'```apache\nLocal: {datetime.datetime.now()}\nUTC: {datetime.datetime.utcnow()}```')

    @commands.command(name='stats')
    async def _statistics(self, ctx):
        """ Get bot stats.
        """
        await ctx.send(f'pong 🏓 ``{self.bot.ws.latency * 1000:.0f}ms``')

    @commands.command(name='arr')
    async def _to_int_arr(self, ctx, *words):
        """ Convert word(s) to an integer array for use with swears (config).
        """
        output = ''
        for word in words:
            tarr = []
            for letter in word:
                tarr.append(ord(letter))
            output += ',\n'+str(tarr)
        await ctx.send(output[2:])

    @commands.command(name='uptime')
    async def _uptime(self, ctx):
        """ Shows the uptime of the bot.
        """
        current_time = int(time.time())
        upfor = uptime.ReadableTime(self.startTime, current_time)
        await ctx.send(f'I\'ve been up for *{upfor}*.')

    @commands.command(name='echo', aliases=['say', 'print'])
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
        msg = await ctx.fetch_message(id)
        await ctx.send(f'Message was created at ``{msg.created_at}`` UTC')

    @commands.command(name='input')
    async def _wait_for_input(self, ctx):
        channel = ctx.message.channel
        await channel.send('Say hello!')
        def check(m):
            return m.content == 'hello' and m.channel == channel
        msg = await self.bot.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))  

    @commands.command(name='bug')
    async def _bug(self, ctx):
        await ctx.send('Submit a bug: https://github.com/runarsf/rufus/issues/new')


def setup(bot):
    bot.add_cog(DevCog(bot))
