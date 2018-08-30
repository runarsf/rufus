""" admin -- rufus.py """
from discord.ext import commands


class osu:
    """ osu! commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def osu(self, cmd, *, msg):
        """ osu! commandShit
        """
        if cmd == 'map':
            await self.bot.say('https://osu.ppy.sh/p/beatmaplist?q=' + msg.replace(' ', '%20'))
        if cmd == 'user':
            await self.bot.say('https://osu.ppy.sh/users/' + msg.replace(' ', '%20'))


def setup(bot):
    """ defines setup """
    bot.add_cog(osu(bot))
