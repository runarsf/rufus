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

    await bot.change_presence(game=discord.Game(name=c.game))

@bot.command()
async def load(extension_name: str):
    """ Loads an extension.
    """
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as exopt:
        await bot.say('```py\n{}: {}\n```'.format(type(exopt).__name__, str(exopt)))
        return
    await bot.say('Successfully loaded {}.'.format(extension_name))

@bot.command()
async def unload(extension_name: str):
    """ Unloads an extension.
    """
    try:
        bot.unload_extension(extension_name)
    except (AttributeError, ImportError) as exopt:
        await bot.say('```py\n{}: {}\n```'.format(type(exopt).__name__, str(exopt)))
        return
    await bot.say('Successfully unloaded {}.'.format(extension_name))

@bot.command()
async def reload(extension_name: str):
    """ Reloads an extension.
    """
    try:
        bot.unload_extension(extension_name)
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as exopt:
        await bot.say('```py\n{}: {}\n```'.format(type(exopt).__name__, str(exopt)))
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
    except Exception as exopt:
        await bot.say('```py\n{}: {}\n```'.format(type(exopt).__name__, str(exopt)))
        return
    if extension_name != '':
        try:
            bot.unload_extension(extension_name)
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as exopt:
            await bot.say('```py\n{}: {}\n```'.format(type(exopt).__name__, str(exopt)))
            return
        await bot.say('Successfully reloaded ``{}``.'.format(extension_name))

@bot.event
async def on_message(message):
    """ No swear words please.
    """
    try:
        if message.author == bot.user:
            return
        if any(word in message.content for word in c.swears):
            await bot.send_file(message.channel, 'img/christ.jpg')
        memer = re.search(r'.*?meme.*?review.*?', message.content)
        if memer:
            await bot.say(':clap: :clap:')
        if any(word in message.content for word in c.mention):
            print(message.author.name + ' ' + message.author.mention + ' :: ' + message.server.name + ' :: ' + message.content)
    except:
        pass
    finally:
        if '>>' in message.content[:2]:
            return
        elif c.prefix in message.content[:1]:
            print(message.author.name + ' ' + message.author.mention + ' :: ' + message.server.name + ' :: ' + message.content)
    await bot.process_commands(message)


if __name__ == '__main__':
    for extension in STARTUP_EXTENSIONS:
        try:
            bot.load_extension(extension)
        except Exception as exopt:
            exc = '{}: {}'.format(type(exopt).__name__, exopt)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(c.token)


def exit_handler():
    """ What to do on exit.
    """
    print(' ')
    print('exiting...')


atexit.register(exit_handler)
