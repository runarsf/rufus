import config as c

import discord
from discord.ext import commands


async def bot_check_role(ctx, role):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True
    resolved = ctx.author.roles
    result = role.lower() in (r.name.lower() for r in resolved)
    if result is False:
        raise ZeroDivizionError

def bot_has_role(role):
    async def pred(ctx):
        return await bot_check_role(ctx, role)
    return commands.check(pred)

#async def is_dev():
#    return await ctx.message.author.id in c.dev_id
