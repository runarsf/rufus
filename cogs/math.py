""" math -- rufus.py """
import math


from discord.ext import commands

class Math:
    """ Math commands. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, left: float, right: float):
        """ Adds two numbers together.
            >add <float1> <float2>
        """
        await self.bot.say(left + right)

    @commands.command()
    async def sub(self, left: float, right: float):
        """ Subtracts two numbers.
            >sub <float1> <float2>
        """
        await self.bot.say(left - right)

    @commands.command()
    async def mult(self, left: float, right: float):
        """ Multiplies two numbers.
            >mult <float1> <float2>
        """
        await self.bot.say(left * right)

    @commands.command()
    async def div(self, left: float, right: float):
        """ Divides two numbers.
            >div <float1> <float2>
        """
        try:
            await self.bot.say(left / right)
        except ZeroDivisionError:
            await self.bot.say('GRRR..')

    @commands.command()
    async def sqrt(self, bold: float):
        """ Sends the square root of the stated number.
            >sqrt <float>
        """
        await self.bot.say(math.sqrt(bold))

    @commands.command()
    async def friends(self):
        """ The amount of friends you have. Your mom doesn't count.
            >friends
        """
        await self.bot.say('0')

    @commands.command()
    async def exp(self, left: float, right: float):
        """ Expenponderlates a number with another.
            >mult <float1> <float2>
        """
        await self.bot.say(left ** right)

    @commands.command()
    async def pi(self):
        """ Sends pi.
            >pi
        """
        await self.bot.say(math.pi)


def setup(bot):
    """ defines setup """
    bot.add_cog(Math(bot))
