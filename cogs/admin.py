""" commands -- rufus.py """
import asyncio
# unused import subprocess
# unused import sys
# unused import os
import config as c

# unused import discord
from discord.ext import commands

class Admin:
    """ commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def purge(self, ctx, amount: int):
        """ Deletes the messages of the specified user. """
        mcont = ctx.message.content
        if mcont == str(c.prefix + 'purge'):
            await self.bot.delete_message(ctx.message)
            print('command.purge :: no argument')
        elif mcont == c.prefix + 'purge all':
            await self.bot.send_message(ctx.message.channel, 'Clearing messages...')
            asyncio.sleep(2)
            async for msg in self.bot.logs_from(ctx.message.channel):
                await self.bot.delete_message(msg)
        else:
            print('purge error on else')

    @commands.command(pass_context=True)
    async def spam(self, ctx, times: int, content='repeating...'):
        """ Repeats a message multiple times. """
        userid = ctx.message.author.id
        if userid == c.owner_id or userid in str(c.dev_id):
            for i in range(times):
                await self.bot.say(content)
                print(i)
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """ Stops the bot. """
        userid = ctx.message.author.id
        if userid == c.owner_id or userid in str(c.dev_id):
            await self.bot.say('*Goodbye.*')
            await self.bot.logout()
        else:
            await self.bot.say('*Insufficient privileges*')

""" NOT RECOMMENDED, WILL CAUSE RAM (<@319005959022313483>) ISSUES
    @commands.command(pass_context=True)
    async def restart(self, ctx):
        \""" Restarts the bot \"""
        userid = ctx.message.author.id
        if userid == c.owner_id or userid in str(c.dev_id):
            await self.bot.say('*restarting...*')
            clear = lambda: os.system('cls')
            asyncio.sleep(2)
            await self.bot.logout()
            clear()
            print('restarting')
            asyncio.sleep(0.5)
            clear()
            print('restarting.')
            asyncio.sleep(0.5)
            clear()
            print('restarting..')
            asyncio.sleep(0.5)
            clear()
            print('restarting...')
            asyncio.sleep(0.5)
            clear()
            print('restarting.')
            asyncio.sleep(0.5)
            clear()
            print('restarting..')
            asyncio.sleep(0.5)
            clear()
            print('restarting...')
            subprocess.call([sys.executable, 'rufus.py'])
        else:
            self.bot.say('*Insufficient privileges*')
"""

def setup(bot):
    """ defines setup """
    bot.add_cog(Admin(bot))
