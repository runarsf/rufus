""" commands -- rufus.py """
import asyncio
import threading
# unused import subprocess
# unused import sys
# unused import os
import config as c

# unused import discord
from discord.ext import commands

class Admin:
    """ Admin restriced commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def purge(self, ctx, amount: str):
        """ Deletes messages. """
        userid = ctx.message.author.id
        usid = int(amount.replace('<@', '').replace('>', ''))
        if userid == c.owner_id or userid in str(c.dev_id):
            await self.bot.delete_message(ctx.message)
            if '<@' in amount and '>' in amount:
                async for amount in self.bot.logs_from(ctx.message.channel):
                    if amount not in self.bot.logs_from(ctx.message.channel):
                        return
                    else:
                        await self.bot.delete_message(ctx.message.id == usid)
            elif amount == str('all'):
                deleted = await self.bot.purge_from(ctx.message.channel, limit=750)
                await self.bot.say("Bulk purged **{}** Messages".format(len(deleted)))
                async for msg in self.bot.logs_from(ctx.message.channel):
                    await self.bot.delete_message(msg)
            elif int(amount) > 0:
                counter = 0
                for counter in range(int(amount)):
                    async for msg in self.bot.logs_from(ctx.message.channel):
                        if int(counter) >= int(amount):
                            return
                        else:
                            await self.bot.delete_message(msg)
                        counter += 1
            else:
                print('purge error on else')
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def bulk(self, ctx, amount: int):
        """ Clears messages """
        userid = ctx.message.author.id
        if userid == c.owner_id or userid in str(c.dev_id):
            deleted = await self.bot.purge_from(ctx.message.channel, limit=amount)
            await self.bot.say("Cleared **{}** Messages".format(len(deleted)))
        else:
            await self.bot.say('*Insufficient privileges*')

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
