""" admin -- rufus.py """
from discord.ext import commands
import getpass
import config as c
import os
import re
import subprocess


class Dev:
    """ dev stuff """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self):
        """ Ping the bot host.
        """
        await self.bot.say('pong 🏓')

    @commands.command(pass_context=True)
    async def pwd(self, ctx):
        """ Print Working Directory.
        """
        if str(ctx.message.author.id) in str(c.owner_id) or str(c.dev_id):
            path = (os.path.dirname(os.path.realpath(__file__)))
            await self.bot.say(path)
        else:
            await self.bot.say('```diff\n-Insufficient privileges.```')

    @commands.command(pass_context=True)
    async def clear(self, ctx):
        """ Clears the console.
            Windows only. Deprecated.
        """
        if str(ctx.message.author.id) in str(c.owner_id) or str(c.dev_id):
            clear = lambda: os.system('cls')
            clear()
            print('Console cleared by {}'.format(ctx.message.author.name))
            await self.bot.delete_message(ctx.message)
        else:
            await self.bot.say('```diff\n-Insufficient privileges.```')

    @commands.command(pass_context=True)
    async def cogs(self, ctx):
        """ Lists out all existing cogs.
        """
        cogger=''
        if str(ctx.message.author.id) in str(c.owner_id) or str(c.dev_id):
            for file in os.listdir('./cogs'):
                if not file == 'uptime.py' and file.endswith('.py'):
                    cogger += (file+' ')
            self.bot.say('```{}```'.format(cogger))
        else:
            await self.bot.say('```diff\n-Insufficient privileges.```')

    @commands.command()
    async def bug(self):
        """ Submit a bug.
        """
        await self.bot.say('Submit a bug: https://github.com/runarsf/rufus/issues/new')

    @commands.command(pass_context=True)
    async def run(self, ctx, customLimit: int = 2):
        """ Run the most recent code block written by you.
            Custom limit may not exceed 50 messages.
        """
        counter = 0
        languages = ['python']
        if customLimit > 50:
            customLimit = 50
            await self.bot.say('```diff\n-Custom limit may not exceed 50 messages, reduced to 50.```')
        async for message in self.bot.logs_from(ctx.message.channel, limit=int(customLimit)):
            if message.content.startswith('```') and message.content.endswith('```') and message.author.id == ctx.message.author.id:
                #lang = str(message.content).split(' ', 1)[0][3:]
                lang = str(re.findall(r'^\w+[^\n]', message.content[3:-3])).strip('[\',]')
                if any(lin in lang for lin in languages): # then check if it's a supported language
                    #await self.bot.say('```{}\n{}```'.format(lang, re.sub(r'^\w+\s{1}', '', message.content[3:-3])))
                    with open('./runners/{}.{}'.format(lang, lang), 'w') as runner_file:
                        runner_file.write(re.sub(r'^\w+\s{1}', '', message.content[3:-3]))
                    await self.bot.say(subprocess.run([lang, './runners/{}.{}'.format(lang, lang)], stdout=subprocess.PIPE).stdout.decode('utf-8'))
                    return
                else:
                    await self.bot.say('```diff\n-No supported languages detected in header.```')
                    return
            counter += 1

def setup(bot):
    """ defines setup """
    bot.add_cog(Dev(bot))
