""" admin -- rufus.py """

from discord.ext import commands


class Engine(commands.Cog, name="Engine"):
    """ Different search engines. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def genius(self, *, content):
        """ Search Genius for lyrics
        """
        await self.bot.say('https://genius.com/search?q=' + content.replace(' ', '%20'))

    @commands.command()
    async def fandom(self, *, content):
        """ Search Fandom for stuff.
        """
        await self.bot.say('http://fandom.wikia.com/?s=' + content.replace(' ', '+'))

    @commands.command()
    async def lmgtfy(self, *, content):
        """ Let Me Google That For You.
        """
        await self.bot.say('http://lmgtfy.com/?q=' + content.replace(' ', '+'))

def setup(bot):
    """ defines setup """
    bot.add_cog(Engine(bot))
