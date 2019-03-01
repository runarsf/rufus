""" admin -- rufus.py """

from discord.ext import commands


class EngineCog(commands.Cog, name="Search Engines"):
    """ EngineCog """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='genius', aliases=['lyrics'])
    async def _genius(self, ctx, *, content):
        """ Search Genius for lyrics
        """
        await ctx.send(f'https://genius.com/search?q={content.replace(" ", "%20")}')

    @commands.command(name='fandom')
    async def _fandom(self, ctx, *, content):
        """ Search Fandom for stuff.
        """
        await ctx.send(f'http://fandom.wikia.com/?s={content.replace(" ", "+")}')

    @commands.command(name='lmgtfy')
    async def _lmgtfy(self, ctx, *, content):
        """ Let Me Google That For You.
        """
        await ctx.send(f'http://lmgtfy.com/?q={content.replace(" ", "+")}')

def setup(bot):
    bot.add_cog(EngineCog(bot))
