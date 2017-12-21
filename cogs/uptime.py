import time
from discord.ext import commands
from cogs import utils


class Utils:
    def __init__(self, bot):
        self.bot = bot
        self.startTime = int(time.time())

    @commands.command(pass_context=True)
    async def uptime(self):
        """ Shows the uptime of the bot.
            >uptime
        """
        current_time = int(time.time())
        uptime = utils.ReadableTime(self.startTime, current_time)
        await self.bot.say('I\'ve been up for *{}*.'.format(uptime))


def setup(bot):
    bot.add_cog(Utils(bot))