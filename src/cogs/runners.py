import config as c
import re
import os
import shutil
import subprocess

from cogs.utils import checks

import discord
from discord.ext import commands


class Runners():
    """ Runners for different languages.
    """
    def python(message, code: str):
        # make folder to hold temporary files
        homedir =f'{c.srcDir}/runners/{message.author.id}'
        if os.path.isdir(homedir):
            return 'File already exists.'
        else:
            os.mkdir(homedir)

        # write code to a temporary file
        with open(f'{homedir}/code.py', 'w+') as codeFile:
            codeFile.write(code)

        # make dockerfile
        dockerfile = f"""FROM python
COPY {homedir} /discordappapp
WORKDIR /discordappapp
CMD ['python3', '-u', '{homedir}/code.py']"""
        with open(f'{homedir}/dockerfile', 'w+') as dockerfileFile:
            dockerfileFile.write(dockerfile)

        # run container and capture output
        with open(f'{homedir}/output.py', 'a') as outputFile:
            subprocess.call(f'cd {homedir} && docker build -t {message.author.id}rbot . && docker run --rm {message.author.id}rbot', shell=True, stdout=outputFile, stderr=outputFile)
        with open(f'{homedir}/output.py', 'r') as outputFile:
            result = outputFile.readlines()

        shutil.rmtree(homedir)
        return result

class RunnerCog(commands.Cog, name="Runner Commands"):
    """ RunnerCog """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='docker')
    @commands.is_owner()
    async def _docker_test(self, ctx):
        """ Docker test.
        """
        testCode = """i = 1
print(i)"""
        await ctx.send('```python\n{}```'.format('\n'.join(Runners.python(ctx.message, testCode))))

    @commands.command(name='run')
    @commands.is_owner()
    async def _runner(self, ctx, customLimit: int = 2):
        """ Run the most recent code block written by you.
            Custom limit may not exceed 50 messages.
        """
        counter = 0
        languages = ['python', 'py']
        customLimit = 50 if customLimit > 50 else customLimit
        async for message in ctx.channel.history(limit=int(customLimit)):
            if message.content.startswith('```') and message.content.endswith('```') and message.author.id == ctx.message.author.id:
                lang = str(re.findall(r'^\w+[^\n]', message.content[3:-3])).strip('[\',]')
                if any(lin in lang for lin in languages):
                    if lang == 'python' or lang == 'py':
                        await ctx.send('```python\n{}```'.format('\n'.join(Runners.python(ctx.message, message.content[3+len(lang):-3]))))
                    return
                else:
                    await ctx.send('```No supported languages detected in codeblock header.```')
                    return
            counter += 1

def setup(bot):
    bot.add_cog(RunnerCog(bot))
