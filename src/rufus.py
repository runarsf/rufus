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
#from pathlib import Path

COGS = ['cogs.owner',
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
                    level=logging.INFO,
                    #format='[%(asctime)s] [' + '%(levelname)s'.ljust(9) + '] %(name)s %(message)s',
                    format='%(levelname)-8s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S'
                    )
log = logging.getLogger(__name__)

def get_prefix(_bot, message):
    """
    Return the prefix used in the specific channel.
    """
    if message.guild:
        scope = 'guild'
    else:
        scope = 'direct'
    return commands.when_mentioned_or(*c.scoped_prefixes[scope])(_bot, message)

bot = commands.Bot(command_prefix=get_prefix,
                   description=c.description,
                   case_insensitive=False)


class DetectURIException(Exception): pass

def ConvertSpotifyURI(url):
    # https://github.com/jpzfm/Spotify-URL-URI-Converter
    if re.search("/track/", url):
        processed = url.split('track/')
        uri = "spotify:track:" + processed[-1][0:22]
    elif re.search("/artist/", url):
        processed = url.split('artist/')
        uri = "spotify:artist:"+processed[-1][0:22]
    elif re.search("/album/", url):
        processed = url.split('album')
        uri = "spotify:album:"+processed[-1][0:22]
    elif re.search("/playlist/", url):
        user = re.search('/user/(.*)/playlist/', url).group(1)
        playlist = url.split('playlist/')
        uri = "spotify:user:" + user + ":playlist:" + playlist[-1][0:22]
    elif re.search(":track:", url):
        processed = url.split('track:')
        uri = "https://open.spotify.com/track/" + processed[-1][0:22]
    elif re.search(":artist:", url):
        processed = url.split('artist:')
        uri = "https://open.spotify.com/artist/" + processed[-1][0:22]
    elif re.search(":album:", url):
        processed = url.split('album:')
        uri = "https://open.spotify.com/album/" + processed[-1][0:22]
    elif re.search(":playlist:", url):
        user = re.search(':user:(.*):playlist:', url).group(1)
        playlist = url.split('playlist:')
        uri = "https://open.spotify.com/user/" + user + "/playlist/" + playlist[-1][0:22]
    else:
        raise DetectURIException("Could not convert url/uri to uri/url")
    return uri


@bot.event
async def on_ready():
    """
    Bot is ready.
    """
    joined_guilds = []
    for guild in bot.guilds:
        #joined_guilds.append(f' - {str(guild.name)}'.ljust(6 + len(max([guild.name for guild in bot.guilds]))) + str(guild.id))
        joined_guilds.append(f' - {str(guild.id).ljust(20)} {guild.name}')

    ready_message = [
        'Logged in as:',
        f'{bot.user.name}: {bot.user.id}',
        f'Discord Version: {discord.__version__}',
        f'\nBot currently running on {len(bot.guilds)} server(s):',
        '\n'.join(joined_guilds)
    ]
    #dashes = '-' * len(max(ready_message, key=len))
    #ready_message = [f'\n{dashes}'] + ready_message + [dashes]
    log.info('\n'.join(ready_message))

    if os.getenv('DOCKERIZED'):
        game_scope = 'docker'
    else:
        game_scope = 'default'
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(c.scoped_games[game_scope]))

@bot.event
async def on_message(message):
    """
    When a message is sent in a channel the bot is a member of.
    """
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
        try:
            uri = ConvertSpotifyURI(message.content)
            await message.add_reaction('🎵')
            def check_reaction(reaction, user):
                return user != bot.user and str(reaction.emoji) == '🎵'
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=240.0, check=check_reaction)
            except asyncio.TimeoutError:
                await message.remove_reaction('🎵', bot.user)
            else:
                await message.remove_reaction('🎵', bot.user)
                await message.channel.send(uri)
        except DetectURIException as err:
            log.debug(err)
            pass
    except:
        pass
    log.info("[%s]%s> %s" % (message.guild.name, message.author.name, message.content))
    await bot.process_commands(message)

@bot.event
async def on_error(error):
    """
    Whan an error occurs.
    """
    log.error('An unexpected error occurred: %s', error)

@bot.event
async def on_command_error(self, exception):
    """
    When a command fails.
    """
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
                                description=f'```css\n{exception}```',
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
    for cog in COGS:
        bot.load_extension(cog)

    log.debug('Starting bot...')
    bot.run(c.data["botToken"], bot=True, reconnect=True)
