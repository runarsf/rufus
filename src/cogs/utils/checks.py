import config as c

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
