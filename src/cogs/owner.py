import git
import inspect
import config as c

#from phue import Bridge
from discord.ext import commands
from importlib import reload


class OwnerCog(commands.Cog, name="Owner"):
    """ OwnerCog """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='configflush', aliases=['flush'], hidden=True)
    @commands.is_owner()
    async def _config_flush(self, ctx):
        """ Reload config.
        """
        reload(c)
        await ctx.send('```Successully reloaded config file.```')

    @commands.command(name='debug', aliases=['eval'])
    @commands.is_owner()
    async def debug(self, ctx, *, code : str):
        """ Evaluates code.
        """
        # https://github.com/Rapptz/RoboDanny/blob/master/cogs/admin.py#L53
        code = code.strip('` ')
        #python = '```py\n{}\n```'
        python = '{}'
        result = None

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.message.guild,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }

        env.update(globals())

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.send(python.format(type(e).__name__ + ': ' + str(e)))
            return

        await ctx.send(python.format(result))

    #@commands.command('hue', aliases=['lights'])
    #@commands.is_owner()
    #async def hue(self, ctx, *, subcommand):
    #    if subcommand:
    #    if subcommand == 'on' or subcommand == 'off':
    #    b = Bridge(c.data['hue_ip'])
    #    b.connect()
    #    b.get_api()
    #    b.set_light(1, 'bri', 254)
    #    await ctx.send(b.get_light(1, 'on'))

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
