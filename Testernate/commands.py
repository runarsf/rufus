import discord
from discord.ext import commands
import config as c

class Commands:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self):
        """ Pings the bot host """
        await self.bot.say('pong 🏓')

def setup(bot):
    bot.add_cog(Commands(bot))