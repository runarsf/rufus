""" admin -- rufus.py """
from discord.ext import commands
import getpass
import config as c
import shutil
import os


class osu:
    """ osu! commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def osu(self, cmd, *, msg):
        """ osu! command collection.
                Argslist:
                    map
                    user
        """
        if cmd == 'map':
            await self.bot.say('https://osu.ppy.sh/p/beatmaplist?q=' + msg.replace(' ', '%20'))
        if cmd == 'user':
            await self.bot.say('https://osu.ppy.sh/users/' + msg.replace(' ', '%20'))

    @commands.command(pass_context=True)
    async def skin(self, ctx):
        """ current osu! skin.
            Deprecated because docker.
        """
        osu=str("C:\\Users\\{}\\AppData\\Local\\osu!".format(getpass.getuser()))
        f=open(osu+"\\Logs\\runtime.log", "r")
        for line in f:
            line=line.replace("\\", "\\\\")
            if "skin.ini" in line:
                skin=line.split("\\\\skin.ini", 1)[0].split('Skins\\', 1)[-1]
        msg = await self.bot.say("``zipping {}...``".format(skin))
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
    """ defines setup """
    bot.add_cog(osu(bot))
