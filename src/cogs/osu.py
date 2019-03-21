import config as c
import os.path
import requests
import time
import asyncio
import urllib.request
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from cogs.utils import countrycodes as cc

import discord
from discord.ext import commands


def getDominantColor(filename: str):
    #Resizing parameters
    width, height = 150,150
    response = requests.get(filename)
    image = Image.open(BytesIO(response.content))
    image = image.resize((width, height),resample = 0)
    #Get colors from image object
    pixels = image.getcolors(width * height)
    #Sort them by count number(first element of tuple)
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    #Get the most frequent color
    dominant_color = sorted_pixels[-1][1]
    hexColor = discord.Color.from_rgb(dominant_color[0], dominant_color[1], dominant_color[2])
    return hexColor

# def scraper(url: str, phrase: str = '<div class="beatmapset-header__content" style="background-image: url("URL_HERE");">'):
    #from bs4 import BeautifulSoup
    #import urllib.request
    #import re
    #import time

    #html_page = urllib.request.urlopen("https://osu.ppy.sh/beatmaps/1149713")
    #html_page = urllib.request.urlopen("https://osu.ppy.sh/beatmapsets/542081#osu/1149713")
    #soup = BeautifulSoup(html_page, features="html.parser")
    #soup = soup.findAll('div')

    #for line in soup:
    #    print(f'\n\n{line}')

class OsuCog(commands.Cog, name="osu!"):
    """ OsuCog """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='osu!update', aliases=['u', 'update'])
    async def _osu_update(self, ctx, username: str):
        """ Get recent osu! plays for player.
            Available modes:
                - osu!
                - taiko
                - ctb
                - mania
        """
        pass

    @commands.command(name='osu!recent', aliases=['recent'])
    async def _osu_most_recent(self, ctx, username: str, mode: str = 'osu!'):
        """ Get most recent osu! play for player.
            Available modes:
                - osu!
                - taiko
                - ctb
                - mania
        """
        if mode.lower() == 'osu!':
            mode = 0
        elif mode.lower() == 'taiko':
            mode = 1
        elif mode.lower() == 'ctb':
            mode = 2
        elif mode.lower() == 'mania' or mode.lower() == 'osu!mania':
            mode = 3

        recentUrl = f'https://osu.ppy.sh/api/get_user_recent?k={c.osu_api_key}&u={username}&type=string&m={mode}'
        recentData = requests.get(recentUrl).json()
        beatmapUrl = f'https://osu.ppy.sh/api/get_beatmaps?k={c.osu_api_key}&b={recentData[0]["beatmap_id"]}'
        beatmapData = requests.get(beatmapUrl).json()

        embed=discord.Embed(title=f'most recent play for {username}', color=getDominantColor('https://assets.ppy.sh/beatmaps/542081/covers/cover.jpg?1521116828'))
        embed.set_thumbnail(url=(f'{scraper("https://osu.ppy.sh/beatmaps/"+recentData[0]["beatmap_id"])}'))
        await ctx.send(embed=embed)

    @commands.command(name='osu!user', aliases=['player'])
    async def _osu_user(self, ctx, username: str, mode: str = 'osu!'):
        """ Get osu! user information.
            Available modes:
                - osu!
                - taiko
                - ctb
                - mania
        """
        def getTopBeatmaps(amount: int = 1):
            result = ''
            bestUrl = f'https://osu.ppy.sh/api/get_user_best?k={c.osu_api_key}&m={mode}&limit=3&u={username}&type=string'
            bestData = requests.get(bestUrl).json()
            for times in range(amount):
                bestMapsUrl = f'https://osu.ppy.sh/api/get_beatmaps?k={c.osu_api_key}&b={bestData[times]["beatmap_id"]}'
                bestMapsData = requests.get(bestMapsUrl).json()
                result = f'{result}\n\t{times+1}. {bestMapsData[0]["title"]}'
            return result

        if mode.lower() == 'osu!':
            mode = 0
        elif mode.lower() == 'taiko':
            mode = 1
        elif mode.lower() == 'ctb':
            mode = 2
        elif mode.lower() == 'mania' or mode.lower() == 'osu!mania':
            mode = 3

        userUrl = f'https://osu.ppy.sh/api/get_user?k={c.osu_api_key}&m={mode}&u={username}&type=string'
        userData = requests.get(userUrl).json()

        embed=discord.Embed(title=f'osu! user information for {userData[0]["username"]}', color=getDominantColor(f'https://a.ppy.sh/{userData[0]["user_id"]}'))
        embed.set_thumbnail(url=(f'https://a.ppy.sh/{userData[0]["user_id"]}'))
        embed.set_footer(text='')
        embed.add_field(name="Username:", value=userData[0]["username"], inline=True)
        embed.add_field(name="ID:", value=userData[0]["user_id"], inline=True)
        embed.add_field(name="Created:", value=userData[0]["join_date"], inline=True)
        embed.add_field(name="300:", value=userData[0]["count300"], inline=True)
        embed.add_field(name="100:", value=userData[0]["count100"], inline=True)
        embed.add_field(name="50:", value=userData[0]["count50"], inline=True)
        embed.add_field(name="Plays:", value=userData[0]["playcount"], inline=True)
        embed.add_field(name="Level:", value=userData[0]["level"], inline=True)
        embed.add_field(name="PP:", value=userData[0]["pp_raw"], inline=True)
        embed.add_field(name="Accuracy:", value=userData[0]["accuracy"], inline=True)
        embed.add_field(name="SS/SSH:", value=f'{userData[0]["count_rank_ss"]}/{userData[0]["count_rank_ssh"]}', inline=True)
        embed.add_field(name="S/SH:", value=f'{userData[0]["count_rank_s"]}/{userData[0]["count_rank_sh"]}', inline=True)
        embed.add_field(name="A:", value=userData[0]["count_rank_a"], inline=True)
        embed.add_field(name="Country:", value=f'{cc.countryCodes[userData[0]["country"]]} ({userData[0]["country"]})', inline=True)
        embed.add_field(name="Profile:", value=f'https://osu.ppy.sh/u/{userData[0]["user_id"]}', inline=True)
        embed.add_field(name="Top Scores:", value=getTopBeatmaps(3), inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='skin', hidden=True)
    @commands.is_owner()
    async def _osu_skin(self, ctx):
        """ current osu! skin.
            Deprecated because docker and hosted on different machine.
        """
        if True:
            await self.bot.say('Command temporarily disabled.')
        elif False:
            # should search for osu! location, this isn't always correct
            osu=str(f'C:\\Users\\{getpass.getuser()}\\AppData\\Local\\osu!')
            f=open(osu+'\\Logs\\runtime.log', 'r')
            for line in f:
                line=line.replace("\\", "\\\\")
                if 'skin.ini' in line:
                    skin=line.split('\\\\skin.ini', 1)[0].split('Skins\\', 1)[-1]
            msg = await self.bot.say('``zipping {}...``'.format(skin))
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


def setup(bot):
    bot.add_cog(OsuCog(bot))
