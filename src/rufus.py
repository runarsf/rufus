import os
import atexit
import json
import re
import random
import config as c
import datetime
import sqlite3
import sys
import asyncio
#import cherrypy
#from threading import Thread

import discord
from discord.ext import commands

STARTUP_EXTENSIONS = ['cogs.owner',
                      'cogs.commands',
                      'cogs.admin',
                      'cogs.dev',
                      'cogs.osu',
                      'cogs.memes',
                      'cogs.runners',
                      'cogs.help'
                     ]

def get_prefix(bot, message):
    """A callable Prefix. This could be edited to allow per server prefixes."""
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

    if c.dockerStatus:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(c.dockerGame))
    else:
        #await bot.change_presence(status=discord.Status.online, activity=discord.Game(c.devGame))
        await bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name=c.devGame, url='https://twitch.tv/toolbar', details='coding'))

    dumpConfig(c.data, f'{c.srcDir}/template-secrets.json')

@bot.event
async def on_message(message):
    """ No swear words please.
    """
    if message.author == bot.user or message.author.bot == True:
        return
    if any(swears in f' {message.content} ' for swears in c.swears):
        await message.add_reaction(random.choice(c.rages))
        logger(message)
    if message.content.upper() == 'F':
        await message.channel.send('F')
        logger(message)
    dads = ["i\'m", "i am", "jeg er", "ich bin", "ik ben"]
    #for dad in dads:
    #    if message.content.lower().startswith(dad):
        #if dad in message.content.lower():
    #        dadmessage = await message.channel.send(random.choice(c.greetings)+', '+message.content[int(message.content.lower().find(dad))+len(dad):].strip()+'! I\'m Rufus.')
    #        logger(message)
    #        try:
    #            channel = message.channel
    #            thankers = ['stop that', 'stop', 'no', 'please stop', 'delet this']
    #            def check(m):
    #                return any(thanks in m.content for thanks in thankers) and m.channel == channel
    #            msg = await bot.wait_for('message', check=check, timeout=25)
    #            await dadmessage.delete()
    #            await msg.delete()
    #            return
    #        except Exception:
    #            return
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
    if True:
    #if isinstance(exception, commands.errors.MissingPermissions):
    #    await self.send(f'```Sorry {self.message.author.name}, you don\'t have permissions to do that!```')
    #elif isinstance(exception, commands.errors.CheckFailure):
    #    await self.send(f'```Sorry {self.message.author.name}, you don\'t have the necessary roles for that.```')
    #elif isinstance(exception, TimeoutError):
    #    return
    #else:
        errorEmbed = discord.Embed(title='', timestamp=datetime.datetime.utcnow(), description=f'```python\n{exception}```', color=discord.Color.from_rgb(200, 0, 0))
        errorEmbed.set_author(name=str(self.message.author), icon_url=str(self.message.guild.get_member(self.message.author.id).avatar_url))
        errorEmbed.set_footer(text=str(type(exception).__name__))
        errorMessage = await self.send(embed=errorEmbed)

        await errorMessage.add_reaction('❔')

        def check(reaction, user):
            return user != self.bot.user and str(reaction.emoji) == '❔'
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await errorMessage.remove_reaction('❔', self.bot.user)
        else:
            await errorMessage.remove_reaction('❔', self.bot.user)
            errorEmbed.add_field(name='Details', value=f'{exception.__doc__}', inline=False)
            errorEmbed.add_field(name='Cause', value=f'{exception.__cause__ }', inline=False)
            await errorMessage.edit(embed=errorEmbed)
            # await self.send('Unknown error: '+exception.__doc__)

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

def dumpConfig(jsonData, dumpFile: str):
    """ Dump json data as a template.
    """
    with open(dumpFile, 'w') as template:
        finalJson = ['{']
        for x in jsonData:
            finalJson.append(f'\t\"{str(x)}\": \"KEY\",')
        finalJson = ''.join(finalJson)
        finalJson = finalJson[:-1]
        finalJson += '}'
        json.dump(json.loads(finalJson), template)

#class HelloWorld(object):
#    @cherrypy.expose
#    def index(self):
#        return "Hello World!"

if __name__ == '__main__':
    for extension in STARTUP_EXTENSIONS:
        bot.load_extension(extension)
    #cherrypy.config.update({'server.socket_port': 8099})

    #threads = []

    #botProcess = Thread(target=bot.run, args=[c.data["botToken"]], kwargs={'bot': True, 'reconnect': True})
    #botProcess.start()
    #threads.append(botProcess)

    #webProcess = Thread(target=cherrypy.quickstart, args=[HelloWorld()])
    #webProcess.start()
    #threads.append(webProcess)

    #for process in threads:
    #    process.join()
    #cherrypy.quickstart(HelloWorld())
    bot.run(c.data["botToken"], bot=True, reconnect=True)
