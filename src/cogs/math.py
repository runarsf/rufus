""" math -- rufus.py """
import math


from discord.ext import commands

class Math(commands.Cog, name="Math"):
    """ Math commands. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, float1: float, float2: float):
        """ Adds two numbers together.
        """
        await self.bot.say(float1 + float2)

    @commands.command()
    async def sub(self, float1: float, float2: float):
        """ Subtracts two numbers.
        """
        await self.bot.say(float1 - float2)

    @commands.command()
    async def mult(self, float1: float, float2: float):
        """ Multiplies two numbers.
        """
        await self.bot.say(float1 * float2)

    @commands.command()
    async def div(self, float1: float, float2: float):
        """ Divides two numbers.
        """
        try:
            await self.bot.say(float1 / float2)
        except ZeroDivisionError:
            await self.bot.say('GRRR..')

    @commands.command()
    async def sqrt(self, float: float):
        """ Sends the square root of the stated number.
        """
        await self.bot.say(math.sqrt(float))

    @commands.command()
    async def exp(self, float1: float, float2: float):
        """ Expenponderlates a number with another.
        """
        await self.bot.say(float1 ** float2)

    @commands.command()
    async def pi(self):
        """ Sends pi.
        """
        await self.bot.say(math.pi)


def setup(bot):
    """ defines setup """
    bot.add_cog(Math(bot))
