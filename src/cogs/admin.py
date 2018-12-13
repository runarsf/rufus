""" admin -- rufus.py """
import os
import ctypes
import config as c

import discord
from discord.ext import commands


class Admin:
    """ Admin restricted commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def purge(self, ctx, amountUserAll: str):
        """ Delete messages from current channel.
        """
        usid = int(amountUserAll.replace('<@', '').replace('>', ''))
        if "admin" in [y.name.lower() for y in ctx.message.author.roles]:
            await self.bot.delete_message(ctx.message)
            if '<@' in amountUserAll and '>' in amountUserAll:
                async for amountUserAll in self.bot.logs_from(ctx.message.channel):
                    if amountUserAll not in self.bot.logs_from(ctx.message.channel):
                        return
                    else:
                        await self.bot.delete_message(ctx.message.id == usid)
            elif amountUserAll == str('all'):
                deleted = await self.bot.purge_from(ctx.message.channel, limit=750)
                await self.bot.say('Bulk-purged **{}** Messages'.format(len(deleted)))
                async for msg in self.bot.logs_from(ctx.message.channel):
                    await self.bot.delete_message(msg)
            elif int(amountUserAll) > 0:
                counter = 0
                for counter in range(int(amountUserAll)):
                    async for msg in self.bot.logs_from(ctx.message.channel):
                        if int(counter) >= int(amountUserAll):
                            return
                        else:
                            await self.bot.delete_message(msg)
                        counter += 1
            else:
                print('purge, error on else')
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def spam(self, ctx, times: int = 1, *, msg: str = 'spam'):
        """ Repeat a message multiple times.
        """
        if "admin" in [y.name.lower() for y in ctx.message.author.roles]:
            for i in range(times):
                await self.bot.say(msg)
                print(i)
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def kick(self, ctx, user: discord.User, *, reason: str = 'no reason given.'):
        """ Kick a user.
                user formatting: user#1234
        """
        if "admin" in [y.name.lower() for y in ctx.message.author.roles]:
            try:
                await self.bot.kick(user)
                await self.bot.say('User {} has been kicked with reason: ``{}``'.format(user, reason))
            except Exception:
                await self.bot.say('```An error occurred. User {} could not be kicked.```'.format(user))
        else:
            await self.bot.say('*Insufficient privileges*')


def setup(bot):
    """ defines setup """
    bot.add_cog(Admin(bot))
