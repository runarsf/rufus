import config as c
import discord
from discord.ext import commands

client = commands.Bot(description=c.description, command_prefix=c.prefix)

class Commands:
    """ I legit want to kill myself """
    
    @client.command(pass_context=True)
    async def ping(self, ctx):
        """ Pings the bot host """
        print(ctx.message.author.name + ' ' + ctx.message.author.id + ' ' + ctx.message.content)
        await client.say('pong 🏓')