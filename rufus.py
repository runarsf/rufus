""" Rufus """
import os
import discord
from discord.ext import commands
import config as c

STARTUP_EXTENSIONS = ["commands"]

bot = commands.Bot(command_prefix=c.prefix, description=c.description)

@bot.event
async def on_ready():
    """ Returns true if bot is ready """
    clear = lambda: os.system('cls')
    clear()
    print('------------------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    LON = len(bot.user.id)
    if LON == 18:
        print('------------------')
    await bot.change_presence(game=discord.Game(name=c.game))

@bot.command()
async def load(extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as exopt:
        await bot.say("```py\n{}: {}\n```".format(type(exopt).__name__, str(exopt)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
async def unload(extension_name: str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

@bot.command()
async def reload(extension_name: str):
    """Loads an extension."""
    try:
        bot.unload_extension(extension_name)
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as exopt:
        await bot.say("```py\n{}: {}\n```".format(type(exopt).__name__, str(exopt)))
        return
    await bot.say("{} reloaded.".format(extension_name))

if __name__ == "__main__":
    for extension in STARTUP_EXTENSIONS:
        try:
            bot.load_extension(extension)
        except Exception as exopt:
            exc = '{}: {}'.format(type(exopt).__name__, exopt)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(c.token)
