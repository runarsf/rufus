import config as c

import urllib.request
import requests
from PIL import Image
from io import BytesIO

import discord
from discord.ext import commands


async def user_is_developer(ctx):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True
    else:
        return ctx.message.author.id in c.dev_id
    #is_dev = await ctx.message.author.id in c.dev_id
    #if is_dev:
    #    return True
    #else:
    #    return False

def is_dev():
    async def checker(ctx):
        return await user_is_developer(ctx)
    return commands.check(checker)

def getDominantColor(filename: str):
    try:
        #Resizing parameters
        width, height = 150, 150
        response = requests.get(filename)
        image = Image.open(BytesIO(response.content))
        image = image.resize((width, height), resample=0)
        #Get colors from image object
        pixels = image.getcolors(width * height)
        #Sort them by count number(first element of tuple)
        sorted_pixels = sorted(pixels, key=lambda t: t[0])
        #Get the most frequent color
        dominant_color = sorted_pixels[-1][1]
        hexColor = discord.Color.from_rgb(
            dominant_color[0], dominant_color[1], dominant_color[2])
        return hexColor
    except:
        return discord.Color.from_rgb(48, 105, 152)

# from bs4 import BeautifulSoup
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
