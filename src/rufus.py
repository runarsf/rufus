""" Rufus """
import os
import atexit
import discord
import re
from discord.ext import commands
from subprocess import call
import config as c
import git


STARTUP_EXTENSIONS = ['cogs.manager',
                      'cogs.admin',
                      'cogs.commands',
                      'cogs.memes',
                      'cogs.engine',
                      'cogs.dev',
                      'cogs.uptime'
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

    DOCKER_MODE = os.environ.get('DOCKER_MODE', False)
    if DOCKER_MODE:
        await bot.change_presence(game=discord.Game(name=c.game))
    else:
        await bot.change_presence(game=discord.Game(name=c.docker_game))

@bot.event
async def on_message(message):
    """ No swear words please.
    """
    try:
        if message.author == bot.user:
            return
        elif any(message.content in cuss for cuss in c.swears):
            await bot.send_file(message.channel, str("{}/img/christ.jpg".format(os.path.dirname(os.path.realpath(__file__)))))
            print(message.author.name + ' ' + message.author.mention + ' :: ' + message.server.name + ' :: ' + 'swore')
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

@bot.command()
async def load(extension_name: str):
    """ Loads an extension.
    """
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as error:
        await bot.say('```py\n{}: {}\n```'.format(type(error).__name__, str(error)))
        return
    await bot.say('Successfully loaded {}.'.format(extension_name))

@bot.command()
async def unload(extension_name: str):
    """ Unloads an extension.
    """
    try:
        bot.unload_extension(extension_name)
    except (AttributeError, ImportError) as error:
        await bot.say('```py\n{}: {}\n```'.format(type(error).__name__, str(error)))
        return
    await bot.say('Successfully unloaded {}.'.format(extension_name))

@bot.command()
async def reload(extension_name: str):
    """ Reloads an extension.
    """
    try:
        bot.unload_extension(extension_name)
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as error:
        await bot.say('```py\n{}: {}\n```'.format(type(error).__name__, str(error)))
        return
    await bot.say('Successfully reloaded ``{}``.'.format(extension_name))

@bot.command()
async def pull(extension_name: str = ''):
    """ Pull github origin.
            If argument is passed, cog will be reloaded.
            Does not support docker mode.
    """
    try:
        g = git.cmd.Git('./')
        g.pull()
    except Exception as error:
        await bot.say('```py\n{}: {}\n```'.format(type(error).__name__, str(error)))
        return
    if extension_name != '':
        try:
            await asyncio.run(reload(extension_name))
        except Exception:
            await bot.say('Could not run coroutine function ``reload``')
        try:
            bot.unload_extension(extension_name)
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as error:
            await bot.say('```py\n{}: {}\n```'.format(type(error).__name__, str(error)))
            return
        await bot.say('Successfully reloaded ``{}``.'.format(extension_name))

if __name__ == '__main__':
    for extension in STARTUP_EXTENSIONS:
        try:
            bot.load_extension(extension)
        except Exception as error:
            exc = '{}: {}'.format(type(error).__name__, error)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(c.token)


def exit_handler():
    """ What to do on exit.
    """
    print(' ')
    print('exiting...')


atexit.register(exit_handler)
