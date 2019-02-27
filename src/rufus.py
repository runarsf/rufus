""" Rufus """
import os
import atexit
import discord
import re
from discord.ext import commands
from subprocess import call
import config as c
import git
import datetime

STARTUP_EXTENSIONS = ['cogs.manager',
                      'cogs.admin',
                      'cogs.commands',
                      'cogs.engine',
                      'cogs.dev',
                      'cogs.uptime',
                      'cogs.osu'
                      ]

bot = commands.Bot(command_prefix=c.prefix, description=c.description)

@bot.event
async def on_ready():
    """ Returns true if bot is ready.
    """
    print('-' * len(bot.user.id))
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print(' ')
    print('Bot currently running on {} servers:'.format(len(bot.servers)))
    for s in bot.servers:
        print(' - ' + s.name + ' :: ' + s.id)
    print('-' * len(bot.user.id))
    print(' ')

    NOT_DOCKER_MODE = os.environ.get('DOCKER_MODE', False)
    if NOT_DOCKER_MODE:
        await bot.change_presence(game=discord.Game(name=c.game))
    else:
        await bot.change_presence(game=discord.Game(name=c.docker_game))

@bot.event
async def on_message(message):
    """ No swear words please.
    """
    if c.prefix in message.content[:1] or 'rufus' in message.content[:5]:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        with open('logs/bot.log', 'a') as logfile:
            logfile.write(str('++ {} - {}\n'.format(datetime.datetime.now().date(), datetime.datetime.now().time())))
            logfile.write(str('{} {}\n'.format(message.server.name, message.server.id)))
            logfile.write(str('{} {}\n'.format(message.author.name, message.author.mention)))
            logfile.write(str('{}\n'.format(message.content)))

    try:
        if message.author == bot.user or message.author.bot == True:
            return
        elif any(mention in message.content for mention in c.mention):
            print(message.author.name + ' ' + message.author.mention + ' :: ' + message.server.name + ' :: ' + message.content)
    finally:
        if c.prefix in message.content[1:2]:
            return
        elif c.prefix in message.content[:1]:
            print(message.author.name + ' ' + message.author.mention + ' :: ' + message.server.name + ' :: ' + message.content)
        if 'rufus' in message.content[:5]:
            message.content = message.content.replace("rufus ", c.prefix, 1)
        if message.content[1:] in c.greetings:
            if 'there' in message.content:
                message.content = c.prefix+'hello there'
            else:
                message.content = c.prefix+'hello'
    await bot.process_commands(message)

#@bot.event
#async def on_command_error(self, exception):
#    if isinstance(exception, commands.errors.CommandNotFound):
#        await self.say('```{}```'.format(exception))
#        return

@bot.command(pass_context=True)
async def load(ctx, extension_name: str):
    """ Loads an extension.
    """
    if str(ctx.message.author.id) == str(c.owner_id) or str(ctx.message.author.id) in c.dev_id:
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as error:
            await bot.say('```py\n{}: {}\n```'.format(type(error).__name__, str(error)))
            return
        await bot.say('Successfully loaded {}.'.format(extension_name))
    else:
        await bot.say('```diff\n-Insufficient privileges.\nAuthor ID: {}\nOwner ID: {}\nDev ID: {}```'.format(ctx.message.author.id, c.owner_id, c.dev_id))
        return

@bot.command(pass_context=True)
async def unload(ctx, extension_name: str):
    """ Unloads an extension.
    """
    if str(ctx.message.author.id) == str(c.owner_id) or str(ctx.message.author.id) in c.dev_id:
        try:
            bot.unload_extension(extension_name)
        except (AttributeError, ImportError) as error:
            await bot.say('```py\n{}: {}\n```'.format(type(error).__name__, str(error)))
            return
        await bot.say('Successfully unloaded {}.'.format(extension_name))
    else:
        await bot.say('```diff\n-Insufficient privileges.\nAuthor ID: {}\nOwner ID: {}\nDev ID: {}```'.format(ctx.message.author.id, c.owner_id, c.dev_id))
        return

@bot.command(pass_context=True)
async def reload(ctx, extension_name: str):
    """ Reloads an extension.
    """
    if str(ctx.message.author.id) == str(c.owner_id) or str(ctx.message.author.id) in c.dev_id:
        try:
            bot.unload_extension(extension_name)
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as error:
            await bot.say('```py\n{}: {}\n```'.format(type(error).__name__, str(error)))
            return
        await bot.say('Successfully reloaded ``{}``.'.format(extension_name))
    else:
        await bot.say('```diff\n-Insufficient privileges.\nAuthor ID: {}\nOwner ID: {}\nDev ID: {}```'.format(ctx.message.author.id, c.owner_id, c.dev_id))
        return

@bot.command(pass_context=True)
async def pull(ctx, extension_name: str = ''):
    """ Pull github origin.
            If argument is passed, cog will be reloaded.
            Does not support docker mode.
    """
    if str(ctx.message.author.id) == str(c.owner_id) or str(ctx.message.author.id) in c.dev_id:
        if NOT_DOCKER_MODE:
            try:
                g = git.cmd.Git('./')
                g.pull()
            except Exception as error:
                await bot.say('```py\n{}: {}\n```'.format(type(error).__name__, str(error)))
                return
            if extension_name != '':
                try:
                    bot.unload_extension(extension_name)
                    bot.load_extension(extension_name)
                except (AttributeError, ImportError) as error:
                    await bot.say('```py\n{}: {}\n```'.format(type(error).__name__, str(error)))
                    return
                await bot.say('Successfully reloaded ``{}``.'.format(extension_name))
    else:
        await bot.say('```diff\n-Insufficient privileges.\nAuthor ID: {}\nOwner ID: {}\nDev ID: {}```'.format(ctx.message.author.id, c.owner_id, c.dev_id))
    return

if __name__ == '__main__':
    for extension in STARTUP_EXTENSIONS:
        try:
            bot.load_extension(extension)
        except Exception as error:
            exception = '{}: {}'.format(type(error).__name__, error)
            print('Failed to load extension {}\n{}'.format(extension, exception))

    bot.run(c.token)


def exit_handler():
    """ What to do on exit.
    """
    print(' ')
    print('exiting...')


atexit.register(exit_handler)
