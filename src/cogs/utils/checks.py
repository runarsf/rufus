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
        return ctx.message.author.id in c.dev_ids

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
