""" commands -- rufus.py """
import time
import subprocess
import sys
import os
import config as c

# unused import discord
from discord.ext import commands

class Admin:
    """ commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def purge(self, ctx):
        """ Deletes the messages of the specified user. """
        mcont = ctx.message.content
        if mcont == str(c.prefix + 'purge'):
            await self.bot.delete_message(ctx.message)
            print('command.purge :: no argument')
        elif mcont == c.prefix + 'purge all':
            await self.bot.send_message(ctx.message.channel, 'Clearing messages...')
            time.sleep(2)
            async for msg in self.bot.logs_from(ctx.message.channel):
                await self.bot.delete_message(msg)
        else:
            print('purge error.else')

    @commands.command()
    async def spam(self, times: int, content='repeating...'):
        """Repeats a message multiple times."""
        for i in range(times):
            await self.bot.say(content)
            print(i)

    @commands.command()
    async def restart(self):
        """ Restarts the bot """
        await self.bot.say('*restarting...*')
        clear = lambda: os.system('cls')
        time.sleep(2)
        await self.bot.logout()
        clear()
        print('restarting')
        time.sleep(0.5)
        clear()
        print('restarting.')
        time.sleep(0.5)
        clear()
        print('restarting..')
        time.sleep(0.5)
        clear()
        print('restarting...')
        time.sleep(0.5)
        clear()
        print('restarting.')
        time.sleep(0.5)
        clear()
        print('restarting..')
        time.sleep(0.5)
        clear()
        print('restarting...')
        subprocess.call([sys.executable, 'rufus.py'])


def setup(bot):
    """ defines setup """
    bot.add_cog(Admin(bot))
