import os
import atexit
import discord
import re
from discord.ext import commands
from subprocess import call
import config as c
import datetime

STARTUP_EXTENSIONS = ['cogs.owner',
                      'cogs.commands',
                      'cogs.admin',
                      'cogs.dev',
                      'cogs.osu',
                      'cogs.memes',
                      'cogs.runners'
                     ]

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*c.prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, description=c.description)

@bot.event
async def on_ready():
    """ Returns true if bot is ready.
    """
    print('-' * len(str(bot.user.id)))
    print('Logged in as:')
    print(f'{bot.user.name} - {bot.user.id}')
    print(f'Version: {discord.__version__}\n')
    print(f'Bot currently running on {len(bot.guilds)} servers:')
    for s in bot.guilds:
        print(f' - {str(s.name)} :: {str(s.id)}')
    print('-' * len(str(bot.user.id))+'\n')

    NOT_DOCKER_MODE = os.environ.get('DOCKER_MODE', False)
    if NOT_DOCKER_MODE:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(c.game))
    else:
        #await bot.change_presence(status=discord.Status.online, activity=discord.Game(c.docker_game))
        await bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name=c.docker_game, url='https://twitch.tv/toolbar', details='programming'))

@bot.event
async def on_message(message):
    """ No swear words please.
    """
    if message.author == bot.user or message.author.bot == True:
        return
    for i in range(len(c.prefixes)):
        if message.content[:len(c.prefixes[i])] == c.prefixes[i]:
            if message.content[len(c.prefixes[i]):] in c.greetings:
                if 'there' in message.content[len(c.prefixes[i]):]:
                    message.content = c.prefixes[i]+'hello there'
                else:
                    message.content = c.prefixes[i]+'hello'
            logger(message)
            await bot.process_commands(message)

@bot.event
async def on_command_error(self, exception):
    if isinstance(exception, commands.errors.MissingPermissions):
        await self.send(f'```Sorry {self.message.author.name}, you do not have permissions to do that!```')
    elif isinstance(exception, commands.errors.CheckFailure):
        await self.send(f'```Sorry {self.message.author.name}, you don\'t have the necessary roles for that.```')
    elif isinstance(exception, TimeoutError):
        return
    else:
        await self.send(f'```python\n{type(exception).__name__}: {exception}```')

def logger(message):
    try:
        test = message.guild.id
        if not os.path.exists(f'{c.srcDir}/logs'):
            os.makedirs(f'{c.srcDir}/logs')
        with open(f'{c.srcDir}/logs/bot.log', 'a') as logfile:
            logfile.write(str('{0.id} - {0.name} : {1.name} - {1.id} : {2.date()} - {2.time()}'.format(message.author, message.guild, datetime.datetime.now())))
            #logfile.write(str(f'++ {datetime.datetime.now().date()} - {datetime.datetime.now().time()}\n'))
            #logfile.write(str(f'{message.guild.name} {str(message.guild.id)}\n'))
            #logfile.write(str(f'{message.author.name} {message.author.mention}\n'))
            logfile.write(str('{message.content}\n'))
        print(f'{message.author.name} {message.author.mention} :: {message.guild.name} :: {message.content}')
    except:
        if not os.path.exists(f'{c.srcDir}/logs'):
            os.makedirs(f'{c.srcDir}/logs')
        with open(f'{c.srcDir}/logs/bot.log', 'a') as logfile:
            logfile.write(str(f'++ {datetime.datetime.now().date()} - {datetime.datetime.now().time()}\n'))
            logfile.write(str(f'direct message\n'))
            logfile.write(str(f'{message.author.name} {message.author.mention}\n'))
            logfile.write(str(f'{message.content}\n'))
        print(f'{message.author.name} {message.author.mention} :: {message.content}')


if __name__ == '__main__':
    for extension in STARTUP_EXTENSIONS:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f'Failed to load extension {extension}\n{type(error).__name__}: {error}')
    bot.run(c.token, bot=True, reconnect=False)
