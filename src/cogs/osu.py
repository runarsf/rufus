import config as c
import os.path
import requests
from discord.ext import commands


class OsuCog(commands.Cog, name="osu!"):
    """ OsuCog """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='o_user')
    async def _osu_user(self, ctx, username, mode='osu!'):
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
            await ctx.send(f'```apache\nUsername: {DATA[0]["username"]} \
                \nID: {DATA[0]["user_id"]} \
                \nCreated: {DATA[0]["join_date"]} \
                \n300: {DATA[0]["count300"]} \
                \n100: {DATA[0]["count100"]} \
                \n50: {DATA[0]["count50"]} \
                \nPlays: {DATA[0]["playcount"]} \
                \nLevel: {DATA[0]["level"]} \
                \nPP: {DATA[0]["pp_raw"]} \
                \nAccuracy: {DATA[0]["accuracy"]} \
                \nSS/SSH: {DATA[0]["count_rank_ss"]}/{DATA[0]["count_rank_ssh"]} \
                \nS/SH: {DATA[0]["count_rank_s"]}/{DATA[0]["count_rank_sh"]} \
                \nA: {DATA[0]["count_rank_a"]} \
                \nCountry: {DATA[0]["country"]} \
                \n\nTop Scores: \
                \n\t1. {BEST_DATA[0]["beatmap_id"]} \
                \n\t2. {BEST_DATA[1]["beatmap_id"]} \
                \n\t3. {BEST_DATA[2]["beatmap_id"]} \
                ```')
        except:
            await ctx.send(f'User with the name or ID of `{username}` doesn\'t exist.')

    @commands.command(name='o_skin', hidden=True)
    @commands.is_owner()
    async def _osu_skin(self, ctx):
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
    bot.add_cog(OsuCog(bot))
