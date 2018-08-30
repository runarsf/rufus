""" commands -- rufus.py """
import asyncio
import threading
# unused import subprocess
# unused import sys
# unused import os
import config as c

import discord
from discord.ext import commands

class Test:
    """ Admin restriced commands """

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    """ defines setup """
    bot.add_cog(Test(bot))