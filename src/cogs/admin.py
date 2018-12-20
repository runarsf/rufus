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
        """
        if "admin" in [y.name.lower() for y in ctx.message.author.roles]:
            try:
                await self.bot.kick(user)
                await self.bot.say('User {} has been kicked with reason: ``{}``'.format(user, reason))
            except Exception:
                await self.bot.say('```An error occurred. User {} could not be kicked.```'.format(user))
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def ban(self, ctx, user: discord.User, *, reason: str = 'no reason given.'):
        """ Ban a user.
        """
        if "admin" in [y.name.lower() for y in ctx.message.author.roles]:
            try:
                await self.bot.ban(ctx.message.server, user)
                await self.bot.say('User {} has been banned with reason: ``{}``'.format(user, reason))
            except Exception:
                await self.bot.say('```An error occurred. User {} could not be banned.```'.format(user))
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def unban(self, ctx, user: discord.User):
        """ Ban a user.
        """
        if "admin" in [y.name.lower() for y in ctx.message.author.roles]:
            try:
                await self.bot.unban(ctx.message.server, user)
                await self.bot.say('User {} has been unbanned.'.format(user))
            except Exception:
                await self.bot.say('```An error occurred. User {} could not be banned.```'.format(user))
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def inviter(self, ctx):
        await client.send_message(discord.Object(id='12324234183172'), 'hello')
        invitelinknew = await self.bot.create_invite(destination = ctx.message.channel, xkcd = True, max_uses = 100)
        embedMsg=discord.Embed(color=0x114455)
        embedMsg.add_field(name="Discord Invite Link", value=invitelinknew)
        embedMsg.set_footer(text="Discord server invited link.")
        await self.bot.say(embed=embedMsg)

    @commands.command(pass_context=True)
    async def invite(self, ctx, userToInvite: discord.User = '', *, message: str = ''):
        """ Invite user to server.
        """
        discord.create_invite()
        inviteLink = 'discord.gg/uaECMPQ'
        if "admin" in [y.name.lower() for y in ctx.message.author.roles]:
            if str(userToInvite) == '':
                await self.bot.say(inviteLink)
            else:
                if message == '':
                    await self.bot.send_message(userToInvite, inviteLink + '\n``Invited by {}.``'.format(ctx.message.author))
                else:
                    await self.bot.send_message(userToInvite, inviteLink + '\n```Invited by {};\n{}```'.format(ctx.message.author, message))
                await self.bot.say('Invite link sent to ``{}``.'.format(userToInvite))
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def nick(self, ctx, user: discord.User = '', *, new_nick: str = ''):
        """ Change user nick.
        """
        if "admin" in [y.name.lower() for y in ctx.message.author.roles]:
            self.bot.change_nickname(user, new_nick)
        else:
            await self.bot.say('*Insufficient privileges*')


def setup(bot):
    """ defines setup """
    bot.add_cog(Admin(bot))
