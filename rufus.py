""" Rufus """
import os
import atexit
import discord
from discord.ext import commands
import config as c
# pip install -r .\requirements.txt


STARTUP_EXTENSIONS = ['cogs.commands',
                      'cogs.admin',
                      'cogs.uptime',
                      'cogs.memes',
                      'cogs.math',
                      'cogs.osu!',
                      'cogs.engine'
                      ]

bot = commands.Bot(command_prefix=c.prefix, description=c.description)


@bot.event
async def on_ready():
    """ Returns true if bot is ready.
    """
    clear = lambda: os.system('cls')
    clear()
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

    # check config
    confile = open('configs.py', 'r')
    cont = confile.read()
    if 'token' not in cont:
        confile = open('configs.py', 'w')
        confile.write('# rufus.py config \ntoken = \'\'')
    else:
        confile.close()


@bot.command()
async def load(extension_name: str):
    """ Loads an extension.
        >load <extension_name>
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
        >unload <extension_name>
    """
    try:
        bot.unload_extension(extension_name)
    except (AttributeError, ImportError) as exopt:
        await bot.say('```py\n{}: {}\n```'.format(type(exopt).__name__, str(exopt)))
        return
    await bot.say('Successfully unloaded {}.'.format(extension_name))

@bot.command()
async def r():
    """ Reloads all extensions, set by the owner.
        >r
    """
    bot.unload_extension('cogs.admin')
    bot.unload_extension('cogs.commands')
    bot.unload_extension('cogs.engine')
    bot.unload_extension('cogs.math')
    bot.unload_extension('cogs.memes')
    bot.unload_extension('cogs.osu!')

    bot.load_extension('cogs.admin')
    bot.load_extension('cogs.commands')
    bot.load_extension('cogs.engine')
    bot.load_extension('cogs.math')
    bot.load_extension('cogs.memes')
    bot.load_extension('cogs.osu!')

    await bot.say('All cogs reloaded.')

@bot.command()
async def reload(extension_name: str):
    """ Loads an extension.
        >reload <extension_name>
    """
    try:
        reunload = 0
        reload = 0
        bot.unload_extension(extension_name)
        reunload = 1
        bot.load_extension(extension_name)
        reload = 1
    except (AttributeError, ImportError) as exopt:
        await bot.say('```py\n{}: {}\n```'.format(type(exopt).__name__, str(exopt)))
        return
    if reunload == 1 and reload == 1:
        await bot.say('Successfully reloaded {}.'.format(extension_name))
    elif reunload == 1 and reload == 0:
        await bot.say('Could not load {}.'.format(extension_name))
    elif reunload == 0 and reload == 1:
        await bot.say('Could not unload {}.'.format(extension_name))
    else:
        await bot.say('Could not reload {}'.format(extension_name))


@bot.event
async def on_message(message):
    """ No swear words please.
    """
    try:
        if message.author == bot.user:
            return
        if any(word in message.content for word in c.swears):
            await bot.send_file(message.channel, 'img/christ.jpg')
        wordsls = ['meme review']
        if any(word in message.content for word in wordsls):
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
