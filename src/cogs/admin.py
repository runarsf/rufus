import discord
import config as c
import asyncio
from discord.ext import commands


class AdminCog(commands.Cog, name="Admin Commands"):
    """ AdminCog """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='spam', hidden=True)
    @commands.has_role('admin')
    async def _spam(self, ctx, times: int = 1, *, msg: str = 'spam'):
        """ Repeat a message multiple times.
        """
        for i in range(times):
            await ctx.send(msg)

    @commands.command(name='pin')
    @commands.has_permissions(manage_messages=True)
    async def _pin(self, ctx):
        """ Pin previous message.
        """
        async for message in ctx.channel.history():
            passer = False
            for fix in c.prefixes:
                if message.content == f'{fix}pin':
                    passer = True
            if passer:
                continue
            await message.pin()
            return

    @commands.command(name='unpin')
    @commands.has_permissions(manage_messages=True)
    async def _unpin(self, ctx):
        """ Unpin previous message.
        """
        async for message in ctx.channel.history():
            passer = False
            for fix in c.prefixes:
                if message.content == f'{fix}unpin':
                    passer = True
            if passer:
                continue
            await message.unpin()
            return

    @commands.command(name='purge')
    @commands.has_permissions(manage_guild=True)
    async def _purge(self, ctx, amount: str, member: discord.Member = None, channel: int = None):
        """ Purge messages from current channel
        """
        def _member_check(m):
            return m.author == member

        if not str(amount) == 'all':
            amnt: int = int(float(amount))
        else:
            is_owner = await ctx.bot.is_owner(ctx.author)
            if not is_owner:
                await ctx.send(f'```Sorry {ctx.message.author.name}, you need to be the bot owner to run this command!```')
                return
            else:
                try:
                    channel = ctx.message.channel
                    await ctx.send(f'Are you sure? This will delete **ALL** messages in the current channel. (*{channel.name}*)')

                    def check(m):
                        return m.content == 'yes' and m.channel == channel
                    def c_check(m):
                        return m.content == 'c' or m.content == 'cancel' and m.channel == channel

                    msg = await self.bot.wait_for('message', check=check, timeout=10)
                    await channel.send('Purging **ALL** messages from current channel in **7 seconds**!\nType \'**cancel**\' or \'**c**\' to cancel.')

                    try:
                        msg = await self.bot.wait_for('message', check=c_check, timeout=7)
                        await ctx.send('Message purge cancelled.')
                    except Exception:
                        await ctx.message.channel.purge()
                        #async for message in ctx.channel.history(): # old method
                        #    await message.delete()

                except Exception:
                    await ctx.send('Response timed out, not doing anything.')
                    return
            return
        amnt += 1
        _suffix = ''
        ch = ctx.message.channel
        if channel is not None:
            ch = self.bot.get_channel(channel)
        if member is not None:
            deleted = await ch.purge(limit=amnt, check=_member_check)
            _suffix = f' from {member.name}'
        else:
            deleted = await ch.purge(limit=amnt)
        _s: str = '' if len(deleted)-1 == 1 else 's'
        msg = await ch.send(f'```Deleted {len(deleted)-1} message{_s}{_suffix}.```')
        await asyncio.sleep(3)
        await msg.delete()

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def _kick(self, ctx, *members: discord.Member):
        """ Kicks the specified member(s).
        """
        for member in members:
            await ctx.message.guild.kick(member)
            await ctx.send(f'```{member} was kicked from the server.```')

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def _ban(self, ctx, *members: discord.Member):
        """ Bans the specified member(s) and deletes their messages.
        """
        for member in members:
            await ctx.message.guild.ban(member, delete_message_days=7)
            await ctx.send(f'```{member} was banned from the server.```')

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def _unban(self, ctx, *, name: str):
        """ Unbans a member.
        """
        bans = await ctx.message.guild.bans()
        member = discord.utils.get(bans, user__name=name)
        if member:
            await ctx.message.guild.unban(member.user)
            await ctx.send(f'{member.user.name}#{member.user.discriminator} was unbanned. Welcome back!')
            return
        await ctx.send(f'{name} isn\' banned.')

    @commands.command(name='leave', aliases=['disconnect'])
    @commands.has_permissions(manage_guild=True, kick_members=True, ban_members=True)
    @commands.guild_only()
    async def _leave(self, ctx):
        """ Remove bot from server.
        """
        server = ctx.message.guild
        await server.leave()

    @commands.command(name='nick', aliases=['nickname', 'changenick'])
    @commands.has_permissions(manage_server=True)
    @commands.guild_only()
    async def _nickname(self, ctx, nickname, *members: discord.Member):
        """ Change member(s) nickname(s).
        """
        for member in members:
            await member.edit(nick=nickname)

    @_nickname.error
    async def nickname_error(self, ctx, error):
        await ctx.say('Command not fully implemented yet!')


def setup(bot):
    bot.add_cog(AdminCog(bot))
