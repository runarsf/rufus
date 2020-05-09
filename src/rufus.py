#!/usr/bin/env python3
import re
import os
import atexit
import json
import random
import datetime
import sqlite3
import logging
import discord
import config as c
import sys
import asyncio
import requests
import time
import socket

from discord.ext import commands
from cogs.utils import rules

startup_extensions = ['cogs.owner',
                      'cogs.commands',
                      'cogs.admin',
                      'cogs.dev',
                      'cogs.osu',
                      'cogs.memes',
                      'cogs.runners',
                      'cogs.help'
                     ]

# DEBUG, INFO, WARNING, ERROR, CRITICAL, EXCEPTION
logging.basicConfig(stream=sys.stdout,
                    #filename='bot.log',
                    level=logging.INFO,
                    format='[%(asctime)s] [' + '%(levelname)s'.ljust(9) + '] %(name)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S'
                    )
log = logging.getLogger(__name__)

def get_prefix(_bot, message):
    if not message.guild:
        return ''
    return commands.when_mentioned_or(*c.prefixes)(_bot, message)

bot = commands.Bot(command_prefix=get_prefix, description=c.description)

@bot.event
async def on_ready():
    joined = []
    for guild in bot.guilds:
        joined.append(f' - {str(guild.name)} :: {str(guild.id)}')
    print()
    print('Logged in as:')
    print(f'{bot.user.name} - {bot.user.id}')
    print(f'Version: {discord.__version__}')
    print(f'\nBot currently running on {len(bot.guilds)} server(s):')
    print('-' * len(max(joined, key=len)))
    print('\n'.join(joined))
    print('-' * len(max(joined, key=len)))
    print()

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(c.game))

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    try:
        if str(rules.getrule('prefixless', message.guild.id)).lower() == 'true':
            if re.compile(r'(\s+|^)(' + '|'.join(c.swears) + ')(\s+|$)').search(message.content.lower()):
                await message.add_reaction(random.choice(c.rages))
                log.info(message)
            if message.content.startswith('man '):
                message.content = message.content.replace('man ', c.prefixes[0]+'help ')
            if message.content.upper() == 'F':
                await message.channel.send('F')
        if str(rules.getrule('dad', message.guild.id)).lower() == 'true':
            dads = ["i\'m", "i am", "jeg er", "ich bin", "ik ben", "jag är", "æ e"]
            for dad in dads:
                if message.content.lower().startswith(dad):
                    if dad in message.content.lower():
                        await message.channel.send(random.choice(c.greetings)+', '+message.content[int(message.content.lower().find(dad))+len(dad):].strip()+'! I\'m Rufus.')
                        log.info(message)
    except:
        pass
    log.info(message)
    await bot.process_commands(message)

@bot.event
async def on_command_error(self, exception):
    log.info(exception)
    if isinstance(exception, commands.errors.MissingPermissions):
        exception = f'Sorry {self.message.author.name}, you don\'t have permissions to do that!'
    elif isinstance(exception, commands.errors.CheckFailure):
        exception = f'Sorry {self.message.author.name}, you don\'t have the necessary roles for that!'
    elif isinstance(exception, TimeoutError):
        log.warn(f'TimeoutError: {exception}')
        return

    error_embed = discord.Embed(title='',
                                timestamp=datetime.datetime.utcnow(),
                                description=f'```python\n{exception}```',
                                color=discord.Color.from_rgb(200, 0, 0))
    error_embed.set_author(name='Woops!',
                           icon_url=str(self.message.author.avatar_url))
    error_embed.set_footer(text=str(type(exception).__name__))
    error_message = await self.send(embed=error_embed)

    await error_message.add_reaction('❔')

    def check_reaction(reaction, user):
        return user != self.bot.user and str(reaction.emoji) == '❔'
    try:
        reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check_reaction)
    except asyncio.TimeoutError:
        await error_message.remove_reaction('❔', self.bot.user)
    else:
        await error_message.remove_reaction('❔', self.bot.user)
        error_embed.add_field(name='Details', value=f'{exception.__doc__}', inline=False)
        error_embed.add_field(name='Cause', value=f'{exception.__cause__ }', inline=False)
        await error_message.edit(embed=error_embed)


if __name__ == '__main__':
    for extension in startup_extensions:
        bot.load_extension(extension)

    bot.run(c.data["botToken"], bot=True, reconnect=True)
