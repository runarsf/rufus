import config as c
import random
import discord
import requests
import time
import wolframalpha, wikipedia
from time import gmtime, strftime
from googletrans import Translator
from discord.ext import commands


class CommandsCog(commands.Cog, name="General Commands"):
    """ CommandsCog """

    def __init__(self, bot):
        self.bot = bot

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
                await ctx.send(summary[:wikiLen])
            except Exception:
                await ctx.send(f'Sorry, no matches were found for ``{query}``.')

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
            time.sleep(1)
            seconds -= 1
            await msg.edit(content=f'`` {seconds} ``')
        await ctx.send(f'Time is up! {os} seconds have passed.{name}')

    @commands.command(name='echo', aliases=['say', 'print', 'printf'])
    async def _echo(self, ctx, *, phrase: str):
        """ Make the bot say something.
        """
        await ctx.message.delete()
        await ctx.send(phrase)

    @commands.command(name='info', aliases=['inf', 'userinfo'])
    async def _info(self, ctx, *, member: discord.Member = ''):
        """ User info.
        """
        if not member:
            member=ctx.message.author
        embed=discord.Embed(title=f'{member.name}#{member.discriminator}', color=0x114455)
        embed.set_thumbnail(url=(member.avatar_url))
        embed.set_footer(text=strftime("%d-%m-%Y %H:%M:%S", gmtime()))
        embed.add_field(name="id:", value=member.id, inline=False)
        embed.add_field(name="nick:", value=member.nick, inline=False)
        embed.add_field(name="created at:", value=member.created_at, inline=False)
        embed.add_field(name="joined at:", value=member.joined_at, inline=False)
        embed.add_field(name="game:", value=str(member.activities).replace('()', 'None'), inline=False)
        embed.add_field(name="top role:", value=member.top_role, inline=False)
        embed.add_field(name="bot?", value=member.bot, inline=False)
        embed.add_field(name="avatar url:", value=member.avatar_url, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CommandsCog(bot))
