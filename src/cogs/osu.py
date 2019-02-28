""" osu! -- rufus.py """
import config as c
import os.path
import requests
from discord.ext import commands


class osu(commands.Cog, name="osu!"):
    """ osu! commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def o_user(self, username, mode='osu!'):
        """ Get osu! user information.
            Available modes:
                - osu!
                - taiko
                - ctb
                - mania
        """
        if mode.lower() == 'osu!':
            mode = 0
        elif mode.lower() == 'taiko':
            mode = 1
        elif mode.lower() == 'ctb':
            mode = 2
        elif mode.lower() == 'mania' or mode.lower() == 'osu!mania':
            mode = 3
        URL = 'https://osu.ppy.sh/api/get_user?k={}&m={}&u={}'.format(c.osu_api_key, mode, username)
        DATA = requests.get(URL).json()
        BEST_URL = 'https://osu.ppy.sh/api/get_user_best?k={}&m={}&limit=3&u={}'.format(c.osu_api_key, mode, username)
        BEST_DATA = requests.get(BEST_URL).json()
        try:
            await self.bot.say('```apache\nUsername: {}\nID: {}\nCreated: {}\n300: {}\n100: {}\n50: {}\nPlays: {}\nLevel: {}\nPP: {}\nAccuracy: {}\nSS/SSH: {}/{}\nS/SH: {}/{}\nA: {}\nCountry: {}\n\nTop Scores:\n\t1. {}\n\t2. {}\n\t3. {}```'.format(DATA[0]['username'],DATA[0]['user_id'],DATA[0]['join_date'],DATA[0]['count300'],DATA[0]['count100'],DATA[0]['count50'],DATA[0]['playcount'],DATA[0]['level'],DATA[0]['pp_raw'],DATA[0]['accuracy'],DATA[0]['count_rank_ss'],DATA[0]['count_rank_ssh'],DATA[0]['count_rank_s'],DATA[0]['count_rank_sh'],DATA[0]['count_rank_a'],DATA[0]['country'],BEST_DATA[0]['beatmap_id'],BEST_DATA[1]['beatmap_id'],BEST_DATA[2]['beatmap_id']))
        except:
            await self.bot.say('User with the name or ID of `{}` doesn\'t exist.'.format(username))

    @commands.command(pass_context=True)
    async def skin(self, ctx):
        """ current osu! skin.
            Deprecated because docker.
        """
        if True:
            await self.bot.say('Command temporarily disabled.')
        elif False:
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
