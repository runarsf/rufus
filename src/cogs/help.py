import datetime
import os
import config as c
from inspect import signature

import discord
from discord.ext import commands


class HelpCog(commands.Cog, name="Help Commands"):
    """ HelpCog """

    def __init__(self, bot):
        self.bot = bot

    '''
    @commands.command()
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def help(self, ctx):
        """Gets all cogs and commands of mine.
           https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html?highlight=commands#command
           https://github.com/Rapptz/discord.py/blob/967d43c35b4d4c288d47a9eb9d374bef34292f1d/discord/ext/commands/bot.py
        """
        embed = discord.Embed(title='', timestamp=datetime.datetime.utcnow(), description=f'```apache\n{", ".join(c.prefixes)}```', color=discord.Color.from_rgb(48, 105, 152))
        for index, command in enumerate(self.bot.commands, start=2):
            nameAliases = str(command) if not ' | '.join(command.aliases) else str(' • '.join(str(command).split(" ")+command.aliases))
            if not command.hidden:
                embed.add_field(name=nameAliases+str(f' `{command.cog.qualified_name}`'), value=str(command.help.split('\n', 1)[0][:30]), inline=False)
        await ctx.send(embed=embed)
        '''


    @commands.command(name='help', aliases=['man'])
    async def help(self, ctx, *, command: str = ''):
        """ General bot help.
            https://docs.python.org/3/library/inspect.html
        """
        gearIcon = 'https://gist.githubusercontent.com/runarsf/0404fe681e5735386ccaf1bd8bfd40a7/raw/125d392d4bb1b21a0fa6c45f063cf353b355c487/gear.png'
        if not command:
            helpEmbed = discord.Embed(title='', timestamp=datetime.datetime.utcnow(), description=f'```apache\n{", ".join(c.prefixes)}```', color=discord.Color.from_rgb(48, 105, 152))
            helpEmbed.set_footer(text='All Commands', icon_url=gearIcon)
            for cog in self.bot.cogs:
                body = ''
                for cmd in self.bot.commands:
                    if str(cmd.cog.qualified_name) == str(cog) and not cmd.hidden:
                        nameAliases = str(cmd) if not ' | '.join(cmd.aliases) else '['+str(' | '.join(str(cmd).split(" ")+cmd.aliases)+']')
                        body += '  • '+nameAliases+'\n'
                helpEmbed.add_field(name=str(cog), value=body, inline=False)
            await ctx.send(embed=helpEmbed)
            return

        cog = self.bot.get_cog(command)
        if cog is None:
            cog = self.bot.get_cog(command.title())
        if command and cog is not None:
            cogEmbed = discord.Embed(title='', timestamp=datetime.datetime.utcnow(), description=f'```\n{cog.description}```', color=discord.Color.from_rgb(0, 14, 40))
            cogEmbed.set_footer(text=cog.qualified_name, icon_url=gearIcon)

            body = ''
            for cmd in self.bot.commands:
                if str(cmd.cog.qualified_name) == str(cog.qualified_name) and not cmd.hidden:
                    nameAliases = str(cmd) if not ' | '.join(cmd.aliases) else '['+str(' | '.join(str(cmd).split(" ")+cmd.aliases)+']')
                    body += '  • '+nameAliases+'\n'

            cogEmbed.add_field(name='Commands', value=body, inline=False)

            await ctx.send(embed=cogEmbed)
            return

        for cmd in self.bot.commands:
            if str(cmd) == command:
                # manualPrefix = ctx.message.content[:ctx.message.content.find("help")]
                #sig = signature(cmd)
                nameAliases = str(cmd) if not ' | '.join(cmd.aliases) else '['+str(' | '.join(str(cmd).split(" ")+cmd.aliases)+']')
                usage = f'{ctx.prefix}{cmd}'
                for key, value in cmd.clean_params.items():
                    #await ctx.send(f'{key} vs {value}')
                    usage += f' {value}'
                #await ctx.send(str(cmd.__doc__)[:1990])
                #await ctx.send(str(cmd.callback)[:1990])
                commandEmbed = discord.Embed(title='',
                        timestamp=datetime.datetime.utcnow(),
                        description=f'```ruby\n{usage}```\n{cmd.help}', color=discord.Color.from_rgb(194, 124, 13))
                commandEmbed.set_author(name=nameAliases, icon_url=str(ctx.message.guild.get_member(ctx.message.author.id).avatar_url))
                commandEmbed.set_footer(text=cmd.cog.qualified_name, icon_url=gearIcon)

                #sig = signature(help)
                #commandEmbed.add_field(name='help function', value=str(sig), inline=False)

                await ctx.send(embed=commandEmbed)
                return

    """
    >>> from inspect import signature
    >>> def foo(a, *, b:int, **kwargs):
    ...     pass

    >>> sig = signature(foo)

    >>> str(sig)
    '(a, *, b:int, **kwargs)'

    >>> str(sig.parameters['b'])
    'b:int'

    >>> sig.parameters['b'].annotation
    <class 'int'>
    """


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(HelpCog(bot))
