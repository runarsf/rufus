import config as c
import random
import requests
import time
import os
import json
import base64
import asyncio
import sqlite3
import wolframalpha, wikipedia
from PIL import Image
from time import gmtime, strftime
from googletrans import Translator

from cogs.utils import checks

import discord
from discord.ext import commands

def caesar(string, shift):
    cipher = ''
    for char in string:
        if char == ' ':
            cipher = cipher + char
        elif char.isupper():
            cipher = cipher + chr((ord(char) + shift - 65) % 26 + 65)
        else:
            cipher = cipher + chr((ord(char) + shift - 97) % 26 + 97)
    return cipher

def tally(message, id):
    _embed_stats = []
    _embed_summary = ['The', 'poll', 'has', 'ended', 'with', 'the', 'following', 'results:']
    _embed_summary[2] = str(f'**{message.embeds[0].title}**')
    _embed_summary: str = ' '.join(_embed_summary)
    nl = '\n'
    for index, reaction in enumerate(message.reactions):
        _embed_summary += f'\n {int(reaction.count)-1}: {message.embeds[0].description.split(f"{nl}")[index][3:]}'
    _embed = discord.Embed(title='Poll ended!', description=str(_embed_summary), color=message.embeds[0].color)
    _embed.set_footer(text=f'Poll ID: {id}')
    return _embed

class CommandsCog(commands.Cog, name="General Commands"):
    """ CommandsCog """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='scramble', aliases=['spoiler'])
    async def _scramble(self, ctx, *, text: str =''):
        """ Scramble a message and delete the original one, react with the given emoji to unscramble.
        """
        await ctx.message.delete()
        channel = ctx.message.channel
        message = await ctx.send(caesar(text, 8))

        await message.add_reaction('❓')

        def check(reaction, user):
            return user != self.bot.user and str(reaction.emoji) == '❓'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
        except asyncio.TimeoutError:
            pass
        else:
            await message.edit(content=str(text))
        await message.remove_reaction('❓', self.bot.user)

    @commands.command(name='bang', hidden=True)
    async def _duckduckgo_bangs(self, ctx, bang: str, *, query: str):
        """ Search using DuckDuckGo bangs.
        """
        requestUrl = 'https://api.duckduckgo.com/?q={bang}+{query.replace(" ", "+")}&format=json&pretty=1&no_redirect=1&t=rufusDiscordBot'
        DATA = requests.get(requestUrl).json()
        DATA = json.loads(DATA)
        await ctx.send(f'```{DATA["Redirect"]}```')

    @commands.command(name='color', aliases=['hex', 'colorsquare'])
    async def _visualize_hex(self, ctx, color: str):
        """ Generate a 128x128px colored square from a color code.
            Example values:
             - Hex => #306998
             - RGB => "rgb(0, 35, 102)"
        """
        img = Image.new('RGB', (128, 128), color)
        img.save(f'tempcolor{ctx.message.author.id}.png')
        await ctx.send(file=discord.File(f'tempcolor{ctx.message.author.id}.png'))
        os.remove(f'tempcolor{ctx.message.author.id}.png')

    @commands.command(name='setvar', aliases=['setvariable', 'set'])
    @checks.is_dev()
    async def _set_db_var(self, ctx, variableName: str, *, variableValue: str):
        """ Assign a value to a variable.
            Value DELETE_ME will delete variable.
        """
        db = sqlite3.connect('uservars.db')
        cr = db.cursor()
        cr.execute('CREATE TABLE IF NOT EXISTS variables(keyword TEXT UNIQUE, value TEXT, owner INTEGER)')
        varexist: bool = False
        cr.execute('SELECT keyword, owner FROM variables')
        for row in cr.fetchall():
            if row[0] == variableName:
                is_owner = await ctx.bot.is_owner(ctx.message.author)
                if int(row[1]) == ctx.message.author.id or is_owner:
                    if variableValue == 'DELETE_ME':
                        cr.execute("DELETE FROM variables WHERE keyword = (?)",
                                  (variableName,))
                        db.commit()
                    else:
                        if variableValue == '++':
                            cr.execute('SELECT keyword, value FROM variables')
                            for row in cr.fetchall():
                                if row[0] == variableName:
                                    variableValue = str(int(row[1]) + 1)
                                    break
                        elif variableValue == '--':
                            cr.execute('SELECT keyword, value FROM variables')
                            for row in cr.fetchall():
                                if row[0] == variableName:
                                    variableValue = str(int(row[1]) - 1)
                                    break
                        cr.execute("UPDATE variables SET value = (?) WHERE keyword = (?)",
                                  (variableValue, variableName))
                        db.commit()
                else:
                    await ctx.send('Variable already exists and is not owned by you.')
                varexist: bool = True
        if not varexist:
            cr.execute("INSERT INTO variables (keyword, value, owner) VALUES (?, ?, ?)",
                     (variableName, variableValue, ctx.message.author.id))
            db.commit()

        cr.execute('SELECT keyword, value, owner FROM variables')
        for row in cr.fetchall():
            if row[0] == variableName:
                await ctx.send(row)
        cr.close()
        db.close()

    @commands.command(name='getvar', aliases=['getvariable', 'readvar', 'readvariable', 'get'])
    @checks.is_dev()
    async def _get_db_var(self, ctx, variableName: str):
        """ Get value from a variable.
        """
        db = sqlite3.connect('uservars.db')
        cr = db.cursor()
        try:
            cr.execute('SELECT keyword, value FROM variables')
            for row in cr.fetchall():
                if row[0] == variableName:
                    await ctx.send(row[1])
        except:
            await ctx.send('No table found, you should create one with the ``setvar`` command.')
        cr.close()
        db.close()

    @commands.command(name='length', aliases=['len'])
    async def _length(self, ctx, *, string: str):
        """ Find length of string.
        """
        await ctx.send('``' + str(len(str(string))) + '``')

    @commands.command(name='characters', aliases=['char', 'chars'])
    async def _characters(self, ctx, *, string: str):
        """ Find character length of string.
        """
        await ctx.send('``' + str(len(str(string).replace(' ', '').replace('　', ''))) + '``')

    @commands.command(name='poll')
    async def _poll(self, ctx, timeout: int, title: str, *choices: str):
        """ Create a poll.
        """
        if len(choices) > 10:
            await ctx.send('Too many choices, choice index cannot exceed 10.')
            return
        if len(choices) < 1:
            await ctx.send('Too few choices, you need at least one.')
            return

        if len(choices) == 2 and choices[0].lower() == 'yes' and choices[1].lower() == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        choice_summary = []
        for key, value in enumerate(choices, start=1):
            choice_summary += f'\n {key}: {value}'
        _embed = discord.Embed(title=title, description=''.join(choice_summary), color=discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))
        message = await ctx.send(embed=_embed)
        for reaction in reactions[:len(choices)]:
            await message.add_reaction(reaction)
        _embed.set_footer(text=f'Poll ID: {message.id}')
        await message.edit(embed=_embed)
        await message.pin()
        async for msg in ctx.channel.history():
            if msg.type == discord.MessageType.pins_add:
                await msg.delete()
                continue
        if int(timeout) > 0:
            await asyncio.sleep(timeout)
            msg = await ctx.get_message(message.id)
            await message.unpin()
            await ctx.send(embed=tally(msg, msg.id))

    @commands.command(name='tally')
    async def _poll_tally(self, ctx, id: int):
        """ Tally poll.
        """
        message = await ctx.get_message(id)
        await message.unpin()
        await ctx.send(embed=tally(message, id))

    @commands.command(name='repeat', aliases=['combine'])
    async def _repeat(self, ctx, times: int = 1, *, repeatString: str = ''):
        """ Repeat the specified string.
        """
        i = 1
        outString = str('')
        while i <= times:
            outString = outString + repeatString.replace(' ', '')
            i = i + 1
        await ctx.send(f'``{outString}``')

    @commands.command(name='input')
    async def _wait_for_input(self, ctx):
        channel = ctx.message.channel
        await channel.send('Say hello!')
        def check(m):
            return m.content == 'hello' and m.channel == channel
        msg = await self.bot.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))

    @commands.command(name='hello', hidden=True)
    async def _greet(self, ctx, *, greeting: str = ''):
        """ hello there
        """
        exclamations = [
            '',
            '!'
        ]
        reactions = [
            'owo',
            'uwu',
            '>w<',
            '^w^',
            '(´・ω・)っ',
            '(•◡•)/',
            '(っ◕‿◕)っ',
            '(◕‿◕)'
        ]
        if greeting == 'there':
            await ctx.send('General Kenobi  \\\.(o-o)./')
        else:
            await ctx.send(f'{random.choice(c.greetings)}{random.choice(exclamations)} {random.choice(reactions)}')

    @commands.command(name='roll', aliases=['random'])
    async def _roll(self, ctx, min: int = 0, max: int = 100):
        """ Rolls a random number.
        """
        suffix = 's'
        if max <= min:
            max = min + 1
        droll = random.randint(int(min), int(max))
        if droll == 1:
            suffix = ''
        if int(droll) <= int(min) and int(droll) != int(min):
            await ctx.send(f'```{ctx.message.author.name} rolls {str(droll)} point{str(suffix)}.```')
            await ctx.send('You need to git gud, rolling isn\'t a joke -.-')
        elif int(droll) == int(max) and int(droll) != int(min):
            await ctx.send(f'```{ctx.message.author.name} rolls {str(droll)} point{str(suffix)}.```')
            await ctx.send('GG!')
        else:
            await ctx.send(f'```{ctx.message.author.name} rolls {str(droll)} point{str(suffix)}.```')

    @commands.command(name='flip')
    async def _flip(self, ctx):
        """ Flip a coin.
        """
        cflip = random.choice(['Heads', 'Tails'])
        if cflip == 'Heads':
            await ctx.message.add_reaction('⚪')
            await ctx.message.add_reaction('🇭') #🇪🇦🇩🇸
        elif cflip == 'Tails':
            await ctx.message.add_reaction('⚫')
            await ctx.message.add_reaction('🇹') #🇦🇮🇱🇸

    @commands.command(name='btc', aliases=['bitcoin'])
    async def _bitcoin(self, ctx):
        """ Show BitCoin price in USD.
        """
        BTC_URL = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        DATA = requests.get(BTC_URL).json()
        BTC_USD = DATA['bpi']['USD']['rate']
        await ctx.send(f'```BTC price is currently at ${BTC_USD} USD```')

    @commands.command(name='trump', aliases=['drumpf', 'dump', 'tronald'])
    async def _trump(self, ctx, *, searchString: str = 'random'):
        """ Search the extensive database of Tronald Dump for rich knowledge.
        """
        if searchString == 'random':
            URL = 'https://api.tronalddump.io/random/quote'
            DATA = requests.get(URL).json()
            OUT = DATA['value']
            await ctx.send(f'```{OUT}```')
        else:
            URL = f'https://api.tronalddump.io/search/quote?query={searchString}'
            DATA = requests.get(URL).json()
            COUNT = DATA['count']
            if COUNT <= 0:
                await ctx.send(f'Sorry, Trump never said anything about ``{searchString}``')
            else:
                OUT = DATA['_embedded']['quotes'][random.randint(0, COUNT-1)]['value']
                await ctx.send(f'```{OUT}```')

    @commands.command(name='query', aliases=['what', 'is', 'am'])
    async def _query(self, ctx, *, searchString: str = ''):
        """ Search Wolfram alpha for query, if no answer is found, search Wikipedia.
        """
        try:
            client = wolframalpha.Client(c.wolfram_api_key)
            res = client.query(searchString)
            answer = next(res.results).text
            await ctx.send(f'```apache\n{answer}```')
        except (Exception, StopIteration):
            try:
                wikipedia.set_lang("en")
                summary = wikipedia.summary(searchString)
                wikiLen = 2000
                if len(summary) > 2000:
                    wikiLoop = 'true'
                    while wikiLoop == 'true':
                        #summary[wikiLen-1:wikiLen].isupper() or
                        if summary[wikiLen-1:wikiLen] == '.':
                            wikiLoop = 'false'
                        else:
                            wikiLen-=1
                    await ctx.send('``Summary was longer than expected, output truncated.``')
                await ctx.send(f'```{summary[:wikiLen]}```')
            except Exception:
                await ctx.send(f'Sorry, no matches were found for ``{query}``.')
        finally:
            try:
                channel = ctx.message.channel
                thankers = ['thank you', 'thanks']
                def check(m):
                    return any(thanks in m.content for thanks in thankers) and m.channel == channel
                msg = await self.bot.wait_for('message', check=check, timeout=25)
                await channel.send('You\'re welcome :⁾')
            except Exception:
                return

    @commands.command(name='translate', aliases=['tr'])
    async def _translate(self, ctx, fromLanguage: str = '', toLanguage: str = '', *, text: str = ''):
        """ Translate string.
        """
        translator = Translator()
        if fromLanguage == '' or toLanguage == '' or text == '':
            await ctx.send('```Missing information.```')
        elif fromLanguage == 'auto' or fromLanguage == 'au':
            translatedList = translator.translate([text], dest=toLanguage)
        else:
            translatedList = translator.translate([text], src=fromLanguage, dest=toLanguage)
        for translated in translatedList:
            if len(f'``{translated.origin}`` -> ``{translated.text}``') >= 2000:
                await ctx.send(f'```{translated.text}```')
            else:
                await ctx.send(f'``{translated.origin}`` -> ``{translated.text}``')

    @commands.command(name='imdb', aliases=['omdb', 'movie', 'series'])
    async def _imdb(self, ctx, *, searchString: str = ''):
        """ Find information about movies, series etc.
        """
        if not searchString == '':
            URL = f'https://www.omdbapi.com/?t={searchString}&apikey={c.omdb_api_key}'
            DATA = requests.get(URL).json()
            try:
                await ctx.send(f'```apache\nTitle: {DATA["Title"]}\nDate: {DATA["Released"]}\nLength: {DATA["Runtime"]}\nGenre: {DATA["Genre"]}\nDirector: {DATA["Director"]}\nActors: {DATA["Actors"]}\n\nPlot: {DATA["Plot"]}```')
            except Exception as error:
                await ctx.send(f'```No movie or series with the title \'{searchString}\' was found.\n{type(error).__name__}: {error}```')

    @commands.command(name='urban', alias=['dictionary', 'dict'])
    async def _urban(self, ctx, *, term: str = 'stupid'):
        """ Search Urban Dictionary for word definitions.
        """
        URL = f'http://api.urbandictionary.com/v0/define?term={term}'
        DATA = requests.get(URL).json()
        DEF = DATA['list'][0]['definition']
        EKS = DATA['list'][0]['example']
        summary = f'Word: {term}\n\nDefinition:\n\t{DEF}\n\nUsage:\n\t{EKS}'
        dictLen = 1990
        if len(summary) > 1990:
            loop = 'true'
            while loop == 'true':
                if summary[dictLen-1:dictLen] == '.':
                    loop = 'false'
                else:
                    dictLen-=1
            await ctx.send('``Summary was longer than expected, output truncated.``')
        await ctx.send(f'```apache\n{summary[:dictLen]}```')

    @commands.command(name='lastfm', aliases=['last', 'fm'])
    async def _lastfm(self, ctx, username: str = '', detailed: str = 'false'):
        """ Get currently playing last.fm songs.
        """
        if detailed == '1' or detailed == 'yes':
            detailed = 'true'
        URL = f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={c.lastfm_api_key}&format=json'
        DATA = requests.get(URL).json()
        TRACK = DATA['recenttracks']['track'][0]['name']
        ARTIST = DATA['recenttracks']['track'][0]['artist']['#text']
        ALBUM = DATA['recenttracks']['track'][0]['album']['#text']
        if detailed == 'true':
            try:
                NOWPLAYING = DATA['recenttracks']['track'][0]['@attr']['nowplaying']
                FM_URL = DATA['recenttracks']['track'][0]['url']
                IMAGE = DATA['recenttracks']['track'][0]['image'][3]['#text']
                await ctx.send(f'```apache\nTrack: {TRACK}\nArtist: {ARTIST}\nAlbum: {ALBUM}\n\nURL: {FM_URL}\nImage: {IMAGE}```')
            except Exception:
                await ctx.send(f'```User {username} is not scrobbling anything at the moment.```')
        else:
            try:
                NOWPLAYING = DATA['recenttracks']['track'][0]['@attr']['nowplaying']
                await ctx.send(f'```brainfuck\n{ARTIST} : {TRACK} ( {ALBUM} )```')
            except Exception:
                await ctx.send(f'```User {username} is not scrobbling anything at the moment.```')

    @commands.command(name='poke')
    @commands.guild_only()
    async def _poke(self, ctx, member: discord.Member = '', *, message: str = ''):
        """ Poke user.
        """
        if member == '':
            await ctx.send('*You tried poking the air... the air didn\'t respond.*')
        else:
            if message == '':
                await ctx.send(f'*{ctx.message.author.name} poked {member}*')
            else:
                await ctx.send(f'*{ctx.message.author.name} poked {member}; ``{message}``*')
            await ctx.message.delete()

    @commands.command(name='timer', aliases=['countdown'])
    async def _countdown(self, ctx, seconds: int, *, name: str = ''):
        """ Starts a countdown timer.
        """
        if name != '':
            name = f' Timer name: {name}'
        os = seconds
        msg = await ctx.send(f'`` {os} ``')
        while seconds > 0:
            await asyncio.sleep(1)
            seconds -= 1
            await msg.edit(content=f'`` {seconds} ``')
        await ctx.send(f'Time is up! {os} seconds have passed.{name}')

    @commands.command(name='info', aliases=['inf', 'userinfo'])
    async def _info(self, ctx, *, member: discord.Member = ''):
        """ User info.
        """
        if not member:
            member=ctx.message.author
        embed=discord.Embed(title=f'{member.name}#{member.discriminator}', color=0x114455)
        embed.set_thumbnail(url=(member.avatar_url))
        embed.set_footer(text=strftime("%d-%m-%Y %H:%M:%S", gmtime()))
        embed.add_field(name="id:", value=member.id, inline=True)
        embed.add_field(name="nick:", value=member.nick, inline=True)
        embed.add_field(name="created at:", value=member.created_at, inline=True)
        embed.add_field(name="joined at:", value=member.joined_at, inline=True)
        embed.add_field(name="game:", value=str(member.activities).replace('()', 'None'), inline=True)
        embed.add_field(name="top role:", value=member.top_role, inline=True)
        embed.add_field(name="bot?", value=member.bot, inline=True)
        embed.add_field(name="avatar url:", value=member.avatar_url, inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    #bot.remove_command('help')
    bot.add_cog(CommandsCog(bot))
