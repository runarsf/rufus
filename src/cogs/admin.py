import discord
import config as c
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
