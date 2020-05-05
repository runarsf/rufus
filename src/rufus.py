#!/usr/bin/env python3
import re
import os
import atexit
import json
import random
import datetime
import sqlite3
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

def get_prefix(bot, message):
    # FIXME: Check if this works
    if not message.guild:
        pass
    return commands.when_mentioned_or(*c.prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, description=c.description)

@bot.event
async def on_ready():
    # TODO: Find max lenght of string and create padding using ljust()
    print('-' * len(str(bot.user.id)))
    print('Logged in as:')
    print(f'{bot.user.name} - {bot.user.id}')
    print(f'Version: {discord.__version__}')
    print(f'\nBot currently running on {len(bot.guilds)} servers:')
    for s in bot.guilds:
        print(f' - {str(s.name)} :: {str(s.id)}')
    print('-' * len(str(bot.user.id))+'\n')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(c.game))

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    try:
        if str(rules.getrule('prefixless', message.guild.id)).lower() == 'true':
            if re.compile(r'(\s+|^)(' + '|'.join(c.swears) + ')(\s+|$)').search(message.content.lower()):
                await message.add_reaction(random.choice(c.rages))
                logger(message)
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
                        logger(message)
    except:
        pass
    for prefix in range(len(c.prefixes)):
        if message.content.startswith(prefix):
            logger(message)
            await bot.process_commands(message)

@bot.event
async def on_command_error(self, exception):
    if isinstance(exception, commands.errors.MissingPermissions):
        exception = f'Sorry {self.message.author.name}, you don\'t have permissions to do that!'
    elif isinstance(exception, commands.errors.CheckFailure):
        exception = f'Sorry {self.message.author.name}, you don\'t have the necessary roles for that!'
    elif isinstance(exception, TimeoutError):
        return
    error_embed = discord.Embed(title='', timestamp=datetime.datetime.utcnow(), description=f'```python\n{exception}```', color=discord.Color.from_rgb(200, 0, 0))
    error_embed.set_author(name=str(self.message.author), icon_url=str(self.message.guild.get_member(self.message.author.id).avatar_url))
    error_embed.set_footer(text=str(type(exception).__name__))
    error_message = await self.send(embed=error_embed)

    await errorMessage.add_reaction('❔')

    def check_reaction(reaction, user):
        return user != self.bot.user and str(reaction.emoji) == '❔'
    try:
        reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check_reaction)
    except asyncio.TimeoutError:
        await errorMessage.remove_reaction('❔', self.bot.user)
    else:
        await errorMessage.remove_reaction('❔', self.bot.user)
        errorEmbed.add_field(name='Details', value=f'{exception.__doc__}', inline=False)
        errorEmbed.add_field(name='Cause', value=f'{exception.__cause__ }', inline=False)
        await errorMessage.edit(embed=errorEmbed)
        # await self.send('Unknown error: '+exception.__doc__)

def logger(message):
    # TODO: Use an actual logger (logging)
    try:
        print(f'{message.author.name} {message.author.mention} :: {message.guild.name} :: {message.content}')
    except:
        print(f'{message.author.name} {message.author.mention} :: {message.content}')


if __name__ == '__main__':
    for extension in startup_extensions:
        bot.load_extension(extension)

    bot.run(c.data["botToken"], bot=True, reconnect=True)
