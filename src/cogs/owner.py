import git
from discord.ext import commands


class OwnerCog(commands.Cog, name="Owner Commands"):
    """ OwnerCog """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load', hidden=True, aliases=['l', 'lo'])
    @commands.is_owner()
    async def _load(self, ctx, *, cog: str):
        """ Command which Loads a Module.
            Remember to use dot path. e.g: cogs.owner
        """
        try:
            self.bot.load_extension(cog)
        except (AttributeError, ImportError) as error:
            await ctx.message.add_reaction('👎')
            await ctx.send(f'```py\nCould not load {cog}: {type(error).__name__} - {error}\n```')
        else:
            await ctx.message.add_reaction('👌')
            #await ctx.send(f'```Successfully loaded {cog}!```')

    @commands.command(name='unload', hidden=True, aliases=['ul', 'unl'])
    @commands.is_owner()
    async def _unload(self, ctx, *, cog: str):
        """ Command which Unloads a Module.
            Remember to use dot path. e.g: cogs.owner
        """
        try:
            self.bot.unload_extension(cog)
        except (AttributeError, ImportError) as error:
            await ctx.message.add_reaction('👎')
            await ctx.send(f'```py\nCould not unload {cog}: {type(error).__name__} - {error}\n```')
        else:
            await ctx.message.add_reaction('👌')
            #await ctx.send(f'```Successfully unloaded {cog}!```')

    @commands.command(name='reload', hidden=True, aliases=['r', 'rel'])
    @commands.is_owner()
    async def _reload(self, ctx, *, cog: str):
        """ Command which Reloads a Module.
            Remember to use dot path. e.g: cogs.owner
        """
        if cog == 'r':
            async for message in ctx.channel.history(limit=200):
                if str(message.content).startswith('rufus reload'):
                    cog = message.content[13:]
                    break
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except (AttributeError, ImportError) as error:
            await ctx.message.add_reaction('👎')
            await ctx.send(f'```py\nCould not reload {cog}: {type(error).__name__} - {error}\n```')
        else:
            await ctx.message.add_reaction('👌')
            #await ctx.send(f'```Successfully reloaded {cog}!```')

    @commands.command(name='pull', hidden=True)
    @commands.is_owner()
    async def _pull(self, ctx, cog: str = ''):
        """ Pull github origin.
            If argument is passed, cog will be reloaded.
            Does not currently support docker mode.
        """
        if NOT_DOCKER_MODE:
            try:
                g = git.cmd.Git('./')
                g.pull()
            except Exception as error:
                await ctx.send(f'```py\n{type(error).__name__}: {str(error)}\n```')
                return
            if cog != '':
                try:
                    bot.unload_extension(cog)
                    bot.load_extension(cog)
                except (AttributeError, ImportError) as error:
                    await ctx.message.add_reaction('👎')
                    await ctx.send(f'```py\n{type(error).__name__}: {str(error)}\n```')
                    return
                else:
                    await ctx.message.add_reaction('👌')
                    #await ctx.send(f'```Successfully reloaded {cog}!```')

    @commands.command(name='stop', hidden=True, aliases=['exit', 'die', 'logout'])
    @commands.is_owner()
    async def _stop(self, ctx):
        """ Stops the bot.
        """
        msg = await ctx.send('*Goodbye.*')
        await msg.add_reaction('👋')
        await self.bot.logout()


def setup(bot):
    bot.add_cog(OwnerCog(bot))
