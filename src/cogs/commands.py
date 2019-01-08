""" commands -- rufus.py """
import random
import config as c
import os.path
#import urllib.request, json, webbrowser
import wolframalpha, wikipedia, requests
from googletrans import Translator
import time
from time import gmtime, strftime
import discord
from discord.ext import commands


class Commands:
    """ commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def len(self, *, string: str):
        """ Find length of string.
        """
        await self.bot.say('``' + str(len(str(string))) + '``')

    @commands.command()
    async def chars(self, *, string: str):
        """ Find amount of characters in a string, excludes spaces.
        """
        await self.bot.say('``' + str(len(str(string).replace(' ', '').replace('　', ''))) + '``')

    @commands.command()
    async def hello(self, *, greeting: str = ''):
        """ hi there
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
            await self.bot.say('General Kenobi  \\\.(o-o)./')
        else:
            await self.bot.say('{}{} {}'.format(random.choice(c.greetings), random.choice(exclamations), random.choice(reactions)))

    @commands.command(pass_context=True)
    async def roll(self, ctx, *, max: int = 100):
        """ Rolls a random number. Default: 0-100.
        """
        if max <= 0:
            max = 100
        droll = random.randint(0, max)
        if droll == 1:
            suffix = ''
        else:
            suffix = 's'
        if droll <= 0:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point' + str(suffix) + '```')
            await self.bot.say('You need to git gud, rolling isn\'t a joke -.-')
        elif droll == 100:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point' + str(suffix) + '```')
            await self.bot.say('GG!')
        else:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point' + str(suffix) + '```')

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """ Flip a coin.
        """
        cflip = random.choice(['Heads', 'Tails'])
        if cflip == 'Heads':
            await self.bot.add_reaction(ctx.message, '⚪')
            await self.bot.add_reaction(ctx.message, '🇭')
            # await self.bot.add_reaction(ctx.message, '🇪')
            # await self.bot.add_reaction(ctx.message, '🇦')
            # await self.bot.add_reaction(ctx.message, '🇩')
            # await self.bot.add_reaction(ctx.message, '🇸')
        elif cflip == 'Tails':
            await self.bot.add_reaction(ctx.message, '⚫')
            await self.bot.add_reaction(ctx.message, '🇹')
            # await self.bot.add_reaction(ctx.message, '🇦')
            # await self.bot.add_reaction(ctx.message, '🇮')
            # await self.bot.add_reaction(ctx.message, '🇱')
            # await self.bot.add_reaction(ctx.message, '🇸')

    @commands.command()
    async def btc(self):
        """ Show BitCoin price in USD.
        """
        BTC_URL = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        DATA = requests.get(BTC_URL).json()
        BTC_USD = DATA['bpi']['USD']['rate']
        await self.bot.say('```' + 'BTC price is currently at $' + BTC_USD + ' USD' + '```')

    @commands.command()
    async def trump(self, *, searchString: str = 'random'):
        """ Search the extensive database of Tronald Dump for rich knowledge.
        """
        if searchString == 'random':
            URL = 'https://api.tronalddump.io/random/quote'
            DATA = requests.get(URL).json()
            OUT = DATA['value']
            await self.bot.say(OUT)
        else:
            URL = 'https://api.tronalddump.io/search/quote?query={}'.format(searchString)
            DATA = requests.get(URL).json()
            COUNT = DATA['count']
            if COUNT <= 0:
                await self.bot.say('Sorry, Trump never said anything about ``{}``.'.format(searchString))
            else:
                OUT = DATA['_embedded']['quotes'][random.randint(0, COUNT-1)]['value']
                await self.bot.say(OUT)

    @commands.command()
    async def query(self, *, query: str = ''):
        """ Search wolfram alpha for query, if no answer is found, search Wikipedia.
        """
        try:
            client = wolframalpha.Client(c.wolfram_api_key)
            res = client.query(query)
            answer = next(res.results).text
            await self.bot.say('```apache\n{}```'.format(answer))
        except (Exception, StopIteration):
            try:
                wikipedia.set_lang("en")
                summary = wikipedia.summary(query)
                wikiLen = 2000
                if len(summary) > 2000:
                    wikiLoop = 'true'
                    while wikiLoop == 'true':
                        #summary[wikiLen-1:wikiLen].isupper() or
                        if summary[wikiLen-1:wikiLen] == '.':
                            wikiLoop = 'false'
                        else:
                            wikiLen-=1
                    await self.bot.say("``Summary was longer than expected, output truncated.``")
                await self.bot.say(summary[:wikiLen])
            except Exception:
                await self.bot.say('Sorry, no matches were found for ``{}``.'.format(query))

    @commands.command()
    async def translate(self, fromLanguage: str = '', toLanguage: str = '', *, text: str = ''):
        """ Translate string.
        """
        translator = Translator()
        if fromLanguage == '' or toLanguage == '' or text == '':
            await self.bot.say('Missing information.')
        elif fromLanguage == 'auto':
            translatedList = translator.translate([text], dest=toLanguage)
        else:
            translatedList = translator.translate([text], src=fromLanguage, dest=toLanguage)
        for translated in translatedList:
            await self.bot.say('``{}`` -> ``{}``'.format(translated.origin, translated.text))

    @commands.command()
    async def imdb(self, *, searchString: str = ''):
        """ Find information about movies, series etc.
        """
        if not searchString == '':
            URL = 'https://www.omdbapi.com/?t={}&apikey={}'.format(searchString, c.omdb_api_key)
            DATA = requests.get(URL).json()
            await self.bot.say('```apache\nTitle: {}\nDate: {}\nLength: {}\nGenre: {}\nDirector: {}\nActors: {}\n\nPlot: {}```'.format(DATA['Title'], DATA['Released'], DATA['Runtime'], DATA['Genre'], DATA['Director'], DATA['Actors'], DATA['Plot']))

    @commands.command()
    async def urban(self, *, term: str = 'stupid'):
        """ Search Urban Dictionary for word definitions.
        """
        URL = 'http://api.urbandictionary.com/v0/define?term={}'.format(term)
        DATA = requests.get(URL).json()
        DEF = DATA['list'][0]['definition']
        EKS = DATA['list'][0]['example']
        summary = 'Word: {}\n\nDefinition:\n\t{}\n\nUsage:\n\t{}'.format(term, DEF, EKS)
        dictLen = 1990
        if len(summary) > 1990:
            loop = 'true'
            while loop == 'true':
                if summary[dictLen-1:dictLen] == '.':
                    loop = 'false'
                else:
                    dictLen-=1
            await self.bot.say("``Summary was longer than expected, output truncated.``")
        await self.bot.say('```apache\n{}```'.format(summary[:dictLen]))

    @commands.command()
    async def fm(self, *, username: str = ''):
        """ Get currently playing last.fm songs.
        """
        URL = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={}&api_key={}&format=json'.format(username, c.lastfm_api_key)
        DATA = requests.get(URL).json()
        TRACK = DATA['recenttracks']['track'][0]['name']
        ARTIST = DATA['recenttracks']['track'][0]['artist']['#text']
        try:
            NOWPLAYING = DATA['recenttracks']['track'][0]['@attr']['nowplaying']
            NOWPLAYING = 'now playing'
            await self.bot.say('```diff\n-{}\n\n+Track: {}\n-Artist: {}```'.format(NOWPLAYING, TRACK, ARTIST))
        except Exception:
            await self.bot.say('```diff\n-User {} is not scrobbling anything at the moment.```'.format(username))

    @commands.command()
    async def osu!user(self):
        """ A command to interact with the osu! api.
                osu [map/user/replay/score/top/recent/multi] [user] [mode]
        """
        URL = 'https://osu.ppy.sh/api/get_user?k={}&m=0&u=MagicStick'.format(c.osu_api_key)
        DATA = requests.get(URL).json()
        JOIN_DATE = DATA[0]['join_date']
        await self.bot.say(JOIN_DATE)

    @commands.command(pass_context=True)
    async def skin(self, ctx):
        """ current osu! skin.
            Deprecated because docker.
        """
        osu=str("C:\\Users\\{}\\AppData\\Local\\osu!".format(getpass.getuser()))
        f=open(osu+"\\Logs\\runtime.log", "r")
        for line in f:
            line=line.replace("\\", "\\\\")
            if "skin.ini" in line:
                skin=line.split("\\\\skin.ini", 1)[0].split('Skins\\', 1)[-1]
        msg = await self.bot.say("``zipping {}...``".format(skin))
        path = (os.path.dirname(os.path.realpath(__file__)))
        shutil.make_archive(path+"\\temp\\"+skin, 'zip', osu+"\\Skins\\"+skin)
        await self.bot.edit_message(msg, "``{} zipped, getting ready for upload!``".format(skin))
        try:
            await self.bot.send_file(ctx.message.channel, path+"\\temp\\"+skin+".zip")
            await self.bot.edit_message(msg, "``{} uploaded!``".format(skin))
        except:
            await self.bot.edit_message(msg, "``Yikes! The skin file was too large to send, sorry about that.``")
        finally:
            filelist = [ f for f in os.listdir(path+"\\temp") if f.endswith(".zip") ]
            for f in filelist:
                os.remove(os.path.join(path+"\\temp", f))

    @commands.command()
    async def owo(self, *, message: str = 'owo'):
        """ owo~ify something.
        """
        owolist = ['(・`ω´・)', ';;w;;', ';w;', 'owo', 'OwO', 'Owo', 'owO', 'uwu', 'UwU', '>w<', '^w^']
        message = message.replace('l', 'w').replace('L', 'W').replace('r', 'w').replace('R', 'W')
        message = message.replace(',', ' ' + random.choice(owolist)).replace('!', ' ' + random.choice(owolist)).replace('?', ' ' + random.choice(owolist))
        await self.bot.say('```{}```'.format(message))

    @commands.command()
    async def ss(self, *, message: str = ''):
        """ ss-ify something.
        """
        if message == '':
            message = 'ẞß'
        message = message.replace('ss', 'ß').replace('SS', 'ẞ').replace('sS', 'ß').replace('Ss', 'ẞ')
        await self.bot.say('```css\n{}```'.format(message))

    @commands.command(pass_context=True)
    async def poke(self, ctx, user: discord.User = '', *, message: str = ''):
        """ Poke user.
        """
        if user == '':
            await self.bot.say('*You tried poking the air... the air didn\'t respond.*')
        else:

            if message == '':
                await self.bot.say('*{} poked {}*'.format(ctx.message.author.name, user))
            else:
                await self.bot.say('*{} poked {}; ``{}``*'.format(ctx.message.author.name, user, message))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def pat(self, ctx, user: discord.User = '', *, message: str = ''):
        """ Pat user uwu.
        """
        if user == '':
            await self.bot.say('uwu')
        else:
            if message == '':
                await self.bot.say('*{} patted {} and is probably a disgusting weeb!*'.format(ctx.message.author.name, user))
            else:
                await self.bot.say('*{} patted {} {}*'.format(ctx.message.author.name, user, message))

    @commands.command(pass_context=True)
    async def hug(self, ctx, *, user: str = ''):
        """ Hug user.
        """
        mcont = ctx.message.content
        if user == '':
            await self.bot.say('*{} tries to hug the air*'.format(ctx.message.author.name))
        elif user == 'me':
            await self.bot.say('*I hugged {}*'.format(ctx.message.author.name))
        elif user == '<@{}>'.format(ctx.message.author.id):
            await self.bot.say('Aaaaaaall by myseeeeeeeelf.')
        elif user == '<@{}>'.format(self.bot.user.id):
            await self.bot.say(' OwO wat dis? Am I being hugger?' +
                               ' Hmmmm... always be a mystery it will')
        else:
            await self.bot.say('{} hugged {} :hearts:'.format(ctx.message.author.name, user))

    @commands.command()
    async def timer(self, seconds: int, *, name: str = ''):
        """ Starts a countdown timer.
        """
        if name != '':
            name = ' Timer name: {}'.format(name)
        os = seconds
        msg = await self.bot.say('`` {} ``'.format(seconds))
        while seconds > 0:
            time.sleep(1)
            seconds -= 1
            await self.bot.edit_message(msg, '`` {} ``'.format(seconds))
        await self.bot.edit_message(msg, '`` Timer expired. ``')
        await self.bot.say('Time is up! {} seconds have passed.{}'.format(os, name))

    @commands.command(pass_context=True)
    async def echo(self, ctx, *, text: str):
        """ Make the bot say something.
        """
        await self.bot.delete_message(ctx.message)
        await self.bot.say(text)

    @commands.command(pass_context=True)
    async def info(self, ctx, user: discord.User = ''):
        """ User info.
        """
        if not user:
            user=ctx.message.author
        #userDescription = """
#id: {}
#nick: {}
#created at: {}
#joined at: {}
#game: {}
#top role: {}
#bot? {}
#avatar: {}
        #""".format(user.id, user.nick, user.created_at, user.joined_at, user.game, user.top_role, user.bot, user.avatar_url)
        embed=discord.Embed(title='{}#{}'.format(user.name, user.discriminator), color=0x114455)
        embed.set_thumbnail(url=(user.avatar_url))
        embed.set_footer(text=strftime("%d-%m-%Y %H:%M:%S", gmtime()))
        embed.add_field(name="id:", value=user.id, inline=False)
        embed.add_field(name="nick:", value=user.nick, inline=False)
        embed.add_field(name="created at:", value=user.created_at, inline=False)
        embed.add_field(name="joined at:", value=user.joined_at, inline=False)
        embed.add_field(name="game:", value=user.game, inline=False)
        embed.add_field(name="top role:", value=user.top_role, inline=False)
        embed.add_field(name="bot?", value=user.bot, inline=False)
        embed.add_field(name="avatar:", value=user.avatar_url, inline=False)
        await self.bot.say(embed=embed)


def setup(bot):
    """ defines setup """
    bot.add_cog(Commands(bot))
