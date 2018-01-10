""" admin -- rufus.py """
import os
import config as c

# unused import discord
from discord.ext import commands


class osu:
    """ osu! commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def osu(self, *, this):
        """ osu! commandShit
        """
        if 'map ' in this:
            await self.bot.say ('https://osu.ppy.sh/p/beatmaplist?q=' + this.replace('map ', '').replace(' ', '%20'))
        if 'users ' in this:
            await self.bot.say('https://osu.ppy.sh/u/' + this.replace('user ', '').replace(' ', '%20'))
        if 'user ' in this:
            await self.bot.say('https://osu.ppy.sh/users/' + this.replace('user ', '').replace(' ', '%20'))
        if '!u ' in this:
            await self.bot.say('https://ameobea.me/osutrack/user/' + this.replace('!u ', '').replace(' ', '%20'))


def setup(bot):
    """ defines setup """
    bot.add_cog(osu(bot))
