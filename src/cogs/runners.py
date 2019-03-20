import config as c
import re
import docker

from cogs.utils import checks

import discord
from discord.ext import commands

class runner():
    def python():
        containerLogs = []
        client = docker.DockerClient(base_url='unix://var/run/docker.sock', timeout=10)
        container = client.containers.run('ubuntu:16.04',command="bash -c ' for((i=1;i<=10;i+=2)); do echo Welcome $i times; sleep 10; done'", detach=True)
        logs = container.logs(stream=True)
        for line in logs:
            containerLogs.append(line)
        return containerLogs


class RunnerCog(commands.Cog, name="Runner Commands"):
    """ RunnerCog """

    def __init__(self, bot):
        self.bot = bot

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
                    if lang == 'python' or 'py':
                        await ctx.send(runner.python())
                    return
                else:
                    await ctx.send('```No supported languages detected in header.```')
                    return
            counter += 1

def setup(bot):
    bot.add_cog(RunnerCog(bot))
