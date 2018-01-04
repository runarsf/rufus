import os
import re
import math
import numpy
import urllib
import discord
import aiohttp
import asyncio
import pyoppai
import logging
import operator
import pytesseract
import collections
import numpy as np
import matplotlib as mpl
import random, time, datetime, json
mpl.use('Agg') # for non gui
from PIL import Image
from threading import Thread
from discord.ext import commands
from discord.utils import find
from __main__ import send_cmd_help
from pippy.beatmap import Beatmap
from pymongo import MongoClient
from bs4 import BeautifulSoup
from .utils.dataIO import fileIO
from cogs.utils import checks
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
from matplotlib import ticker
from data.osu.oppai_chunks import oppai
from imgurpython import ImgurClient
from random import randint

prefix = fileIO("data/red/settings.json", "load")['PREFIXES'][0]
help_msg = [
            "**No linked account (`{}osuset user [username]`) or not using **`{}command [username] [gamemode]`".format(prefix, prefix),
            "**No linked account (`{}osuset user [username]`)**".format(prefix)
            ]
modes = ["osu", "taiko", "ctb", "mania"]
modes2 = ["osu", "taiko", "fruits", "mania"]
client = MongoClient()
db = client['owo_database_2']
log = logging.getLogger("red.osu")
log.setLevel(logging.DEBUG)

class Osu:
    """Cog to give osu! stats for all gamemodes."""
    def __init__(self, bot):
        self.bot = bot
        self.api_keys = fileIO("data/osu/apikey.json", "load")
        if 'imgur_auth_info' in self.api_keys.keys():
            client_id = self.api_keys['imgur_auth_info']['client_id']
            client_secret = self.api_keys['imgur_auth_info']['client_secret']
            self.imgur = ImgurClient(client_id, client_secret)
        else:
            self.imgur = None
        self.osu_settings = fileIO("data/osu/osu_settings.json", "load")
        self.num_max_prof = 8
        self.max_map_disp = 3
        self.sleep_time = 0.06

    # ---------------------------- Settings ------------------------------------
    @commands.group(pass_context=True)
    async def osuset(self, ctx):
        """Where you can define some settings"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @osuset.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def tracktop(self, ctx, top_num:int):
        """ Set # of top plays being tracked """
        msg = ""
        if top_num < 1 or top_num > 100:
            msg = "**Please enter a valid number. (1 - 100)**"
        else:
            self.osu_settings["num_track"] = top_num
            msg = "**Maximum tracking set to {} plays.**".format(top_num)
            fileIO("data/osu/osu_settings.json", "save", self.osu_settings)
        await self.bot.say(msg)

    @osuset.command(pass_context=True, no_pm=True, name = 'ccbmp')
    @checks.is_owner()
    async def clear_cache(self):
        db.beatmap_cache.update_one({"type":'list'}, {'$set':{
            'ids': list([])
        }})

        db.beatmap_cache.update_one({"type":'maps'}, {'$set':{
            'maps': list([])
        }})

    @osuset.command(pass_context=True, no_pm=True, name = 'reccount')
    @checks.is_owner()
    async def reccount(self):
        counter = 0
        for pp_maps in db.suggest_osu.find({}, no_cursor_timeout = True):
            counter += len(pp_maps['beatmaps'])

        await self.bot.say('There are currently `{}` maps in the osu! standard recommendation database.'.format(counter))

    @osuset.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def displaytop(self, ctx, top_num:int):
        """ Set # of best plays being displayed in top command """
        msg = ""
        if top_num < 1 or top_num > 10:
            msg = "**Please enter a valid number. (1 - 10)**"
        else:
            self.osu_settings["num_best_plays"] = top_num
            msg = "**Now Displaying Top {} Plays.**".format(top_num)
            fileIO("data/osu/osu_settings.json", "save", self.osu_settings)
        await self.bot.say(msg)

    @osuset.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_messages=True)
    async def tracking(self, ctx, toggle=None):
        """ For disabling tracking on server (enable/disable) """
        server = ctx.message.server

        server_settings = db.osu_settings.find_one({'server_id':server.id})
        if not server_settings:
            db.osu_settings.insert_one({'server_id':server.id})
            server_settings = db.osu_settings.find_one({'server_id':server.id})

        if 'tracking' not in server_settings:
            db.osu_settings.update_one({'server_id':server.id}, {'$set': {
                'tracking': True}})
        server_settings = db.osu_settings.find_one({'server_id':server.id})

        status = ""
        if not toggle:
            track = server_settings['tracking']
            if not track:
                track = True
                status = "Enabled"
            else:
                track = False
                status = "Disabled"
        elif toggle.lower() == "enable":
            track = True
            status = "Enabled"
        elif toggle.lower() == "disable":
            track = False
            status = "Disabled"
        db.osu_settings.update_one({'server_id':server.id}, {'$set': {'tracking': track}})
        await self.bot.say("**Player Tracking {} on {}.**".format(server.name, status))

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def overview(self, ctx):
        """ Get an overview of your settings """
        server = ctx.message.server
        user = ctx.message.author

        em = discord.Embed(description='', colour=user.colour)
        em.set_author(name="Current Settings for {}".format(server.name), icon_url = server.icon_url)

        # determine api to use
        server_settings = db.osu_settings.find_one({'server_id':server.id})
        passive_settings = db.options.find_one({'server_id':server.id})

        if server_settings:
            if "api" not in server_settings:
                api = "Official osu! API"
            elif server_settings["api"] == self.osu_settings["type"]["default"]:
                api = "Official osu! API"
            elif server_settings["api"] == self.osu_settings["type"]["ripple"]:
                api = "Ripple API"
        else:
            api = "Official osu! API"

        # determine
        if not server_settings or "tracking" not in server_settings or server_settings["tracking"] == True:
            tracking = "Enabled"
        else:
            tracking = "Disabled"

        info = "**__General Settings__**\n"
        info += "**Default API:** {}\n".format(api)
        info += "**Top Plays (Global):** {}\n".format(self.osu_settings['num_best_plays'])
        info += "**Tracking:** {}\n".format(tracking)

        if tracking == "Enabled":
            info += "**Tracking Max (Global):** {}\n".format(self.osu_settings['num_track'])
        info += "**Tracking Total (Global):** {} players\n".format(str(db.track.count()))
        cycle_time = self.bot.get_cog('Tracking').cycle_time
        info += "**Tracking Cycle Time:** {:.3f} min\n".format(float(cycle_time))

        if not passive_settings:
            passive_settings = {
                "graph_beatmap": True,
                "graph_screenshot": False,
                "beatmap": True,
                "screenshot": True
            }

        info += "**\n__Passive Options__**\n"
        info += "**Beatmap Url Detection:** {}\n".format(self._is_enabled(passive_settings['beatmap']))
        info += "**Beatmap Graph:** {}\n".format(self._is_enabled(passive_settings['graph_beatmap']))
        info += "**Screenshot Detection:** {}\n".format(self._is_enabled(passive_settings['screenshot']))
        info += "**Screenshot Graph:** {}".format(self._is_enabled(passive_settings['graph_screenshot']))

        em.description = info
        await self.bot.say(embed = em)

    def _is_enabled(self, option):
        if option:
            return 'Enabled'
        else:
            return 'Disabled'

    @osuset.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def api(self, ctx, *, choice):
        """'official' or 'ripple'"""
        server = ctx.message.server
        server_settings = db.osu_settings.find_one({'server_id':server.id})
        if not server_settings or 'api' not in server_settings:
            db.osu_settings.insert_one({'server_id':server.id, 'api':self.osu_settings["type"]["default"]})

        if not choice.lower() == "official" and not choice.lower() == "ripple":
            await self.bot.say("The two choices are `official` and `ripple`")
            return
        elif choice.lower() == "official":
            db.osu_settings.update_one({'server_id':server.id}, {'$set':{"api": self.osu_settings["type"]["default"]}})
        elif choice.lower() == "ripple":
            db.osu_settings.update_one({'server_id':server.id}, {'$set':{"api": self.osu_settings["type"]["ripple"]}})
        await self.bot.say("**Switched to `{}` server as default on `{}`.**".format(choice, server.name))

    @osuset.command(pass_context=True, no_pm=True)
    async def default(self, ctx, mode:str):
        """ Set your default gamemode """
        user = ctx.message.author
        server = ctx.message.server

        try:
            if mode.lower() in modes:
                gamemode = modes.index(mode.lower())
            elif int(mode) >= 0 and int(mode) <= 3:
                gamemode = int(mode)
            else:
                await self.bot.say("**Please enter a valid gamemode.**")
                return
        except:
            await self.bot.say("**Please enter a valid gamemode.**")
            return

        user_set = db.user_settings.find_one({'user_id':user.id})
        if user_set:
            db.user_settings.update_one({'user_id':user.id},
                {'$set':{"default_gamemode": int(gamemode)}})
            await self.bot.say("**`{}`'s default gamemode has been set to `{}`.** :white_check_mark:".format(user.name, modes[gamemode]))
        else:
            await self.bot.say(help_msg[1])

    @osuset.group(name="key", pass_context=True)
    @checks.is_owner()
    async def setkey(self, ctx):
        """Sets your osu and puush api key"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @setkey.command(name="imgur", pass_context=True)
    @checks.is_owner()
    async def setimgur(self, ctx):
        await self.bot.whisper("Type your imgur client ID. You can reply here.")
        client_id = await self.bot.wait_for_message(timeout=30, author=ctx.message.author)
        if client_id is None:
            return
        await self.bot.whisper("Type your client secret.")
        client_secret = await self.bot.wait_for_message(timeout=30, author=ctx.message.author)
        if client_secret is None:
            return
        self.api_keys['imgur_auth_info'] = {}
        self.api_keys['imgur_auth_info']['client_id'] = client_id.content
        self.api_keys['imgur_auth_info']['client_secret'] = client_secret.content
        fileIO("data/osu/apikey.json", "save", self.api_keys)
        self.imgur = ImgurClient(client_id.content, client_secret.content)
        await self.bot.whisper("Imgur API details added. :white_check_mark:")

    @setkey.command(name="osu", pass_context=True)
    @checks.is_owner()
    async def setosu(self, ctx):
        await self.bot.whisper("Type your osu! api key. You can reply here.")
        key = await self.bot.wait_for_message(timeout=30, author=ctx.message.author)
        if key is None:
            return
        else:
            self.api_keys["osu_api_key"] = key.content
            fileIO("data/osu/apikey.json", "save", self.api_keys)
            await self.bot.whisper("osu! API Key details added. :white_check_mark:")

    @commands.command(pass_context=True, no_pm=True)
    async def osu(self, ctx, *username):
        """[p]osu usernames [-ripple|-official]"""
        await self._process_user_info(ctx, username, 0)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(pass_context=True, no_pm=True)
    async def osutop(self, ctx, *username):
        """[p]osutop username [-ripple|-official]"""
        await self._process_user_top(ctx, username, 0)

    @commands.command(pass_context=True, no_pm=True)
    async def taiko(self, ctx, *username):
        """[p]taiko usernames [-ripple|-official]"""
        await self._process_user_info(ctx, username, 1)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(pass_context=True, no_pm=True)
    async def taikotop(self, ctx, *username):
        """[p]taikotop username [-ripple|-official]"""
        await self._process_user_top(ctx, username, 1)

    @commands.command(pass_context=True, no_pm=True)
    async def ctb(self, ctx, *username):
        """[p]ctb usernames [-ripple|-official]"""
        await self._process_user_info(ctx, username, 2)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(pass_context=True, no_pm=True)
    async def ctbtop(self, ctx, *username):
        """[p]ctbtop username [-ripple|-official]"""
        await self._process_user_top(ctx, username, 2)

    @commands.command(pass_context=True, no_pm=True)
    async def mania(self, ctx, *username):
        """[p]mania usernames [-ripple|-official]"""
        await self._process_user_info(ctx, username, 3)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(pass_context=True, no_pm=True)
    async def maniatop(self, ctx, *username):
        """[p]maniatop username [-ripple|-official]"""
        await self._process_user_top(ctx, username, 3)

    @commands.command(pass_context=True, no_pm=True)
    async def recent(self, ctx, *username):
        """[p]recent username [gamemode] [-ripple|-official]"""
        await self._process_user_recent(ctx, username)

    @commands.command(pass_context=True)
    async def scores(self, ctx, map_link, *username):
        """[p]scores map_link [-t] [username]"""
        if not 'https://osu.ppy.sh/b/' in map_link:
            await self.bot.say("There needs to be a proper beatmap link")
            return
        else:
            map_link = map_link.replace('https://osu.ppy.sh/b/', '')
        await self._process_map_score(ctx, map_link, username)

    @commands.command(pass_context = True, name = 'osuleaderboard', aliases = ['ol','osul'])
    async def osuleaderboard(self, ctx, *option):
        """Uses linked database and cached data to generate leaderboard"""
        return
        try:
            mode = modes[mode] # mode
            members = ctx.message.server.members
            userlist = []
            for member in members:
                userinfo = await self._process_username(ctx, member, disp_error = False)
                if not userinfo:
                    continue

                osu_id = userinfo['osu_id']

                # find userinfo
                player = db.osutrack.find_one({'osu_id': osu_id})
                if not player:
                    player = db.user_settings.find({'osu_user_id': osu_id})
                    try:
                        player_info = player['userinfo'][mode]
                        player_info['discord_username'] = userinfo['discord_username']
                    except:
                        pass # has not done >osu command
                else:
                    player_info = player['userinfo'][mode]

                userlist.append(player_info)

            sorted(userlist, key=operator.itemgetter('pp_rank'), reverse=True)
            sorted_list = userlist

            title = "Osu! Leaderboard for {}\n".format(server.name)
            board_type = 'PP'
            footer_text = ""
            icon_url = server.icon_url

            # multiple page support
            page = 1
            per_page = 15
            pages = math.ceil(len(sorted_list)/per_page)
            for option in options:
                if str(option).isdigit():
                    if page >= 1 and int(option) <= pages:
                        page = int(str(option))
                    else:
                        await self.bot.say("**Please enter a valid page number! (1 - {})**".format(str(pages)))
                        return
                    break

            msg = ""
            msg += "**Rank              Name (Page {}/{})**\n".format(page, pages)
            rank = 1 + per_page*(page-1)
            start_index = per_page*page - per_page
            end_index = per_page*page

            default_label = "   "
            special_labels = ["♔", "♕", "♖", "♗", "♘", "♙"]

            for single_user in sorted_list[start_index:end_index]:
                if rank-1 < len(special_labels):
                    label = special_labels[rank-1]
                else:
                    label = default_label

                msg += u'`{:<2}{:<2}{:<2}   # {:<22}'.format(rank, label, u"➤", self._truncate_text(single_user[0],20))
                msg += u'{:>5}{:<2}{:<2}{:<5}`\n'.format(" ", " ", " ", "Total {}: ".format(board_type) + str(single_user[1]))
                rank += 1
            msg +="----------------------------------------------------\n"
            msg += "`{}`".format(footer_text)

            em = discord.Embed(description='', colour=user.colour)
            em.set_author(name=title, icon_url = icon_url)
            em.description = msg

            await self.bot.say(embed = em)
        except:
            pass

    @checks.admin_or_permissions(manage_server=True)
    @commands.group(pass_context=True)
    async def options(self, ctx):
        """Set some server options"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @options.command(pass_context=True, no_pm=True)
    async def beatmapgraph(self, ctx):
        """Toggle beatmap graph"""
        key_name = "graph_beatmap"
        server = ctx.message.server
        option = self._handle_option(key_name, server.id)

        msg = ""
        if option:
            msg = "**Beatmap graph enabled.**"
        else:
            msg = "**Beatmap graph disabled.**"

        await self.bot.say(msg)

    @options.command(pass_context=True, no_pm=True)
    async def ssgraph(self, ctx):
        """Toggle screenshot beatmap graph"""
        key_name = "graph_screenshot"
        server = ctx.message.server
        option = self._handle_option(key_name, server.id)

        msg = ""
        if option:
            msg = "**Screenshot beatmap graph enabled.**"
        else:
            msg = "**Screenshot beatmap graph disabled.**"

        await self.bot.say(msg)

    @options.command(pass_context=True, no_pm=True)
    async def beatmap(self, ctx):
        """Toggle beatmap url detection"""
        key_name = "beatmap"
        server = ctx.message.server
        option = self._handle_option(key_name, server.id)

        msg = ""
        if option:
            msg = "**Beatmap url detection enabled.**"
        else:
            msg = "**Beatmap url detection disabled.**"

        await self.bot.say(msg)

    @options.command(pass_context=True, no_pm=True)
    async def screenshot(self, ctx):
        """Toggle screenshot detection"""
        key_name = "screenshot"
        server = ctx.message.server
        option = self._handle_option(key_name, server.id)

        msg = ""
        if option:
            msg = "**Screenshot detection enabled.**"
        else:
            msg = "**Screenshot detection disabled.**"

        await self.bot.say(msg)

    def _handle_option(self, key_name, server_id):
        server_options = db.options.find_one({"server_id":server_id})
        if server_options is None:
            server_options = {
                "server_id": server_id,
                "graph_beatmap": True,
                "graph_screenshot": False,
                "beatmap": True,
                "screenshot": True
            }
            server_options[key_name] = not server_options[key_name]
            db.options.insert_one(server_options)
        else:
            server_options[key_name] = not server_options[key_name]
            db.options.update_one({"server_id":server_id}, {
                '$set':{key_name: server_options[key_name]
                }})

        return server_options[key_name]

    @osuset.command(pass_context=True, no_pm=True)
    async def user(self, ctx, *, username):
        """Sets user information given an osu! username"""
        user = ctx.message.author
        channel = ctx.message.channel
        server = user.server
        key = self.api_keys["osu_api_key"]

        if not self._check_user_exists(user):
            try:
                osu_user = list(await get_user(key, self.osu_settings["type"]["default"], username, 1))
                newuser = {
                    "discord_username": user.name,
                    "osu_username": username,
                    "osu_user_id": osu_user[0]["user_id"],
                    "default_gamemode": 0,
                    "ripple_username": "",
                    "ripple_user_id": "",
                    "user_id": user.id
                }
                db.user_settings.insert_one(newuser)
                await self.bot.say("{}, your account has been linked to osu! username `{}`".format(user.mention, osu_user[0]["username"]))
            except:
                await self.bot.say("`{}` doesn't exist in the osu! database.".format(username))
        else:
            try:
                osu_user = list(await get_user(key, self.osu_settings["type"]["default"], username, 1))
                db.user_settings.update_one({'user_id': user.id}, {'$set':{'osu_username':username,
                    "osu_user_id":osu_user[0]["user_id"]
                    }})

                stevy_info = db.user_settings.find_one({'user_id':user.id})
                await self.bot.say("{}, your osu! username has been edited to `{}`".format(user.mention, osu_user[0]["username"]))
            except:
                await self.bot.say("`{}` doesn't exist in the osu! database.".format(username))

    @osuset.command(name = "skin", pass_context=True, no_pm=True)
    async def setskin(self, ctx, link:str):
        """Link your skin."""
        user = ctx.message.author
        user_set = db.user_settings.find_one({'user_id':user.id})
        if user_set != None:

            """ # Later
            if link == '-find':
                url = self._find_skin(user_set['osu_user_id'])
            elif self._is_valid_skin(link):
                url = link
            else:
                return"""

            db.user_settings.update_one({'user_id':user.id},
                {'$set':{"skin": link}})
            await self.bot.say("**`{}`'s skin has been set to `{}`.**".format(user.name, link))
        else:
            await self.bot.say(help_msg[1])

    @commands.command(pass_context=True, no_pm=True)
    async def skin(self, ctx, user:discord.Member = None):
        """[p]skin username"""
        if user == None:
            user = ctx.message.author

        userinfo = db.user_settings.find_one({'user_id':user.id})

        if userinfo != None:
            if 'skin' in userinfo:
                await self.bot.say("**`{}`'s Skin: <{}>.**".format(user.name, userinfo['skin']))
            else:
                await self.bot.say("**`{}` has not set a skin.**".format(user.name))
        else:
            await self.bot.say("**`{}` does not have an account linked.**".format(user.name))

    # Gets json information to proccess the small version of the image
    async def _process_user_info(self, ctx, usernames, gamemode:int):
        key = self.api_keys["osu_api_key"]
        channel = ctx.message.channel
        user = ctx.message.author
        server = user.server

        # checks for detailed flag
        if '-d' in usernames:
            detailed = True
            usernames = list(usernames)
            del usernames[usernames.index('-d')]
            usernames = tuple(usernames)
        else:
            detailed = False

        if not usernames:
            usernames = [None]
        # get rid of duplicates initially
        usernames = list(set(usernames))

        # determine api to use
        usernames, api = self._determine_api(server, usernames)

        # gives the final input for osu username
        final_usernames = []
        for username in usernames:
            test_username = await self._process_username(ctx, username)
            if test_username != None:
                final_usernames.append(test_username)

        # get rid of duplicates initially
        final_usernames = list(set(final_usernames))

        # testing if username is osu username
        all_user_info = []
        sequence = []

        count_valid = 0
        for i in range(len(final_usernames)):
            #try:
            userinfo = list(await get_user(key, api, final_usernames[i], gamemode, no_cache = True)) # get user info from osu api
            # self._update_linked_user(userinfo)
            if userinfo != None and len(userinfo) > 0 and userinfo[0]['pp_raw'] != None:
                all_user_info.append(userinfo[0])
                sequence.append((count_valid, int(userinfo[0]["pp_rank"])))
                count_valid = count_valid + 1
            else:
                await self.bot.say("**`{}` has not played enough.**".format(final_usernames[i]))
            #except:
                #await self.bot.say("Error. Please try again later.")
                #return

        sequence = sorted(sequence, key=operator.itemgetter(1))

        all_players = []
        for i, pp in sequence:
            if detailed:
                all_players.append(await self._det_user_info(api, server, user, all_user_info[i], gamemode))
            else:
                all_players.append(await self._get_user_info(api, server, user, all_user_info[i], gamemode))
        disp_num = min(self.num_max_prof, len(all_players))
        if disp_num < len(all_players):
            await self.bot.say("Found {} users, but displaying top {}.".format(len(all_players), disp_num))

        for player in all_players[0:disp_num]:
            await self.bot.say(embed=player)

    def _update_linked_user(self, userinfo):
        pass

    # takes iterable of inputs and determines api, also based on defaults
    def _determine_api(self, server, inputs):

        if not inputs or ('-ripple' not in inputs and '-official' not in inputs): # in case not specified
            server_settings = db.osu_settings.find_one({'server_id':server.id})
            if server_settings and "api" in server_settings:
                if server_settings["api"] == self.osu_settings["type"]["default"]:
                    api = self.osu_settings["type"]["default"]
                elif server_settings["api"] == self.osu_settings["type"]["ripple"]:
                    api = self.osu_settings["type"]["ripple"]
            else:
                api = self.osu_settings["type"]["default"]
        if '-ripple' in inputs:
            inputs = list(inputs)
            inputs.remove('-ripple')
            api = self.osu_settings["type"]["ripple"]
        if '-official' in inputs:
            inputs = list(inputs)
            inputs.remove('-official')
            api = self.osu_settings["type"]["default"]

        if not inputs:
            inputs = [None]

        return inputs, api

    # Gets the user's most recent score
    async def _process_user_recent(self, ctx, inputs):
        key = self.api_keys["osu_api_key"]
        channel = ctx.message.channel
        user = ctx.message.author
        server = user.server

        # forced handle gamemode
        gamemode = -1
        inputs = list(inputs)
        for mode in modes:
            if len(inputs) >= 2 and mode in inputs:
                gamemode = get_gamemode_number(mode)
                inputs.remove(mode)
            elif len(inputs) == 1 and mode == inputs[0]:
                gamemode = get_gamemode_number(mode)
                inputs.remove(mode)

        recent_best = False
        if '-b' in inputs:
            recent_best = True
            inputs.remove('-b')

        inputs = tuple(inputs)

        # handle api and username (1)
        username, api = self._determine_api(server, list(inputs))
        username = username[0]

        # gives the final input for osu username
        test_username = await self._process_username(ctx, username)
        if test_username:
            username = test_username
        else:
            return

        # determines which recent gamemode to display based on user
        if gamemode == -1:
            target_id = self._get_discord_id(username, api)
            if target_id != -1:
                user_setting = db.user_settings.find_one({'user_id':target_id})
                gamemode = user_setting['default_gamemode']
            elif target_id == -1 and self._check_user_exists(user):
                user_setting = db.user_settings.find_one({'user_id':user.id})
                gamemode = user_setting['default_gamemode']
            else:
                gamemode = 0

        try:
            userinfo = list(await get_user(key, api, username, gamemode))
            await asyncio.sleep(self.sleep_time)
            if recent_best:
                userbest = list(await get_user_best(key, api, username, gamemode, 100))
                web = False
            else:
                userrecent = list(await get_user_recent(key, api, username, gamemode))
        except:
            await self.bot.say("Error. Please try again later.")
            return
        await asyncio.sleep(self.sleep_time)

        if not userinfo:
            await self.bot.say("**`{}` was not found or no recent plays in `{}`.**".format(username, get_gamemode(gamemode)))
            return

        try:
            userinfo = userinfo[0]
            if recent_best:
                # save keep index
                for i, score in enumerate(userbest):
                    userbest[i]['index'] = i
                userbest = sorted(userbest, key=operator.itemgetter('date'), reverse=True)
                userbest = [userbest[0]]

                # get best plays map information and scores, assume length is self.osu_settings['num_best_plays']
                best_beatmaps = []
                best_acc = []

                beatmap = list(await get_beatmap(key, api, beatmap_id=userbest[0]['beatmap_id']))[0]
                best_beatmaps = [beatmap]
                best_acc = [calculate_acc(userbest[0], gamemode)]
                score_num = userbest[0]['index']

                msg, embed = await self._get_user_top(
                    ctx, api, userinfo, userbest, best_beatmaps, best_acc, gamemode, score_num = score_num, web = web)
            else:
                userrecent = userrecent[0]
                msg, embed = await self._get_recent(ctx, api, userinfo, userrecent, gamemode)
        except:
            await self.bot.say("**`{}` was not found or no recent plays in `{}`.**".format(username, get_gamemode(gamemode)))
            return

        await self.bot.say(msg, embed=embed)

    def _get_discord_id(self, username:str, api:str):
        #if api == self.osu_settings["type"]["ripple"]:
            #name_type = "ripple_username"
        #else:
            #name_type = "osu_username"
        # currently assumes same name
        name_type = "osu_username"
        user = db.user_settings.find_one({name_type:username})
        if user:
            return user['user_id']
        return -1

    # Gets information to proccess the top play version of the image
    async def _process_user_top(self, ctx, username, gamemode: int):
        key = self.api_keys["osu_api_key"]
        channel = ctx.message.channel
        user = ctx.message.author
        server = user.server

        # Written by Jams
        score_num = None
        show_recent = False
        greater_than = None
        if '-p' in username:
            if '-r' in username or '-g' in username:
                await self.bot.say("**You cannot use -r, -g, or -p at the same time**")
                return
            marker_loc = username.index('-p')
            if len(username) - 1 == marker_loc:
                await self.bot.say("**Please provide a score number!**")
                return

            username = tuple(username)
            score_num = username[marker_loc + 1]
            if not score_num.isdigit():
                await self.bot.say("**Please use only whole numbers for number of top plays!**")
                return
            else:
                score_num = int(score_num)

            if score_num <= 0 or score_num > 100:
                await self.bot.say("**Please enter a valid top play number! (1-100)**")
                return

            username = list(username)
            del username[marker_loc + 1]
            del username[marker_loc]
        elif '-r' in username:
            if '-g' in username:
                await self.bot.say("**You cannot use -r, -g, or -p at the same time**")
                return
            username = list(username)
            del username[username.index('-r')]
            show_recent = True
        elif '-g' in username:
            username = list(username)
            marker_loc = username.index('-g')
            greater_than = username[marker_loc + 1]
            if not greater_than.replace('.', '').isdigit():
                await self.bot.say("**Please use only numbers for amount of PP!**")
                return
            else:
                greater_than = float(greater_than)
            del username[marker_loc + 1]
            del username[marker_loc]

        # if you're not getting the score number, then only use the first one
        if not username:
            usernames = [None]
        elif not score_num and username:
            usernames = [username[0]]
        else:
            usernames = list(username)

        # determine api to use
        usernames, api = self._determine_api(server, usernames)

        embed_list = [] # final list to display
        for username in usernames:

            # gives the final input for osu username
            username = await self._process_username(ctx, username)

            # get info, get from website if api is official
            userinfo = list(await get_user(key, api, username, gamemode))
            #if api == self.osu_settings["type"]["default"]: # returns the same format
                #userbest, best_beatmaps, best_acc = await self._get_user_best_web(ctx, userinfo[0], gamemode, num_plays = 100)
                #is_web = True
            #else:
            userbest = list(await get_user_best(key, api, username, gamemode, 100))
            best_beatmaps, best_acc = None, None
            is_web = False

            if not userinfo or not userbest:
                await self.bot.say("**`{}` was not found or not enough plays.**".format(username))
                return

            # save keep index
            for i, score in enumerate(userbest):
                userbest[i]['index'] = i

            # handle options and process userbest
            if show_recent:
                userbest = sorted(userbest, key=operator.itemgetter('date'), reverse=True)
                userbest = userbest[:self.osu_settings['num_best_plays']]
            elif greater_than:
                # count how many are above.
                counter = 0
                for score in userbest:
                    if float(score['pp']) >= greater_than:
                        counter += 1
                await self.bot.say("**`{}` has {} plays worth more than {}PP**".format(username, str(counter), greater_than))
                return
            elif score_num:
                # grab only that one.
                index = score_num - 1
                userbest = [userbest[index]]
            else:
                userbest = userbest[:self.osu_settings['num_best_plays']]

            # process best_beatmaps and best_acc arrays, assume in order
            if not best_beatmaps and not best_acc:
                # get best plays map information and scores, assume length is self.osu_settings['num_best_plays']
                best_beatmaps = []
                best_acc = []
                for i in range(len(userbest)):
                    beatmap = list(await get_beatmap(key, api, beatmap_id=userbest[i]['beatmap_id']))[0]
                    best_beatmaps.append(beatmap)
                    best_acc.append(calculate_acc(userbest[i], gamemode))
                    await asyncio.sleep(self.sleep_time)
            else:
                temp_best_maps = []
                temp_best_acc = []
                if score_num:
                    index = score_num - 1
                    best_beatmaps, best_acc = [best_beatmaps[index]], [best_acc[index]]
                else:
                    for play in userbest:
                        temp_best_maps.append(best_beatmaps[int(play['index'])])
                        temp_best_acc.append(best_acc[int(play['index'])])
                    best_beatmaps = temp_best_maps
                    best_acc = temp_best_acc

            # get top
            msg, embed = await self._get_user_top(
                ctx, api, userinfo[0], userbest, best_beatmaps, best_acc, gamemode, score_num = score_num, recent = show_recent, web = is_web)
            embed_list.append((msg, embed))

        # print out all the necessary embeds
        for msg, embed in embed_list:
            await self.bot.say(msg, embed = embed)

    # Gives a user profile image with some information
    async def _get_user_top(self, ctx, api, user, userbest, best_beatmaps, best_acc, gamemode, score_num = None, recent = False, web = False):
        server_user = ctx.message.author
        server = ctx.message.server
        key = self.api_keys["osu_api_key"]

        if api == self.osu_settings["type"]["default"]:
            profile_url ='https://a.ppy.sh/{}'.format(user['user_id'])
        elif api == self.osu_settings["type"]["ripple"]:
            profile_url = 'http://a.ripple.moe/{}.png'.format(user['user_id'])

        flag_url = 'https://osu.ppy.sh/images/flags/{}.png'.format(user['country'])
        gamemode_text = get_gamemode(gamemode)

        msg = ''
        desc = ''

        # takes in the processed userbest
        for i in range(len(userbest)):
            mods = num_to_mod(userbest[i]['enabled_mods'])
            oppai_info = await get_pyoppai(best_beatmaps[i]['beatmap_id'], accs = [float(best_acc[i])], mods = int(userbest[i]['enabled_mods']))

            # missing information
            best_beatmaps[i]['max_combo'] = oppai_info['max_combo']

            if not mods:
                mods = []
                mods.append('No Mod')
            beatmap_url = 'https://osu.ppy.sh/b/{}'.format(best_beatmaps[i]['beatmap_id'])

            info = ''
            if not score_num:
                number = '{}. '.format(str(int(userbest[i]['index']) + 1))
            else:
                number = ''

            star_str, _ = compare_val(best_beatmaps[i]['difficultyrating'], oppai_info, param = 'stars', dec_places = 2, single = True)
            info += '**{}[{} [{}]]({}) +{}** [{}★]\n'.format(
                number, best_beatmaps[i]['title'],
                best_beatmaps[i]['version'], beatmap_url,
                fix_mods(''.join(mods)), star_str)

            # choke text
            choke_text = ''
            if (oppai_info != None and userbest[i]['countmiss'] != None and best_beatmaps[i]['max_combo']!= None) and (int(userbest[i]['countmiss'])>=1 or (int(userbest[i]['maxcombo']) <= 0.95*int(best_beatmaps[i]['max_combo']) and 'S' in userbest[i]['rank'])):
                choke_text += ' _({:.2f}pp for FC)_'.format(oppai_info['pp'][0])
            info += '▸ **{} Rank** ▸ **{:.2f}pp**{} ▸ {:.2f}%\n'.format(userbest[i]['rank'], float(userbest[i]['pp']), choke_text, float(best_acc[i]))
            info += '▸ {} ▸ x{}/{} ▸ [{}/{}/{}/{}]\n'.format(
                userbest[i]['score'],
                userbest[i]['maxcombo'], best_beatmaps[i]['max_combo'],
                userbest[i]['count300'],userbest[i]['count100'],userbest[i]['count50'],userbest[i]['countmiss']
                )

            if web:
                timeago = time_ago(datetime.datetime.utcnow() + datetime.timedelta(hours=8), datetime.datetime.strptime(userbest[i]['date'], '%Y-%m-%dT%H:%M:%S+00:00'))
            else:
                timeago = time_ago(datetime.datetime.utcnow() + datetime.timedelta(hours=8), datetime.datetime.strptime(userbest[i]['date'], '%Y-%m-%d %H:%M:%S'))
            info += '▸ Score Set {}Ago\n'.format(timeago)
            desc += info

        em = discord.Embed(description=desc, colour=server_user.colour)
        if recent:
            title = "Most Recent {} Top Play for {}".format(gamemode_text, user['username'])
        elif score_num:
            title = "Top {} {} Play for {}".format(str(score_num), gamemode_text, user['username'])
        else:
            title = "Top {} {} Plays for {}".format(self.osu_settings['num_best_plays'], gamemode_text, user['username'])

        em.set_author(name = title, url="https://osu.ppy.sh/u/{}".format(user['user_id']), icon_url=flag_url)
        em.set_footer(text = "On osu! {} Server".format(self._get_api_name(api)))
        em.set_thumbnail(url=profile_url)

        return (msg, em)

    # Written by Jams
    async def _process_map_score(self, ctx, map_id, inputs):
        key = self.api_keys["osu_api_key"]
        channel = ctx.message.channel
        user = ctx.message.author
        server = user.server

        # determine api to use
        _, api = self._determine_api(server, list(inputs))

        # do this now to allow getting the gamemode from the map itself if not specified
        beatmap = list(await get_beatmap(key, api, beatmap_id=map_id))[0]

        if '-g' in inputs:
            marker_loc = inputs.index('-g')
            gamemode = inputs[marker_loc + 1]
            if gamemode.isdigit() and (int(gamemode) >= 0 and int(gamemode) <= 3):
                inputs = list(inputs)
                del inputs[marker_loc + 1]
                del inputs[marker_loc]
                inputs = tuple(inputs)
                gamemode = int(gamemode)
            else:
                await self.bot.say("**Please input a valid gamemode number.**")
                return
        else:
            gamemode = int(beatmap['mode'])

        username, _ = self._determine_api(server, list(inputs))
        username = username[0]
        # gives the final input for osu username
        username = await self._process_username(ctx, username)

        # for getting user scores
        userinfo = list(await get_user(key, api, username, gamemode))
        userscores = list(await get_scores(
            key, api, map_id, userinfo[0]['user_id'], gamemode))
        if userinfo and userscores:
            msg, top_plays = await self._get_user_scores(ctx, api, map_id, userinfo[0], userscores, gamemode, beatmap)
            await self.bot.say(msg, embed=top_plays)
        else:
            await self.bot.say("**`{}` was not found or no scores on the map.**".format(username))

    ## processes username. probably the worst chunck of code in this project so far. will fix/clean later
    async def _process_username(self, ctx, username, disp_error = True, check_api = True):
        channel = ctx.message.channel
        user = ctx.message.author
        server = user.server
        key = self.api_keys["osu_api_key"]

        # if nothing is given, must rely on if there's account
        if not username:
            if self._check_user_exists(user):
                find_user = db.user_settings.find_one({"user_id":user.id})
                username = find_user["osu_username"]
            else:
                if disp_error:
                    await self.bot.say("It doesn't seem that you have an account linked. Do `{}osuset user [username]`.".format(prefix))
                return None # bad practice, but too lazy to make it nice
        # if it's a discord user, first check to see if they are in database and choose that username
        # then see if the discord username is a osu username, then try the string itself
        elif find(lambda m: m.name == username, channel.server.members) is not None:
            target = find(lambda m: m.name == username, channel.server.members)
            try:
                find_user = db.user_settings.find_one({"user_id":target.id})
                username = find_user["osu_username"]
            except:
                if check_api and await get_user(key, self.osu_settings["type"]["default"], username, 0):
                    username = str(target)
                else:
                    await self.bot.say(help_msg[1])
                    return None
        # @ implies its a discord user (if not, it will just say user not found in the next section)
        # if not found, then oh well.
        elif "@" in username:
            user_id = re.findall("\d+", username)
            if user_id:
                user_id = user_id[0]
                find_user = db.user_settings.find_one({"user_id":user_id})
                if find_user:
                    username = find_user["osu_username"]
                else:
                    await self.bot.say(help_msg[1])
                    return None
            else:
                await self.bot.say(help_msg[1])
                return None
        else:
            username = str(username)
        return username

    # Checks if user exists
    def _check_user_exists(self, user):
        find_user = db.user_settings.find_one({"user_id":user.id})
        if not find_user:
            return False
        return True

    def _get_api_name(self, url:str):
        if url == self.osu_settings["type"]["ripple"]:
            return "Ripple"
        else:
            return "Official"

    # Gives a small user profile
    async def _get_user_info(self, api:str, server, server_user, user, gamemode: int):
        if api == self.osu_settings["type"]["default"]:
            profile_url ='https://a.ppy.sh/{}'.format(user['user_id'])
            pp_country_rank = " ({}#{})".format(user['country'], user['pp_country_rank'])
        elif api == self.osu_settings["type"]["ripple"]:
            profile_url = 'http://a.ripple.moe/{}.png'.format(user['user_id'])
            pp_country_rank = ""

        flag_url = 'https://osu.ppy.sh/images/flags/{}.png'.format(user['country'])

        gamemode_text = get_gamemode(gamemode)

        #try:
        user_url = 'https://{}/u/{}'.format(api, user['user_id'])
        em = discord.Embed(description='', colour=server_user.colour)
        em.set_author(name="{} Profile for {}".format(gamemode_text, user['username']), icon_url = flag_url, url = user_url)
        em.set_thumbnail(url=profile_url)
        level_int = int(float(user['level']))
        level_percent = float(user['level']) - level_int

        info = ""
        info += "**▸ {} Rank:** #{} {}\n".format(self._get_api_name(api), user['pp_rank'], pp_country_rank)
        info += "**▸ Level:** {} ({:.2f}%)\n".format(level_int, level_percent*100)
        info += "**▸ Total PP:** {}\n".format(user['pp_raw'])
        info += "**▸ Hit Accuracy:** {}%\n".format(user['accuracy'][0:5])
        info += "**▸ Playcount:** {}".format(user['playcount'])
        em.description = info

        if api == self.osu_settings["type"]["default"]:
            time_url = "https://osu.ppy.sh/u/{}".format(user['user_id'])
            soup = await get_web(time_url)
            timestamps = []
            for tag in soup.findAll(attrs={'class': 'timeago'}):
                timestamps.append(datetime.datetime.strptime(tag.contents[0].strip().replace(" UTC", ""), '%Y-%m-%d %H:%M:%S'))
            if user['username'] == 'peppy':
                timeago = time_ago(datetime.datetime.now(), timestamps[0])
            else:
                timeago = time_ago(datetime.datetime.now(), timestamps[1])
            timeago = "Last Logged in {} ago".format(timeago)
            em.set_footer(text=timeago)
        else:
            em.set_footer(text = "On osu! {} Server".format(self._get_api_name(api)))

        return em
        #except:
            #return None

    # Gives a detailed user profile
    async def _det_user_info(self, api:str, server, server_user, user, gamemode: int):
        key = self.api_keys["osu_api_key"]
        if api == self.osu_settings["type"]["default"]:
            profile_url ='https://a.ppy.sh/{}'.format(user['user_id'])
            pp_country_rank = " ({}#{})".format(user['country'], user['pp_country_rank'])
        elif api == self.osu_settings["type"]["ripple"]:
            profile_url = 'http://a.ripple.moe/{}.png'.format(user['user_id'])
            pp_country_rank = ""

        flag_url = 'https://osu.ppy.sh/images/flags/{}.png'.format(user['country'])

        gamemode_text = get_gamemode(gamemode)

        #try:
        user_url = 'https://{}/u/{}'.format(api, user['user_id'])
        em = discord.Embed(description='', colour=server_user.colour)
        em.set_author(name="{} Profile for {}".format(gamemode_text, user['username']), icon_url = flag_url, url = user_url)
        em.set_thumbnail(url=profile_url)
        topscores = list(await get_user_best(key, api, user['username'], gamemode, 100))
        modstats = await self._process_mod_stats(topscores, user)
        level_int = int(float(user['level']))
        level_percent = float(user['level']) - level_int
        totalhits = int(user['count50']) + int(user['count100']) + int(user['count300'])
        if totalhits == 0:
            totalhits = 1
        totalranks = int(user['count_rank_ss']) + int(user['count_rank_s']) + int(user['count_rank_a'])
        if totalranks == 0:
            totalranks = 1

        info = ""
        info += "**▸ {} Rank:** #{} {}\n".format(self._get_api_name(api), user['pp_rank'], pp_country_rank)
        info += "**▸ Level:** {} ({:.2f}%)\n".format(level_int, level_percent*100)
        info += "**▸ Total PP:** {:,} ({:,.2f} Per Play)\n".format(float(user['pp_raw']), float(user['pp_raw']) / int(user['playcount']))
        info += "**▸ Hit Accuracy:** {}%\n".format(user['accuracy'][0:5])
        info += "**▸ Playcount:** {:,}\n".format(int(user['playcount']))
        info += "**▸ Total Hits:** {:,} ({:,.2f} Per Play)\n".format(
            totalhits, totalhits / int(user['playcount']))
        info += "**▸ Ranked Score:** {:,} ({:,.2f} Per Play)\n".format(
            int(user['ranked_score']), int(user['ranked_score']) / int(user['playcount']))
        info += "**▸ Total Score: ** {:,} ({:,.2f} Per Play)\n".format(
            int(user['total_score']), int(user['total_score']) / int(user['playcount']))
        info += "**▸ 300:** {:,} *({:.2f}%)* **○ 100:** {:,} *({:.2f}%)* **○ 50:** {:,} *({:.2f}%)*\n".format(
            int(user['count300']), (int(user['count300']) / totalhits) * 100,
            int(user['count100']), (int(user['count100']) / totalhits) * 100,
            int(user['count50']), (int(user['count50']) / totalhits) * 100)
        info += "**▸ SS:** {:,} *({:.2f}%)* **○ S:** {:,} *({:.2f}%)* **○ A:** {:,} *({:.2f}%)*\n".format(
            int(user['count_rank_ss']), (int(user['count_rank_ss']) / totalranks) * 100,
            int(user['count_rank_s']), (int(user['count_rank_s']) / totalranks) * 100,
            int(user['count_rank_a']), (int(user['count_rank_a']) / totalranks) * 100)

        if api == self.osu_settings["type"]["default"]:
            time_url = "https://osu.ppy.sh/u/{}".format(user['user_id'])
            soup = await get_web(time_url)
            timestamps = []
            for tag in soup.findAll(attrs={'class': 'timeago'}):
                timestamps.append(datetime.datetime.strptime(tag.contents[0].strip().replace(" UTC", ""), '%Y-%m-%d %H:%M:%S'))
            if user['username'] == 'peppy':
                logged = time_ago(datetime.datetime.now(), timestamps[0])
                info += "**▸ Joined Osu! in the beginning.**\n"
                info += "**▸ Last Logged in {}**".format(logged)
            else:
                joined = time_ago(datetime.datetime.now(), timestamps[0])
                logged = time_ago(datetime.datetime.now(), timestamps[1])
                info += "**▸ Joined Osu! {}**\n".format(joined)
                info += "**▸ Last Logged in {}**".format(logged)
        em.description = info
        em.add_field(name='Favourite Mods:', value='{}'.format(modstats[0]))
        em.add_field(name='PP Sources:', value='{}'.format(modstats[1]))
        em.add_field(name='PP Range:', value='{:,} - {:,} = {:,}'.format(
            float(topscores[0]['pp']), float(topscores[len(topscores) - 1]['pp']),
            round(float(topscores[0]['pp']) - float(topscores[len(topscores) - 1]['pp']), 2)))
        if self._get_api_name(api) == "Official":
            em.set_footer(text = "On osu! {} Server".format(self._get_api_name(api)))
        else:
            em.set_footer(text = "On osu! {} Server (Servers other than Official are glitched with -d)".format(self._get_api_name(api)))
        return em
        #except:
            #return None

    # Written by Jams
    async def _process_mod_stats(self, scores, user):
        moddic = {"weighted": {}, "unweighted": {}}
        totals = {"weighted":0, "unweighted":0}
        for i, score in enumerate(scores):
            mod = fix_mods(''.join(num_to_mod(score['enabled_mods'])))
            if mod == '':
                mod = "No Mod"
            weight = float(score['pp']) * (0.95 ** i)
            unweighted = float(score['pp'])
            if not mod in moddic['weighted']:
                moddic['weighted'][mod] = weight
                moddic['unweighted'][mod] = unweighted
                totals['weighted'] += weight
                totals['unweighted'] += unweighted
            else:
                moddic['weighted'][mod] += weight
                moddic['unweighted'][mod] += unweighted
                totals['weighted'] += weight
                totals['unweighted'] += unweighted
        mods_weighted = sorted(list(moddic['weighted'].items()), key=operator.itemgetter(1), reverse=True)
        mods_unweighted = sorted(list(moddic['unweighted'].items()), key=operator.itemgetter(1), reverse=True)
        favourites = ''
        for mod in mods_unweighted:
            favourites += "**{}**: {:.2f}% ".format(mod[0], (moddic['unweighted'][mod[0]] / totals['unweighted']) * 100)
        sources = ''
        for mod in mods_weighted:
            sources += "**{}**: {:.2f}PP ".format(mod[0], mod[1])
        return [favourites, sources]

    async def _get_recent(self, ctx, api, user, userrecent, gamemode:int):
        server_user = ctx.message.author
        server = ctx.message.server
        key = self.api_keys["osu_api_key"]

        if api == self.osu_settings["type"]["default"]:
            profile_url ='https://a.ppy.sh/{}'.format(user['user_id'])
        elif api == self.osu_settings["type"]["ripple"]:
            profile_url = 'http://a.ripple.moe/{}.png'.format(user['user_id'])

        flag_url = 'https://osu.ppy.sh/images/flags/{}.png'.format(user['country'])

        # get best plays map information and scores
        beatmap = list(await get_beatmap(key, api, beatmap_id=userrecent['beatmap_id']))[0]
        if not userrecent:
            return ("**No recent score for `{}` in user's default gamemode (`{}`)**".format(user['username'], get_gamemode(gamemode)), None)
        acc = calculate_acc(userrecent, gamemode)
        fc_acc = no_choke_acc(userrecent, gamemode)
        mods = num_to_mod(userrecent['enabled_mods'])

        # determine mods
        if not mods:
            mods = []
            mods.append('No Mod')
        else:
            oppai_mods = "+{}".format("".join(mods))

        beatmap_url = 'https://osu.ppy.sh/b/{}'.format(beatmap['beatmap_id'])

        msg = "**Most Recent {} Play for {}:**".format(get_gamemode(gamemode), user['username'])
        info = ""

        # calculate potential pp
        pot_pp = ''
        if userrecent['rank'] == 'F':
            totalhits = (int(userrecent['count50']) + int(userrecent['count100']) + int(userrecent['count300']) + int(userrecent['countmiss']))
            oppai_output = await get_pyoppai(userrecent['beatmap_id'], accs=[float(acc)], mods = int(userrecent['enabled_mods']), completion=totalhits)
            if oppai_output != None:
                pot_pp = '**No PP** ({:.2f}PP for {:.2f}% FC)'.format(oppai_output['pp'][0], fc_acc)
        else:
            oppai_output = await get_pyoppai(userrecent['beatmap_id'], combo=int(userrecent['maxcombo']), accs=[float(acc)], fc=fc_acc, mods = int(userrecent['enabled_mods']), misses=int(userrecent['countmiss']))
            if oppai_output != None:
                if oppai_output['pp'][0] != oppai_output['pp'][1]:
                    pot_pp = '**{:.2f}PP** ({:.2f}PP for {:.2f}% FC)'.format(oppai_output['pp'][0], oppai_output['pp'][1], fc_acc)
                else:
                    pot_pp = '**{:.2f}PP**'.format(oppai_output['pp'][0])

        info += "▸ **{} Rank** ▸ {} ▸ {}%\n".format(userrecent['rank'], pot_pp, round(acc,2))
        info += "▸ {} ▸ x{}/{} ▸ [{}/{}/{}/{}]\n".format(
            userrecent['score'],
            userrecent['maxcombo'], beatmap['max_combo'],
            userrecent['count300'], userrecent['count100'], userrecent['count50'], userrecent['countmiss'])
        if userrecent['rank'] == 'F':
            try:
                info += "▸ **Map Completion:** {:.2f}%".format(oppai_output['map_completion'])
            except:
                pass

        # get stars
        star_str, _ = compare_val(beatmap['difficultyrating'], oppai_output, 'stars', dec_places = 2, single = True)

        # grab beatmap image
        soup = await get_web(beatmap_url)
        map_image = [x['src'] for x in soup.findAll('img', {'class': 'bmt'})] # just in case yaknow
        map_image_url = 'http:{}'.format(map_image[0]).replace(" ","%")

        em = discord.Embed(description=info, colour=server_user.colour)
        em.set_author(name="{} [{}] +{} [{}★]".format(beatmap['title'], beatmap['version'],
            fix_mods(''.join(mods)),star_str), url = beatmap_url, icon_url = profile_url)
        em.set_thumbnail(url=map_image_url)
        timeago = time_ago(datetime.datetime.utcnow() + datetime.timedelta(hours=8), datetime.datetime.strptime(userrecent['date'], '%Y-%m-%d %H:%M:%S'))
        em.set_footer(text = "{}Ago On osu! {} Server".format(timeago, self._get_api_name(api)))
        return (msg, em)

    # to take load off of the api/faster osutop
    async def _get_user_best_web(self, ctx, user, gamemode:int, num_plays = None):
        if not num_plays:
            num_plays = self.osu_settings['num_best_plays']

        user_id = user['user_id']
        url = "https://osu.ppy.sh/u/{}".format(user['user_id'])
        mode = modes[gamemode]
        if gamemode == 2:
            mode = "fruits"

        url = 'https://osu.ppy.sh/users/{}'.format(user_id)
        soup = await get_web(url, parser = "lxml")
        script = soup.find('script',{"id": "json-user"})
        user = json.loads(script.get_text())

        top_plays = user['allScoresBest'][mode]
        play_list = []
        map_list = []
        acc_list = []

        for play in top_plays[:num_plays]:
            play_info = {}
            map_info = {}

            map_info['title'] = play['beatmapset']['title']
            map_info['beatmap_id'] = play['beatmap']['id']
            map_info['difficultyrating'] = play['beatmap']['difficulty_rating']
            map_info['version'] = play['beatmap']['version']
            map_info['max_combo'] = None # website doesn't give this information :C
            map_list.append(map_info)

            play_info['beatmap_id'] = play['beatmap']['id']
            play_info['score'] = play['score']
            play_info['pp'] = play['pp']
            play_info['rank'] = play['rank']
            play_info['date'] = play['created_at']
            play_info['enabled_mods'] = mod_to_num(''.join(play['mods']))
            play_info['maxcombo'] = play['max_combo']
            play_info['count300'] = play['statistics']['count_300']
            play_info['count100'] = play['statistics']['count_100']
            play_info['count50'] = play['statistics']['count_50']
            play_info['countgeki'] = play['statistics']['count_geki']
            play_info['countkatu'] = play['statistics']['count_katu']
            play_info['countmiss'] = play['statistics']['count_miss']
            play_list.append(play_info)

            acc_list.append(float(play['accuracy']*100))

        return play_list, map_list, acc_list

    # written by Jams
    async def _get_user_scores(self, ctx, api, map_id, user, userscore, gamemode:int, beatmap):
        server_user = ctx.message.author
        server = ctx.message.server
        key = self.api_keys["osu_api_key"]

        if api == self.osu_settings["type"]["default"]:
            profile_url ='https://a.ppy.sh/{}'.format(user['user_id'])
        elif api == self.osu_settings["type"]["ripple"]:
            profile_url = 'http://a.ripple.moe/{}.png'.format(user['user_id'])

        flag_url = 'https://osu.ppy.sh/images/flags/{}.png'.format(user['country'])
        gamemode_text = get_gamemode(gamemode)

        # sort the scores based on pp
        userscore = sorted(userscore, key=operator.itemgetter('pp'), reverse=True)

        # get best plays map information and scores
        best_beatmaps = []
        best_acc = []
        pp_sort = []
        for i in range(len(userscore)):
            score = userscore[i]
            best_beatmaps.append(beatmap)
            best_acc.append(calculate_acc(score,gamemode))

        all_plays = []
        desc = ''
        mapname = '{} [{}]'.format(
            best_beatmaps[i]['title'],
            best_beatmaps[i]['version'])

        for i in range(len(userscore)):
            mods = num_to_mod(userscore[i]['enabled_mods'])
            oppai_info = await get_pyoppai(best_beatmaps[i]['beatmap_id'], accs = [float(best_acc[i])], mods = int(userscore[i]['enabled_mods']))

            if not mods:
                mods = []
                mods.append('No Mod')
            beatmap_url = 'https://osu.ppy.sh/b/{}'.format(best_beatmaps[i]['beatmap_id'])

            info = ''
            star_str, _ = compare_val(best_beatmaps[i]['difficultyrating'], oppai_info, param = 'stars', dec_places = 2, single = True)
            info += '**{}. {} Score** [{}★]\n'.format(
                i+1, fix_mods(''.join(mods)), star_str)
            # choke text
            choke_text = ''
            if (oppai_info != None and userscore[i]['countmiss'] != None and best_beatmaps[i]['max_combo']!= None) and (int(userscore[i]['countmiss'])>=1 or (int(userscore[i]['maxcombo']) <= 0.95*int(best_beatmaps[i]['max_combo']) and 'S' in userscore[i]['rank'])):
                choke_text += ' _({:.2f}pp for FC)_'.format(oppai_info['pp'][0])
            info += '▸ **{} Rank** ▸ **{:.2f}pp**{} ▸ {:.2f}%\n'.format(userscore[i]['rank'], float(userscore[i]['pp']), choke_text, float(best_acc[i]))
            info += '▸ {} ▸ x{}/{} ▸ [{}/{}/{}/{}]\n'.format(
                userscore[i]['score'],
                userscore[i]['maxcombo'], best_beatmaps[i]['max_combo'],
                userscore[i]['count300'],userscore[i]['count100'],userscore[i]['count50'],userscore[i]['countmiss']
                )

            timeago = time_ago(datetime.datetime.utcnow() + datetime.timedelta(hours=8), datetime.datetime.strptime(userscore[i]['date'], '%Y-%m-%d %H:%M:%S'))
            info += '▸ Score Set {}Ago\n'.format(timeago)

            desc += info
        em = discord.Embed(description=desc, colour=server_user.colour)
        title = "Top {} Plays for {} on {}".format(gamemode_text, user['username'], mapname)
        em.set_author(name = title, url="https://osu.ppy.sh/b/{}".format(map_id), icon_url=flag_url)
        em.set_footer(text = "On osu! {} Server".format(self._get_api_name(api)))
        em.set_thumbnail(url=profile_url)

        return ("", em)

    #--------------------- Suggestion Database Creation/Methods ------------------------
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(pass_context=True, no_pm=True, aliases = ['r','rec'])
    async def recommend(self, ctx, *options):
        """>recommend [mods] [target pp]"""
        key = self.api_keys["osu_api_key"]
        # gives the final input for osu username
        username = ctx.message.author.name
        username = await self._process_username(ctx, username)

        if not username:
            return
        if len(options) > 2:
            await self.bot.say('**Incorrect usage: `>recommend [mods] [target pp]`**')
            return

        mods = None
        target_pp = None
        for option in options:
            if option.isnumeric():
                target_pp = float(option)
            else:
                if str(option).lower() == 'nomod':
                    mods = ''
                elif str(option).lower() == 'any':
                    mods = 'ANY'
                else:
                    mods = str(option)

        #print('Target pp: ', str(target_pp), 'Mods: ', mods)

        top_num = 10 # use top 12 plays
        gamemode = 0
        try:
            userbest = list(await get_user_best(
                key, self.osu_settings["type"]["default"], username, gamemode, top_num))
        except:
            await self.bot.say('Error. Please try again later.')
            return

        # get statistics for these plays <- should be its own function
        # since used multiple times (-d)
        top_beatmap_ids = []
        moddic = {}
        totals = 0
        sum_pp = 0
        for i in range(len(userbest)):
            score = userbest[i]
            top_beatmap_ids.append(score['beatmap_id'])
            mod_text = fix_mods(''.join(num_to_mod(score['enabled_mods'])))

            unweighted = float(score['pp'])
            sum_pp += float(score['pp'])
            if not mod_text in moddic.keys():
                moddic[mod_text] = unweighted
                totals += unweighted
            else:
                moddic[mod_text] += unweighted
                totals += unweighted

        if target_pp is None:
            if len(userbest) != 0:
                average_pp = sum_pp/len(userbest)
                average_pp += random.randint(0, int(average_pp/5))
            else:
                await self.bot.say('**Not enough plays.**')
                return
        else:
            average_pp = target_pp

        mods_unweighted = sorted(list(moddic.items()), key=operator.itemgetter(1), reverse=True)
        mods_unweighted = mods_unweighted[:3]

        # give recommendation
        pp_range = determine_pp_range(average_pp)
        full_pp_list = db.suggest_osu.find_one({'pp_range':pp_range})
        if not full_pp_list:
            await self.bot.say('**No suggestions at the moment.**')
            return

        # handle what mod to look for
        if mods != 'ANY':
            if mods is None: # based on player's mods
                # I could make this weighted, but whatever
                mods = random.choice([best_mod for best_mod, _ in mods_unweighted])
            elif mods is not None:
                mods = mods.replace('+','').upper()
            user_mods = set(num_to_mod(mod_to_num(mods))) # mods is now a set

        suggest_list = []
        for beatmap_id, mod_combo_list in full_pp_list['beatmaps']:
            map_mods = set(num_to_mod(mod_to_num(
                ''.join(mod_combo_list).replace('SD', '').replace('PF', ''))))

            # won't check anything else if mods = ANY
            if mods == 'ANY' or (user_mods == map_mods and beatmap_id not in top_beatmap_ids):
                # print('Mods detected. {} {}'.format(str(mod), str(mods)))
                suggest_list.append((beatmap_id, ''.join(list(map_mods))))

        if suggest_list:
            beatmap_id, mods = random.choice(suggest_list)
            beatmap_url = 'https://osu.ppy.sh/b/{}'.format(beatmap_id)
            beatmap = await get_beatmap(key, self.osu_settings["type"]["default"], beatmap_id)
            await self.disp_beatmap(ctx.message, beatmap, beatmap_url, mods=mods, username = ctx.message.author.name)
        else:
            await self.bot.say('**No suggestions at the moment.**')
            return

    # this code is very similar to the play tracker
    async def suggestion_play_parser(self, player):
        # ensures that data is recieved
        got_data = False
        get_data_counter = 1
        top_plays = None
        mode = 0
        if 'osu_id' in player:
            osu_id = player['osu_id']
        else:
            osu_id = player['userinfo']['osu']['user_id']

        key = self.api_keys["osu_api_key"]
        while(not got_data and get_data_counter <= 10):
            try:
                top_plays = await get_user_best(
                    key, self.osu_settings["type"]["default"], osu_id,
                    mode, self.osu_settings["num_track"])
                got_data = True
            except:
                get_data_counter += 1

        if top_plays is None:
            return

        # if still no data
        if top_plays == None:
            print("Data fetched failed for {}".format(player['username']))
            return

        for play in top_plays:
            await self._append_suggestion_database(play)

    async def _append_suggestion_database(self, play):
        # calculate the pp for the beatmap
        accs = [100] # based on 100% acc
        mods_list = num_to_mod(play['enabled_mods']) # list
        oppai_output = await get_pyoppai(play['beatmap_id'], accs=accs, mods = int(play['enabled_mods']))
        if not oppai_output:
            return

        pp_100 = float(oppai_output['pp'][0])
        pp_range = determine_pp_range(pp_100)
        # create structure...
        section = db.suggest_osu.find_one({'pp_range':pp_range})
        if not section:
            """
            new_play = self._new_database_entry(play, oppai_output, mods_list)
            new_range = {'pp_range':pp_range, 'beatmaps': [new_play]}
            db.suggest_std.insert_one(new_range)
            """
            new_range = {'pp_range':pp_range, 'beatmaps': [(play['beatmap_id'], mods_list)]}
            db.suggest_osu.insert_one(new_range)
        else:
            for temp_beatmap, temp_mods in section['beatmaps']:
                if temp_beatmap == play['beatmap_id'] and temp_mods == mods_list:
                    return
            """
            new_play = self._new_database_entry(play, oppai_output, mods_list)
            section['beatmaps'].append(new_play)
            db.suggest_std.update_one({'pp_range':pp_range}, {'$set':{"beatmaps":section['beatmaps']}})
            """
            section['beatmaps'].append((play['beatmap_id'], mods_list))
            db.suggest_osu.update_one({'pp_range':pp_range}, {'$set':{"beatmaps":section['beatmaps']}})
        print("New {}, beatmap_id: {} mods: {}".format(pp_range, play['beatmap_id'], str(mods_list)))

    def _new_database_entry(self, play, oppai_output, mods_list):
            new_play = {}
            new_play['beatmap_id'] = play['beatmap_id']
            new_play['mods_list'] = mods_list
            bpm = play['bpm']
            if 'DT' in mods:
                bpm *= 1.5
            elif 'HT' in mods:
                bpm /= 1.5
            new_play['bpm'] = bpm
            new_play['ar'] = oppai_output['ar']
            new_play['od'] = oppai_ouput['od']

    # ---------------------------- Detect Links ------------------------------
    # called by listener
    async def find_link(self, message):
        # await self.bot.send_message(message.channel, 'URL DETECTED')
        server = message.server

        #try:
        if message.author.id == self.bot.user.id:
            return
        if message.content.startswith(prefix):
            return

        # ------------------------ get attachments ------------------------
        all_urls = []
        # get all attachments
        in_attachments = False
        for att in message.attachments:
            if 'screenshot' in str(att).lower():
                all_urls.append((str(att['proxy_url']), ''))
                in_attachments = True

        # process from a url in msg
        original_message = message.content

        # this is just me being extremely lazy and not wanting to deal with regex, will fix later
        for domain in ['osu', 'ripple', 'puu']:
            get_urls = re.findall("(https:\/\/{}[^\s]+)([ ]\+[A-Za-z][^\s]+)?".format(domain), original_message)
            for url in get_urls:
                all_urls.append(url)
            get_urls = re.findall("(http:\/\/{}[^\s]+)([ ]\+[A-Za-z][^\s]+)?".format(domain), original_message)
            for url in get_urls:
                all_urls.append(url)

        # get rid of duplicates
        all_urls = list(set(all_urls))

        if len(all_urls) > 3:
            all_urls = all_urls[0:3]
            await self.bot.send_message(message.channel, "Too many things, processing first 3.")

        ## -------------------- user url detection ---------------------

        if 'https://osu.ppy.sh/u/' in original_message:
            await self.process_user_url(all_urls, message)

        ## -------------------- beatmap detection ---------------------
        try:
            server_options = db.options.find_one({"server_id":server.id})
        except:
            return

        if server_options is None or server_options["beatmap"]:
            # try:
            beatmap_url_triggers = [
                'https://osu.ppy.sh/s/',
                'https://osu.ppy.sh/b/',
                'http://osu.ppy.sh/ss/',
                'https://osu.ppy.sh/ss/',
                'http://ripple.moe/ss/',
                'https://ripple.moe/ss/',
                'https://puu.sh',
                '.jpg', '.png'
                ]

            if any([link in original_message for link in beatmap_url_triggers]) or in_attachments:
                # print('LINK DETECTED!')
                await self.process_beatmap(all_urls, message, server_options)
            #except:
                #pass

    # processes user input for user profile link
    async def process_user_url(self, all_urls, message):
        key = self.api_keys["osu_api_key"]
        server_user = message.author
        try:
            server = message.author.server
        except:
            await self.bot.send_message('Cannot execute here.')
            return

        for url, suffix in all_urls:
            try:
                if url.find('https://osu.ppy.sh/u/') != -1:
                    user_id = url.replace('https://osu.ppy.sh/u/','')
                    user_info = await get_user(
                        key, self.osu_settings["type"]["default"], user_id, 0)
                    find_user = db.user_settings.find_one({"user_id":user_id})
                    if find_user:
                        gamemode = int(find_user["default_gamemode"])
                    else:
                        gamemode = 0
                    em = await self._get_user_info(
                        self.osu_settings["type"]["default"],
                        server, server_user, user_info[0], gamemode)
                    await self.bot.send_message(message.channel, embed = em)
            except:
                pass

    # processes user input for the beatmap
    async def process_beatmap(self, all_urls, message, server_options = None):
        key = self.api_keys["osu_api_key"]
        # print(all_urls)
        for url, mods in all_urls:
            screenshot_links = [
                'http://osu.ppy.sh/ss/',
                'https://osu.ppy.sh/ss/',
                'http://ripple.moe/ss/',
                'https://ripple.moe/ss/',
                'https://puu.sh',
                '.jpg', '.png'
                ]

            is_screenshot = any([url.find(link) != -1 for link in screenshot_links]) # checked twice..?
            #try:
            if url.find('https://osu.ppy.sh/s/') != -1:
                beatmap_id = url.replace('https://osu.ppy.sh/s/','')
                beatmap_info = await get_beatmapset(key, self.osu_settings["type"]["default"], beatmap_id)
                extra_info = None
                display_if = (server_options and server_options['graph_beatmap']) or (server_options is None)
                include_graph = display_if and len(beatmap_info) == 1
            elif url.find('https://osu.ppy.sh/b/') != -1:
                beatmap_id = url.replace('https://osu.ppy.sh/b/','')
                # find mods
                beatmap_info = await get_beatmap(key, self.osu_settings["type"]["default"], beatmap_id)
                extra_info = None
                include_graph = True
                if server_options and not server_options['graph_beatmap']:
                    include_graph = False
            elif is_screenshot:
                # (beatmap_info, beatmap_id, mods, pp, mode)
                print('Screenshot Detected!')
                if server_options is None or server_options["screenshot"]:
                    beatmap_info, beatmap_id, mods, map_url, extra_info = await self._get_screenshot_map(
                        url, unique_id = str(message.author.id))
                    url = map_url
                    include_graph = False # default is true
                    if server_options and server_options['graph_screenshot']:
                        include_graph = True
                else:
                    beatmap_info = None
            else: # catch all case
                beatmap_info = None

            if beatmap_info:
                #print(include_graph)
                await self.disp_beatmap(message, beatmap_info, url, mods, extra_info = extra_info, graph = include_graph)
            #except:
                #pass

    async def _get_screenshot_map(self, url, unique_id):
        key = self.api_keys["osu_api_key"]

        if not unique_id:
            unique_id = '0'

        # print(url)

        filepath = 'data/osu/temp/ss_{}.png'.format(unique_id)
        none_response = (None, None, None, None, None)

        # print("GETTING IMAGE")
        # determine if valid image
        try:
            async with aiohttp.get(url) as r:
                image = await r.content.read()
            with open(filepath,'wb') as f:
                f.write(image)
                f.close()
            original_image = Image.open(filepath)
        except:
            return none_response

        # print("IMAGE RETRIEVED")

        # get certain measurements for screenshot
        height = original_image.size[1]
        width = original_image.size[0]
        title_bar_height = height*0.124 # approximate ratio
        title_bar_width = width*0.66 # approximate ratio
        info_image = original_image.crop((0, 0, title_bar_width, title_bar_height))
        # info_image.save('ss_test.png')
        # deallocate memory?
        os.remove(filepath)
        info = pytesseract.image_to_string(info_image).split('\n')

        # process info
        map_name = None
        map_author = None # not as important
        player_name = None
        # print(info)
        for text in info:
            if len(text) != 0:
                if ('-' in text or "—" in text) and not map_name:
                    map_name = text

                played_by_present = get_similarity('Played by', text) > (len('Played by')/len(text))*(0.9)
                if played_by_present and not player_name and "by" in text:
                    player_name = text[text.find('by')+3:]
                    player_name = player_name[0:player_name.find(' on ')]
                    player_name = player_name.replace('|<', 'k').replace('l<', 'k')

                beatmap_author_present = get_similarity('Beatmap by', text) > (len('Beatmap by')/len(text))*(0.9)
                if beatmap_author_present and "by" in text:
                    map_author = text[text.find('by')+3:]

        # -------- last resorts for map names --------
        if len(info) > 0 and not map_name:
            map_name = info[0] # try setting the map name to the first thing

        # if there's no difficulty information, then try the whole top
        if '[' not in map_name or ']' not in map_name:
            title_image = original_image.crop((0, 0, width, title_bar_height/3 + 2))
            map_name = pytesseract.image_to_string(title_image)

        # print
        print(player_name, map_name, map_author)

        # deallocated memory?
        original_image = None
        info = None

        # if it couldn't get the name, not point in continuing
        if map_name is None or len(map_name) < 5:
            return none_response

        # first try top scores, then try recent plays
        for mode in modes2:
            for attr in ['best', 'recent']:
                # get from site
                try:
                    url = 'https://osu.ppy.sh/users/{}/{}'.format(player_name, mode)
                    soup = await get_web(url, parser = "lxml")
                    script = soup.find('script',{"id": "json-scores"})
                    user = json.loads(script.get_text())
                    success = True

                    beatmap_info = None
                    mods = ''
                except:
                    continue

                if attr == "best":
                    list_type = "Top"
                else:
                    list_type = "Recent"

                #try:
                plays = user[attr]
                for play in plays:
                    # using api to be consistent
                    if 'title' in play['beatmapset']:
                        compiled_name = "{} - {} [{}]".format(
                            play['beatmapset']['artist'],
                            play['beatmapset']['title'],
                            play['beatmap']['version'])
                        similarity = get_similarity(compiled_name, map_name)
                        # print(similarity)
                        if compiled_name in map_name or similarity >= 0.85: # high threshhold
                            # no pp if not top
                            if attr == "best":
                                pp = play["pp"]
                            else:
                                pp = None

                            extra_info = {
                                "rank": play["rank"],
                                "pp": pp,
                                "created_at": play['created_at'],
                                "accuracy": play['accuracy'],
                                "username": player_name.capitalize(),
                                "statistics": play['statistics'],
                                "type": list_type
                                }
                            mods = fix_mods(''.join(play['mods']))
                            beatmap_id = play['beatmap']['id']
                            url = 'https://osu.ppy.sh/b/{}'.format(beatmap_id)
                            beatmap_info = await get_beatmap(key, self.osu_settings["type"]["default"], beatmap_id)
                            return (beatmap_info, beatmap_id, mods, url, extra_info)

        # if that fails, try searching google? use only map name
        #try:
        author_query = ""
        if map_author:
            author_query = "(mapped by {})".format(map_author)

        search_query = "{} {} - Osu!".format(map_name, author_query).replace('|<', 'k')
        print(search_query)
        google_results = await get_google_search(search_query)
        # print(google_results)
        g_result_upper_threshold = 0.99
        overall_map_list = []
        max_similarity = 0
        map_sims = []
        for result in google_results:
            if 'https://osu.ppy.sh/s/' in result:
                url = ''
                beatmapset_id = result.replace('https://osu.ppy.sh/s/','')
                beatmap_info = await get_beatmapset(key, self.osu_settings["type"]["default"], beatmapset_id)
                # grab the correct map
                max_similarity = 0
                map_sims = []
                for bm in beatmap_info:
                    title = '{} - {} [{}]'.format(bm['artist'], bm['title'], bm['version'])
                    max_similarity = max(max_similarity, get_similarity(title, map_name))
                    map_sims.append(max_similarity)

                map_index = map_sims.index(max_similarity)
                # print(map_sims, map_index)
                bm_info = beatmap_info[map_index]
                beatmap_id = beatmap_info[map_index]["beatmap_id"]
                url = 'https://osu.ppy.sh/b/{}'.format(beatmap_id)

                return_tup = ([bm_info], beatmap_id, '', url, None)
                if max_similarity >= g_result_upper_threshold:
                    return return_tup
                else:
                    overall_map_list.append((max_similarity, return_tup))

            elif 'https://osu.ppy.sh/b/' in result:
                url = result
                beatmap_id = result.replace('https://osu.ppy.sh/b/','')
                beatmap_info = await get_beatmap(key, self.osu_settings["type"]["default"], beatmap_id)
                beatmap_info = beatmap_info[0]
                title = '{} - {} [{}]'.format(beatmap_info['artist'], beatmap_info['title'], beatmap_info['version'])
                max_similarity = max(max_similarity, get_similarity(title, map_name))
                map_sims.append(max_similarity)

                return_tup = ([beatmap_info], beatmap_id, '', url, None)
                if max_similarity >= g_result_upper_threshold: # threshhold
                    return return_tup
                else:
                    overall_map_list.append((max_similarity, return_tup))

        # get if none of them are extremely accurate, pick the most accurate
        # print(overall_map_list)
        if overall_map_list:
            sorted(overall_map_list, key=operator.itemgetter(0), reverse = True)
            return overall_map_list[0][1]

        return none_response

    # displays the beatmap properly
    async def disp_beatmap(self, message, beatmap, beatmap_url:str, mods='', extra_info = None, graph = False, username = None):
        # create embed
        em = discord.Embed()

        # process time
        num_disp = min(len(beatmap), self.max_map_disp)
        if (len(beatmap) > self.max_map_disp):
            msg = "Found {} maps, but only displaying {}.\n".format(len(beatmap), self.max_map_disp)
        else:
            msg = "Found {} map(s).\n".format(len(beatmap))

        # sort by difficulty first
        map_order = []
        for i in range(len(beatmap)):
            map_order.append((i,float(beatmap[i]['difficultyrating'])))
        map_order = sorted(map_order, key=operator.itemgetter(1), reverse=True)
        map_order = map_order[0:num_disp]

        beatmap_msg = ""
        oppai_version = ""
        accs = [95, 99, 100]

        mods = fix_mods(mods.upper())
        mod_num = mod_to_num(mods)

        # deal with extra info
        if extra_info and extra_info['pp'] == None:
            statistics = extra_info['statistics']
            totalhits = int(statistics['count_50']) + int(statistics['count_100']) + int(statistics['count_300']) + int(statistics['count_miss'])
            user_oppai_info = await get_pyoppai(
                beatmap[0]['beatmap_id'], accs = [float(extra_info['accuracy']*100)], mods = mod_num, completion = totalhits)
            extra_info['pp'] = user_oppai_info['pp'][0]

        # safe protect
        if self.imgur.credits['ClientRemaining'] is not None and int(self.imgur.credits['ClientRemaining']) >= 60:
            imgur_object = self.imgur
        else:
            imgur_object = None

        oppai_info = await get_pyoppai(beatmap[0]['beatmap_id'], accs = accs, mods = mod_num, plot = graph, imgur = imgur_object)

        m0, s0 = divmod(int(beatmap[0]['total_length']), 60)
        if oppai_info != None:
            # oppai_version = oppai_info['oppai_version']
            if 'DT' in mods or 'HT' in mods or 'NC' in mods:
                if 'DT' in mods or 'NC' in mods:
                    m1, s1, bpm_mod = calc_time(beatmap[0]['total_length'], beatmap[0]['bpm'], 1.5)
                elif 'HT' in mods:
                    m1, s1, bpm_mod = calc_time(beatmap[0]['total_length'], beatmap[0]['bpm'], (2/3))
                desc = '**Length:** {}:{}({}:{})  **BPM:** {:.1f}({}) '.format(
                    m0, str(s0).zfill(2),
                    m1, str(s1).zfill(2),
                    float(beatmap[0]['bpm']), bpm_mod)
            else:
                desc = '**Length:** {}:{} **BPM:** {}  '.format(m0,
                    str(s0).zfill(2), beatmap[0]['bpm'])
        else:
            desc = '**Length:** {}:{} **BPM:** {}  '.format(m0,
                str(s0).zfill(2), beatmap[0]['bpm'])

        # Handle mods
        desc += "**Mods:** "
        if mods != '':
            desc += mods
        else:
            desc += '-'
        desc += '\n'

        for i, diff in map_order:
            if i == 0:
                temp_oppai_info = oppai_info
            elif oppai_info == None:
                temp_oppai_info == None
            else:
                temp_oppai_info = await get_pyoppai(beatmap[i]['beatmap_id'], accs = accs, mods = mod_num)

            # updated values, if it has the oppai value, it will give it
            stars, stars_val = compare_val(beatmap[i]['difficultyrating'], temp_oppai_info, param = 'stars', dec_places = 2)
            ar, ar_val = compare_val(beatmap[i]['diff_approach'], temp_oppai_info, param = 'ar')
            od, od_val = compare_val(beatmap[i]['diff_overall'], temp_oppai_info, param = 'od')
            hp, hp_val = compare_val(beatmap[i]['diff_drain'], temp_oppai_info, param = 'hp')
            cs, cs_val = compare_val(beatmap[i]['diff_size'], temp_oppai_info, param = 'cs')
            max_combo, max_combo_val = compare_val(beatmap[i]['max_combo'], temp_oppai_info, param = 'max_combo', dec_places = 0)

            # calculate pp for other gamemodes if necessary
            gamemode = int(beatmap[i]['mode'])
            # print(gamemode)

            if gamemode == 1: # taiko
                temp_oppai_info['pp'] = await _get_taiko_pp(
                    stars_val, od_val, max_combo_val, accs = accs, mods = mods)
            elif gamemode == 2: # ctb
                temp_oppai_info['pp'] = await _get_ctb_pp(
                    stars, beatmap[i]['diff_approach'], max_combo_val, accs = accs, mods = mods)
            """elif gamemode == 3: # mania
                # print(temp_oppai_info)
                # print(beatmap[i])
                temp_oppai_info['pp'] = await _get_mania_pp(
                    beatmap[i]['difficultyrating'], od_val, temp_oppai_info['max_combo'], score = None, accs = accs, mods = mods)"""

            beatmap_info = ""
            beatmap_info += "**▸Difficulty:** {}★ **▸Max Combo:** x{}\n".format(
                stars, max_combo)
            beatmap_info += "**▸AR:** {} **▸OD:** {} **▸HP:** {} **▸CS:** {}\n".format(
                ar, od, hp, cs)

            # calculate pp values
            if temp_oppai_info != None:
                beatmap_info += '**▸PP:** '
                for j in range(len(accs[0:3])):
                    beatmap_info += '○ **{}%**–{:.2f} '.format(accs[j], temp_oppai_info['pp'][j])

            show_mode = ''
            if gamemode != 0:
                show_mode = ' [{}]'.format(modes[gamemode])

            em.add_field(name = "__{}__{}\n".format(beatmap[i]['version'], show_mode), value = beatmap_info, inline = False)

        # download links
        dl_links = self._get_dl_links(beatmap[i]['beatmapset_id'], beatmap[i]['beatmap_id'])
        desc += '**Download:** [map]({})([no vid]({}))  [osu!direct]({})  [bloodcat]({})\n'.format(
            dl_links[0],dl_links[1],dl_links[2],dl_links[3])
        desc += '-------------------\n'

        # if it's a screenshot and score is detected
        if extra_info:
            official = ""
            if extra_info['type'] == "Recent":
                official = " _(Not official)_"

            pp = "-"
            if extra_info['pp']:
                pp = "{:.2f}".format(float(extra_info['pp']))

            desc += "**{} play for [{}]({})\n▸ {} rank  ▸ {}pp{}  ▸ {:.2f}%**\n".format(
                extra_info['type'],
                extra_info['username'], 'https://osu.ppy.sh/users/{}'.format(extra_info['username'].replace(' ', '\\_').replace("_", "\\_")),
                extra_info['rank'], pp, official, float(extra_info['accuracy']*100))
            timeago = time_ago(
                datetime.datetime.utcnow(),
                datetime.datetime.strptime(extra_info['created_at'], '%Y-%m-%dT%H:%M:%S+00:00')) # 2016-11-04T04:20:35+00:00
            desc += 'Played {}Ago\n'.format(timeago) # timestamp
            desc += '-------------------'

        # determine color of embed based on status
        colour, colour_text = self._determine_status_color(int(beatmap[i]['approved']))

        # create return em
        em.colour = colour
        em.description = desc
        em.set_author(name="{} – {} by {}".format(beatmap[0]['artist'], beatmap[0]['title'], beatmap[0]['creator']), url=beatmap_url)
        soup = await get_web(beatmap_url)
        map_image = [x['src'] for x in soup.findAll('img', {'class': 'bmt'})]
        map_image_url = 'http:{}'.format(map_image[0]).replace(" ", "%")
        em.set_thumbnail(url=map_image_url)
        if oppai_info and 'graph_url' in oppai_info:
            em.set_image(url=oppai_info['graph_url'])

        # await self.bot.send_message(message.channel, map_image_url)
        for_user = ''
        if username is not None:
            for_user = 'Request for {} | '.format(username)

        em.set_footer(text = '{} | {}Powered by Oppai v0.9.5'.format(colour_text, for_user))

        await self.bot.send_message(message.channel, msg, embed = em)

    def _get_dl_links(self, beatmapset_id, beatmap_id):
        vid = 'https://osu.ppy.sh/d/{}'.format(beatmapset_id)
        novid = 'https://osu.ppy.sh/d/{}n'.format(beatmapset_id)
        direct = 'osu://b/{}'.format(beatmap_id)
        bloodcat = 'https://bloodcat.com/osu/s/{}'.format(beatmapset_id)

        ret = [vid, novid, direct, bloodcat]
        return ret

    def _determine_status_color(self, status):
        colour = 0xFFFFFF
        text = 'Unknown'

        if status == -2: # graveyard, red
            colour = 0xc10d0d
            text = 'Graveyard'
        elif status == -1: # WIP, purple
            colour = 0x713c93
            text = 'Work in Progress'
        elif status == 0: # pending, blue
            colour = 0x1466cc
            text = 'Pending'
        elif status == 1: # ranked, bright green
            colour = 0x02cc37
            text = 'Ranked'
        elif status == 2: # approved, dark green
            colour = 0x0f8c4a
            text = 'Approved'
        elif status == 3: # qualified, turqoise
            colour = 0x00cebd
            text = 'Qualified'
        elif status == 4: # loved, pink
            colour = 0xea04e6
            text = 'Loved'

        return (colour, text)

# ----------------------- Tracking Section -------------------------------
class Tracking:
    def __init__(self, bot):
        self.bot = bot
        self.osu_settings = fileIO("data/osu/osu_settings.json", "load")
        self.api_keys = fileIO("data/osu/apikey.json", "load")
        self.max_requests = 1100 # per minute, for tracking only
        self.total_requests = 0
        self.server_send_fail = []
        self.cycle_time = 0
        self.sleep_time = 0.01 # initial
        self.track_server_limit = 150
        global api_counter
        self.latency = collections.deque(maxlen = 300)
        if os.path.exists('data/osu/temp/latency.txt'):
            with open('data/osu/temp/latency.txt', "r") as f:
                for line in f:
                    self.latency.append(int(line.strip()))

    @commands.group(pass_context=True)
    async def osutrack(self, ctx):
        """Set some tracking options"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    # @commands.cooldown(1, 300, commands.BucketType.user)
    @osutrack.command(name = "latency", pass_context=True, no_pm=True)
    async def graph_latency(self, ctx):
        """Check tracking latency for past 300 plays"""
        channel = ctx.message.channel

        plt.figure(figsize=(10, 5))
        plt.style.use('ggplot')
        self.latency = collections.deque([i for i in self.latency if i < 1200], maxlen = 300)
        x = np.array(self.latency)/60 # for minutes
        plt.hist(x, bins=18, color='c')
        plt.axvline(x.mean(), color='b', linestyle='dashed', linewidth=2)
        plt.xlabel('min')
        plt.ylabel('# Plays')
        plt.tight_layout()
        filepath = 'data/osu/temp/latency.png'
        plt.savefig(filepath)
        plt.close()
        await self.bot.send_file(channel, filepath, content='**Tracking Latency for Previous 300 Plays**')
        # self.save_latency()

    async def save_latency(self):
        # save the data somewhere
        filepath = 'data/osu/temp/latency.txt'
        with open(filepath, "w") as f:
            for l in self.latency:
                f.write(str(l) +"\n")

    @osutrack.command(pass_context=True, no_pm=True)
    async def list(self, ctx):
        """Check which players are currently tracked"""
        server = ctx.message.server
        channel = ctx.message.channel
        user = ctx.message.author
        max_users = 30

        em = discord.Embed(colour=user.colour)
        em.set_author(name="osu! Players Currently Tracked in {}".format(server.name), icon_url = server.icon_url)
        channel_users = {}

        target_channel = None
        for track_user in db.track.find({}):
            if "servers" in track_user and server.id in track_user["servers"]:
                target_channel = find(lambda m: m.id == track_user['servers'][server.id]["channel"], server.channels)
                if target_channel.name not in channel_users:
                    channel_users[target_channel.name] = []


                if "options" in track_user['servers'][server.id]:
                    options = track_user['servers'][server.id]["options"]
                else:
                    options = None
                channel_users[target_channel.name].append((track_user['username'], options))

        if target_channel:
            display_num = min(max_users, len(channel_users[target_channel.name]))
        else:
            display_num = 0

        if target_channel:
            channel_users[target_channel.name] = sorted(channel_users[target_channel.name], key=operator.itemgetter(0))
            for channel_name in channel_users.keys():
                display_list = []
                for username, options in channel_users[channel_name][0:display_num]:
                    if options is not None:
                        display_list.append("{} [m:`{}` t:`{}`]".format(username, "|".join(map(str, options['gamemodes'])), str(options['plays'])))
                    else:
                        display_list.append("{} [m:`0` t:`50`]".format(username))

                msg_users = ", ".join(display_list)
                if display_num < len(channel_users[channel_name]):
                    msg_users += "..."
                em.add_field(name = "__#{} ({})__".format(channel_name, len(channel_users[channel_name])), value = msg_users)
        else:
            em.description = "None."
        await self.bot.say(embed = em)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @osutrack.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def add(self, ctx, *usernames:str):
        """Adds a player to track for top scores.\n"""
        """-m (gamemodes) -t (top # plays)"""
        """osutrack add username1 username2 -m 03 -t 30"""
        server = ctx.message.server
        channel = ctx.message.channel

        key = self.api_keys["osu_api_key"]
        msg = ""
        count_add = 0
        count_update = 0

        if usernames == ():
            await self.bot.say("**Please enter a user (+ Parameters)! e.g. `Stevy -m 02 -t 20`**")
            return

        # gets options for tracking
        options, usernames = await self._get_options(usernames)
        if options == None:
            return

        for username in usernames:
            track_num = self._get_server_track_num(server)
            if track_num >= self.track_server_limit:
                await self.bot.say('**You are at or past the user tracking limit: `{}` Tracked.**'.format(str(track_num)))
                msg = "**Added `{}` users to tracking on `#{}`. {}**".format(count_add, channel.name,self._display_options(options))
                break

            #try:
            userinfo = list(await get_user(key, self.osu_settings["type"]["default"], username, 0))

            if not userinfo or len(userinfo) == 0:
                msg += "`{}` does not exist in the osu! database.\n".format(username)
            else:
                userinfo = userinfo[0]
                username = userinfo['username']
                osu_id = userinfo["user_id"]
                track_user = db.track.find_one({"osu_id":osu_id})
                track_user_username = db.track.find_one({"username":username})

                if not track_user:
                    # backwards compatibility
                    if track_user_username and not track_user:
                        print("Existing Create ID")
                        db.track.update_one({"username":username}, {'$set':{"osu_id":osu_id}})
                    else:
                        new_json = {}
                        new_json['username'] = username
                        new_json['osu_id'] = osu_id
                        new_json["servers"] = {}
                        new_json["servers"][server.id] = {}
                        new_json["servers"][server.id]["channel"] = channel.id
                        new_json["servers"][server.id]["options"] = options
                        # add current userinfo
                        new_json["userinfo"] = {}
                        for mode in modes:
                            new_json["userinfo"][mode] = list(await get_user(key, self.osu_settings["type"]["default"], osu_id, get_gamemode_number(mode), no_cache = True))[0]
                            self.total_requests += 1

                        # add last tracked time
                        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        new_json["last_check"] = current_time
                        db.track.insert_one(new_json)
                    count_add += 1
                    msg += "**`{}` added. Will now track on `#{}`. {}**\n".format(username, channel.name, self._display_options(options))
                else:
                    count_add += 1
                    if "servers" in track_user and server.id in track_user["servers"].keys():
                        track_user["servers"][server.id]["channel"] = channel.id
                        track_user["servers"][server.id]["options"] = options
                        db.track.update_one({"osu_id":osu_id}, {'$set':{
                            "servers.{}.channel".format(server.id):channel.id,
                            "servers.{}.options".format(server.id):options,
                            }})

                        msg += "**Updated tracking `{}` on `#{}`. {}**\n".format(username, channel.name, self._display_options(options))
                    else:
                        db.track.update_one({"osu_id":osu_id}, {'$set':{
                            "servers.{}.channel".format(server.id):channel.id,
                            "servers.{}.options".format(server.id):options,
                            }})
                        msg += "**`{}` now tracking on `#{}`. {}**\n".format(username, channel.name, self._display_options(options))
            #except:
                #pass
            await asyncio.sleep(self.sleep_time)

        if len(msg) > 500:
            await self.bot.say("**Added `{}` users to tracking on `#{}`. {}**".format(count_add, channel.name,self._display_options(options)))
        else:
            await self.bot.say(msg)

    def _get_server_track_num(self, server):
        """Reads database to see how many people are tracked on this server"""
        counter = 0
        target_channel = None
        for track_user in db.track.find({}):
            if "servers" in track_user and server.id in track_user["servers"]:
                counter += 1
        return counter

    def _display_options(self, options):
        msg = ""
        gamemodes_str = []
        for mode in options['gamemodes']:
            gamemodes_str.append(str(mode))

        msg += "(Modes: `{}`, Plays: `{}`)".format('|'.join(gamemodes_str), str(options['plays']))
        return msg

    @osutrack.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_messages=True)
    async def clear(self, ctx):
        """Clear all tracked users from server."""
        server = ctx.message.server
        user = ctx.message.author

        await self.bot.say('**You are about to clear users tracked on this server. Confirm by typing `yes`.**')
        answer = await self.bot.wait_for_message(timeout=15, author=user)
        if answer is None:
            await self.bot.say('**Clear canceled.**')
        elif "yes" not in answer.content.lower():
            await self.bot.say('**No action taken.**')
        else:
            for username in db.track.find({}):
                servers = username['servers']
                if server.id in servers.keys():
                    del servers[server.id]
                    db.track.update_one({'username':username['username']}, {'$set': {'servers':servers}})
            await self.bot.say('**Users tracked on `{}` cleared.**'.format(server.name))

    # this needs serious refactoring.. why do i even use a tuple?
    async def _get_options(self, usernames:tuple):
        # option parser, these are default
        options = {"gamemodes": [0], "plays": 50}
        if '-m' in usernames:
            marker_loc = usernames.index('-m')
            # check if nothing after
            if len(usernames) - 1 == marker_loc:
                await self.bot.say("**Please provide a mode!**")
                return (None, usernames)

            modes = usernames[marker_loc + 1]
            if not modes.isdigit():
                await self.bot.say("**Please use only whole numbers for number of top plays!**")
                return (None, usernames)

            modes = list(modes)
            valid_modes = [0,1,2,3]
            final_modes = []
            # parse modes into strings
            for mode in modes:
                if int(mode) in valid_modes:
                    final_modes.append(int(mode))

            if not final_modes:
                await self.bot.say("**Please enter valid modes! e.g. `0123`**")
                return (None, usernames)

            final_modes = set(final_modes)
            options["gamemodes"] = sorted(list(final_modes))
            usernames = list(usernames)
            del usernames[marker_loc + 1]
            del usernames[marker_loc]
            usernames = tuple(usernames)

        if '-t' in usernames:
            marker_loc = usernames.index('-t')
            # check if nothing after
            if len(usernames) - 1 == marker_loc:
                await self.bot.say("**Please provide a number for top plays!**")
                return (None, usernames)

            top_num = usernames[marker_loc + 1]
            if top_num.isdigit():
                top_num = int(top_num)
            else:
                await self.bot.say("**Please provide an integer for top plays!**")
                return (None, usernames)

            if top_num > self.osu_settings['num_track'] or top_num < 1:
                await self.bot.say("**Please provide a valid number of plays! (1-{})**".format(self.osu_settings['num_track']))
                return (None, usernames)

            options["plays"] = top_num
            usernames = list(usernames)
            del usernames[marker_loc + 1]
            del usernames[marker_loc]
            usernames = tuple(usernames)

        if '-c' in usernames:
            if len(options["gamemodes"]) != 1:
                await self.bot.say("**You must specify a single gamemode for country tracking.**")
                return (None, usernames)

            marker_loc = usernames.index('-c')
            # check if nothing after
            if len(usernames) - 1 == marker_loc:
                await self.bot.say("**Please provide a 2-char country code or `global`**")
                return (None, usernames)

            country_code = str(usernames[marker_loc + 1]).upper()
            if len(country_code) != 2 and country_code != 'GLOBAL':
                await self.bot.say("**Please provide a 2-char country code or `global`**")
                return (None, usernames)

            usernames = list(usernames)
            del usernames[marker_loc + 1]
            del usernames[marker_loc]
            usernames = tuple(usernames)

            # default values
            if country_code == 'GLOBAL':
                num_top_players = 50
            else:
                num_top_players = 25

            if '-p' in usernames:
                marker_loc = usernames.index('-p')
                # check if nothing after
                if len(usernames) - 1 == marker_loc:
                    await self.bot.say("**Please provide a number for # of top players!**")
                    return (None, usernames)

                num_top_players = usernames[marker_loc + 1]
                if num_top_players.isdigit():
                    num_top_players = int(num_top_players)
                else:
                    await self.bot.say("**Please provide an integer for # of top players!**")
                    return (None, usernames)

                if (num_top_players > 50 and country_code != 'GLOBAL') or (num_top_players > 100 and country_code == 'GLOBAL') :
                    await self.bot.say("**Please provide a valid number of top players! Global Max: `100`, Country Max: `50`**")
                    return (None, usernames)

                usernames = list(usernames)
                del usernames[marker_loc + 1]
                del usernames[marker_loc]
                usernames = tuple(usernames)

            # append the appropriate user ids
            leaderboard_userids = await get_leaderboard(mode = options["gamemodes"][0], country_code = country_code, limit = num_top_players)
            # new usernames
            if not usernames:
                usernames = []
            else:
                usernames = list(usernames)

            # print(leaderboard_userids, len(leaderboard_userids), country_code, num_top_players, usernames)
            usernames = tuple(leaderboard_userids)
            await self.bot.say("Disclaimer: This is a static list!. Please give owo a moment...")

        return (options, usernames)

    @osutrack.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def remove(self, ctx, *usernames:str):
        """Removes a player to track for top scores."""
        server = ctx.message.server
        channel = ctx.message.channel
        msg = ""
        count_remove = 0

        if usernames == ():
            await self.bot.say("Please enter a user")
            return

        for username in usernames:
            user_find = db.track.find_one({"username":username})
            if user_find and "servers" in user_find and server.id in user_find["servers"]:
                if channel.id == user_find["servers"][server.id]["channel"]:
                    db.track.update_one({"username":username}, {"$unset":{"servers.{}".format(server.id):"channel"}})
                    msg+="**No longer tracking `{}` in `#{}`.**\n".format(username, channel.name)
                    count_remove += 1
                else:
                    msg+="**`{}` is not currently being tracked in `#{}`.**\n".format(username, channel.name)
            else:
                msg+="**`{}` is not currently being tracked.**\n".format(username)

        if len(msg) > 500:
            await self.bot.say("**Removed `{}` users from tracking on `#{}`.**".format(count_remove, channel.name))
        else:
            await self.bot.say(msg)

    @osutrack.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def untrack(self, ctx, *usernames:str):
        """Removes a user from the database."""
        server = ctx.message.server
        channel = ctx.message.channel
        msg = ""
        count_remove = 0

        if answer is None:
            await self.bot.say('**Clear canceled.**')
        elif "yes" not in answer.content.lower():
            await self.bot.say('**No action taken.**')
        else:
            for username in db.track.find({}):
                servers = username['servers']
                if server.id in servers.keys():
                    del servers[server.id]
                    db.track.update_one({'username':username['username']}, {'$set': {'servers':servers}})
            await self.bot.say('**Users tracked on `{}` cleared.**'.format(server.name))

    # ------- play tracker ----------
    async def play_tracker(self):
        # tries to load x new people each time the bot boots up
        global api_counter
        # await self.remove_duplicates()
        # await self.create_suggestion_database()
        cycle = 0
        self.total_requests = await self._count_total_requests()

        while self == self.bot.get_cog('Tracking'):
            api_counter = 0
            total_tracking = db.track.count() # counts total number of players
            requests_per_user = self.total_requests/total_tracking # without recent (hardcoded)
            max_cycles_per_min = self.max_requests/requests_per_user
            self.cycle_time = total_tracking/max_cycles_per_min # minutes
            self.sleep_time = (self.cycle_time * 60) / total_tracking # in seconds
            print("Time Started. Projected Cycle Time: {} Rate: {}".format(str(self.cycle_time), str(self.max_requests)))

            current_time = datetime.datetime.now()
            loop = asyncio.get_event_loop()
            should_cache = False
            for player in db.track.find({}, no_cursor_timeout=True):

                if cycle % 10 == 0:
                    should_cache = True
                    cycle = 0

                loop.create_task(self.player_tracker(player, cache = should_cache))
                await asyncio.sleep(self.sleep_time)

            loop_time = datetime.datetime.now()
            elapsed_time = loop_time - current_time
            rate = api_counter/(elapsed_time.total_seconds()/60)
            print("Time Ended. Cycle Time: {} Rate: {} Requests: {}".format(str(elapsed_time), str(rate), str(api_counter)))

            if self.cycle_time*60 < 60:
                await asyncio.sleep(60 - self.cycle_time*60)
            else:
                pass
            cycle += 1

    async def remove_single_duplicate(self, username:str):
        player_find_count = db.track.find({"username":username}).count()
        if player_find_count == 2:
            db.track.delete_one({"username":username})
            print("Deleted One Instance of {}".format(username))
        elif player_find_count > 2:
            db.track.delete_many({"username":username})
            print("Deleted All Instances of {}".format(username))

    async def remove_duplicates(self):
        for player in db.track.find({}, no_cursor_timeout=True):
            player_find_count = db.track.find({"username":player['username']}).count()
            if player_find_count == 2:
                db.track.delete_one({"username":player['username']})
                print("Deleted One Instance of {}".format(player['username']))
            elif player_find_count > 2:
                db.track.delete_many({"username":player['username']})
                print("Deleted All Instances of {}".format(player['username']))

    async def _count_total_requests(self):
        total_requests = 0

        for player in db.track.find({}, no_cursor_timeout=True):
            max_gamemodes = 0
            for mode in modes:
                all_servers = player['servers'].keys()
                for server_id in all_servers:
                    try:
                        num_gamemodes = len(player['servers'][server_id]['options']['gamemodes'])
                    except:
                        num_gamemodes = 1 # precaution

                    max_gamemodes = max(num_gamemodes, max_gamemodes)
            total_requests += max_gamemodes

        print("There are currently a total of {} requests".format(total_requests))
        return total_requests

    async def _remove_bad_servers(self):
        if self.server_send_fail != [] and len(self.server_send_fail) <= 15: # arbitrary threshold in case discord api fails
            for player in db.track.find({}, no_cursor_timeout=True):
                all_servers = player['servers'].keys()
                for failed_server_id in self.server_send_fail:
                    if failed_server_id in all_servers:
                        del player['servers'][failed_server_id]
                        db.track.update_one({"username":player['username']}, {'$set':{"servers":player['servers']}})
                        find_test = db.track.find_one({"username":player['username']})
                        if failed_server_id in find_test['servers'].keys():
                            log.info("FAILED to delete Server {} from {}".format(failed_server_id, player['username']))
                        else:
                            log.info("Deleted Server {} from {}".format(failed_server_id, player['username']))
            self.server_send_fail = []

    # used to track top plays of specified users (someone please make this better c:)
    # Previous failed attempts include exponential blocking, using a single client session (unreliable),
    # threading/request to update info and then displaying separately, aiohttp to update and then displaying separately
    async def player_tracker(self, player, cache = False):
        key = self.api_keys["osu_api_key"]

        # purge, not implemented
        purge = True

        # get id, either should be the same, but one is backup
        if 'osu_id' in player:
            osu_id = player['osu_id']
        else:
            osu_id = player['userinfo']['osu']['user_id']

        # create last check just in case it doesn't exist
        if 'last_check' not in player:
            print("Creating Last Check for {}".format(player['username']))
            player['last_check'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.track.update_one({"username":player['username']}, {'$set':{"last_check":player['last_check']}})

        # ensures that data is recieved
        got_data = False
        get_data_counter = 1
        new_data = None

        new_data, required_modes = await self._fetch_new(osu_id, player["servers"]) # contains data for player

        # if still no data
        if new_data == None:
            print("Data fetched failed for {}".format(player['username']))
            return

        current_time = datetime.datetime.now()

        for mode in required_modes:

            gamemode_number = get_gamemode_number(mode)
            score_gamemode = get_gamemode_display(mode)
            try:
                best_plays = new_data["best"][mode] # single mode
                recent_play = new_data["recent"][mode] # not used yet

                # print(best_plays)
                best_timestamps = []
                for best_play in best_plays:
                    best_timestamps.append(best_play['date'])
            except:
                continue

            top_play_num_tracker = [] # used for pruning
            for i in range(len(best_timestamps)): # max 100
                last_top = player["last_check"]
                last_top_datetime = datetime.datetime.strptime(last_top, '%Y-%m-%d %H:%M:%S')
                best_datetime = datetime.datetime.strptime(best_timestamps[i], '%Y-%m-%d %H:%M:%S')

                if best_datetime > last_top_datetime: # and (current_time.timetuple().tm_yday - best_datetime.timetuple().tm_yday) <= 1: # could just use string...
                    purge = False # if there was a best, then continue
                    top_play_num = i+1
                    play = best_plays[i]
                    play_map = await get_beatmap(key, self.osu_settings["type"]["default"], play['beatmap_id'])
                    new_user_info = list(await get_user(key, self.osu_settings["type"]["default"], osu_id, gamemode_number, no_cache = True))

                    # ----- put into suggestion database -----
                    if gamemode_number == 0:
                        await self._append_suggestion_database(play)

                    if new_user_info != None and len(new_user_info) > 0 and new_user_info[0]['pp_raw'] != None:
                        new_user_info = new_user_info[0]
                    else:
                        print(player["username"] + "({})".format(osu_id) + " has not played enough.")
                        return

                    # send appropriate message to channel
                    if mode in player["userinfo"]:
                        old_user_info = player["userinfo"][mode]
                        em = await self._create_top_play(top_play_num, play, play_map, old_user_info, new_user_info, score_gamemode)
                    else:
                        old_user_info = None
                        em = await self._create_top_play(top_play_num, play, play_map, old_user_info, new_user_info, score_gamemode)

                    # display it to the player with info
                    all_servers = player['servers'].keys()
                    for server_id in all_servers:
                        try:
                            server = find(lambda m: m.id == server_id, self.bot.servers)
                            server_settings = db.osu_settings.find_one({"server_id": server_id})
                            if server and (not server_settings or "tracking" not in server_settings or server_settings["tracking"] == True):
                                server_player_info = player['servers'][server_id]
                                if 'options' in server_player_info:
                                    plays_option = server_player_info['options']['plays']
                                    gamemodes_option = server_player_info['options']['gamemodes']
                                if 'options' not in server_player_info or i <= plays_option and  gamemode_number in gamemodes_option:
                                    channel = find(lambda m: m.id == player['servers'][server_id]["channel"], server.channels)
                                    await self.bot.send_message(channel, embed = em)
                        except:
                            log.info("Failed to send to server {}".format(server_id))
                            if server_id not in self.server_send_fail:
                                self.server_send_fail.append(server_id)

                    # calculate latency
                    besttime = datetime.datetime.strptime(best_timestamps[i], '%Y-%m-%d %H:%M:%S')
                    oldlastcheck = datetime.datetime.strptime(last_top, '%Y-%m-%d %H:%M:%S')
                    delta = besttime.minute - oldlastcheck.minute

                    log.info("Created top {} {} play for {}({}) | {} {}".format(top_play_num, mode, new_user_info['username'], osu_id, str(besttime), str(oldlastcheck)))

                    # update userinfo for next use
                    player["last_check"] = best_timestamps[i]
                    player['userinfo'][mode] = new_user_info # already non-list

                    # save timestamp for most recent top score... should just go by id..
                    # update username
                    if player['username'] != new_user_info['username']:
                        print("Username updated from {} to {}".format(player['username'], new_user_info['username']))
                        db.track.update_one({"username":player['username']}, {'$set':{"username":new_user_info['username']}})
                        player['username'] = new_user_info['username']

                    # update top plays
                    player['userinfo'][mode] = new_user_info
                    player['userinfo'][mode]['best_plays'] = new_data['best'][mode]
                    db.track.update_one({"username":player['username']}, {'$set':{"userinfo":player['userinfo']}})
                    # db.track.update_one({"username":player['username']}, {'$set':{"userinfo.{}".format(mode):new_user_info}})
                    db.track.update_one({"username":player['username']}, {'$set':{"last_check":best_timestamps[i]}})

            # caching... everything, every 10 cycles... maybe better?
            try:
                if cache and new_data:
                    player['userinfo'][mode]['best_plays'] = new_data['best'][mode]
                    db.track.update_one({"username":player['username']}, {'$set':{"userinfo":player['userinfo']}})
                    # print("{} {} Cached".format(player['username'], mode))
            except:
                pass

            # remove duplicates if necessary
            await self.remove_single_duplicate(player['username'])

    async def _fetch_new(self, osu_id, player_servers):
        key = self.api_keys["osu_api_key"]
        new_data = {"best":{}, "recent":{}}

        required_modes = await self._get_required_modes(player_servers)
        # print(required_modes)

        for mode in required_modes:
            try:
                new_data["best"][mode] = await get_user_best(
                    key, self.osu_settings["type"]["default"], osu_id,
                    get_gamemode_number(mode), self.osu_settings["num_track"], no_cache = True)
                """new_data["recent"][mode] = await get_user_recent(
                    key, self.osu_settings["type"]["default"], osu_id,
                    get_gamemode_number(mode))""" # get recent, ahahahah yeah right.
                new_data["recent"][mode] = {}
            except:
                pass
        return new_data, required_modes


    async def _get_required_modes(self, player_servers):
        required_modes = []
        for server_id in player_servers.keys():
            server_player_info = player_servers[server_id]
            if 'options' in server_player_info:
                required_modes.extend(server_player_info['options']['gamemodes'])
            else: # if no option exists
                required_modes.extend([0])

        required_modes = list(set(required_modes))
        required_modes_txt = []
        for mode_num in required_modes:
            required_modes_txt.append(modes[mode_num])
        return required_modes_txt

    async def _create_top_play(self, top_play_num, play, beatmap, old_user_info, new_user_info, gamemode):
        beatmap_url = 'https://osu.ppy.sh/b/{}'.format(play['beatmap_id'])
        user_url = 'https://{}/u/{}'.format(self.osu_settings["type"]["default"], new_user_info['user_id'])
        profile_url = 'https://a.ppy.sh/{}'.format(new_user_info['user_id'])
        beatmap = beatmap[0]

        # get infomation
        m0, s0 = divmod(int(beatmap['total_length']), 60)
        mods = num_to_mod(play['enabled_mods'])
        em = discord.Embed(description='', colour=0xffa500)
        acc = calculate_acc(play, int(beatmap['mode']))

        # determine mods
        if not mods:
            mods = []
            mods.append('No Mod')
            oppai_output = None
        else:
            oppai_mods = "+{}".format("".join(mods))
            oppai_output = await get_pyoppai(beatmap['beatmap_id'], accs=[int(acc)], mods = int(play['enabled_mods']))

        # grab beatmap image
        soup = await get_web(beatmap_url)
        map_image = [x['src'] for x in soup.findAll('img', {'class': 'bmt'})]
        map_image_url = 'http:{}'.format(map_image[0])
        em.set_thumbnail(url=map_image_url)
        em.set_author(name="New #{} for {} in {}".format(top_play_num, new_user_info['username'], gamemode), icon_url = profile_url, url = user_url)

        info = ""
        map_title = "{} [{}]".format(beatmap['title'], beatmap['version'])
        map_rank = None
        map_rank = await self.get_map_rank(new_user_info['user_id'], map_title)
        # print(map_rank) # just for debugging
        map_rank_str = ''
        if map_rank:
            map_rank_str = '▸ #{}'.format(str(map_rank))

        info += "▸ [**__{}__**]({}) {}                            \n".format(map_title, beatmap_url, map_rank_str)
        # calculate bpm and time... MUST clean up.
        if oppai_output and ('DT' in str(mods).upper() or 'HT' in str(mods).upper()):
            if 'DT' in str(mods):
                m1,s1,bpm1 = calc_time(beatmap['total_length'], beatmap['bpm'], 1.5)
            elif 'HT' in str(mods):
                m1,s1,bpm1 = calc_time(beatmap['total_length'], beatmap['bpm'], 2/3)

            star_str, _ = compare_val(beatmap['difficultyrating'], oppai_output, 'stars', dec_places = 2)
            info += "▸ **{}★** ▸ {}:{}({}:{}) ▸ {}({})bpm\n".format(
                star_str,
                m0, str(s0).zfill(2),
                m1, str(s1).zfill(2),
                beatmap['bpm'], bpm1)
        elif 'DT' in str(mods).upper() or 'HT' in str(mods).upper():
            if 'DT' in str(mods):
                m1,s1,bpm1 = calc_time(beatmap['total_length'], beatmap['bpm'], 1.5)
            elif 'HT' in str(mods):
                m1,s1,bpm1 = calc_time(beatmap['total_length'], beatmap['bpm'], 2/3)

            star_str, _ = compare_val(beatmap['difficultyrating'], oppai_output, 'stars', dec_places = 2)
            info += "▸ **{}★** ▸ {}:{}({}:{}) ▸ {}({})bpm\n".format(
                star_str,
                m0, str(s0).zfill(2),
                m1, str(s1).zfill(2),
                beatmap['bpm'], bpm1)
        else:
            stars_str, _ = compare_val(beatmap['difficultyrating'], oppai_output, 'stars', dec_places = 2)
            info += "▸ **{}★** ▸ {}:{} ▸ {}bpm\n".format(
                stars_str, m0, str(s0).zfill(2), beatmap['bpm'])
        try:
            if old_user_info != None:
                dpp = float(new_user_info['pp_raw']) - float(old_user_info['pp_raw'])
                if dpp == 0:
                    pp_gain = ""
                else:
                    pp_gain = "({:+.2f})".format(dpp)
                info += "▸ +{} ▸ **{:.2f}%** ▸ **{}** Rank ▸ **{:.2f} {}pp**\n".format(fix_mods(''.join(mods)),
                    float(acc), play['rank'], float(play['pp']), pp_gain)
                info += "▸ {} ▸ x{}/{} ▸ [{}/{}/{}/{}]\n".format(
                    play['score'], play['maxcombo'], beatmap['max_combo'],
                    play['count300'],play['count100'],play['count50'],play['countmiss'])
                info += "▸ #{} → #{} ({}#{} → #{})".format(
                    old_user_info['pp_rank'], new_user_info['pp_rank'],
                    new_user_info['country'],
                    old_user_info['pp_country_rank'], new_user_info['pp_country_rank'])
            else: # if first time playing
                info += "▸ +{} ▸ **{:.2f}%** ▸ **{}** Rank ▸ **{:.2f}pp**\n".format(
                    fix_mods(''.join(mods)), float(acc), play['rank'], float(play['pp']))
                info += "▸ {} ▸ x{}/{} ▸ [{}/{}/{}/{}]\n".format(
                    play['score'], play['maxcombo'], beatmap['max_combo'],
                    play['count300'],play['count100'],play['count50'],play['countmiss'])
                info += "▸ #{} ({}#{})".format(
                    new_user_info['pp_rank'],
                    new_user_info['country'],
                    new_user_info['pp_country_rank'])
        except:
            info += "Error"
        em.description = info

        time_ago_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=8) - datetime.datetime.strptime(play['date'], '%Y-%m-%d %H:%M:%S')
        self.latency.append(int(time_ago_datetime.total_seconds())) # keep track of how long it took
        await self.save_latency()

        timeago = time_ago(
            datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            datetime.datetime.strptime(play['date'], '%Y-%m-%d %H:%M:%S'))
        em.set_footer(text = "{}Ago On osu! Official Server".format(timeago))
        return em

    # gets user map rank if less than 1000
    async def get_map_rank(self, osu_userid, title):
        try:
            ret = None
            url = 'https://osu.ppy.sh/users/{}'.format(osu_userid)
            soup = await get_web(url, parser = "lxml")
            find = soup.find('script',{"id": "json-user"})
            user = json.loads(find.get_text())

            for recent_play in user['recentActivities']:
                if title in recent_play['beatmap']['title']:
                    ret = int(recent_play['rank'])
                    break
            return ret
        except:
            return None

    # one_time, very beta (meirl)
    async def create_suggestion_database(self):
        self.total_requests = await self._count_total_requests()
        print("Appending Suggestion Database.")
        total_tracking = db.track.count() # around 1700 for owo
        requests_per_user = self.total_requests/total_tracking # without recent (hardcoded)
        max_cycles_per_min = self.max_requests/requests_per_user
        self.cycle_time = total_tracking/max_cycles_per_min # minutes
        self.sleep_time = (self.cycle_time * 60) / total_tracking # in seconds
        print('Sleep per user: ', self.sleep_time)

        current_time = datetime.datetime.now()
        loop = asyncio.get_event_loop()
        counter = 0
        bound_size = 0 # EDIT THIS VALUE
        start_index = randint(0, total_tracking - bound_size - 1)
        end_index = start_index + bound_size
        # force_list = ['124493', '4787150', '2558286', '1419095', '2614511', '2831793', '2003326','227717'] # EDIT THESE LISTS
        # force_list = ['1205412', '941094', '64501'] # ez/fl players
        # force_list = ['147515'] # random
        force_list = [] # empty
        for player in db.track.find({}, no_cursor_timeout=True):
            if 'osu_id' in player:
                osu_id = player['osu_id']
            else:
                osu_id = player['userinfo']['osu']['user_id']
            if (counter > start_index and counter <= end_index) or osu_id in force_list:
                loop.create_task(self.suggestion_play_parser(player))
                # await asyncio.sleep(self.sleep_time)
            counter += 1

        loop_time = datetime.datetime.now()
        elapsed_time = loop_time - current_time
        print("Time ended: " + str(elapsed_time))
        print("Suggestion Database Creation ENDED!!!. Took: {}".format(str(elapsed_time)))

    async def _append_suggestion_database(self, play):
        # calculate the pp for the beatmap
        accs = [100] # based on 100% acc
        mods_list = num_to_mod(play['enabled_mods']) # list
        oppai_output = await get_pyoppai(play['beatmap_id'], accs=accs, mods = int(play['enabled_mods']))
        if not oppai_output:
            return

        pp_100 = float(oppai_output['pp'][0])
        pp_range = determine_pp_range(pp_100)
        # create structure...
        section = db.suggest_osu.find_one({'pp_range':pp_range})
        if not section:
            """
            new_play = self._new_database_entry(play, oppai_output, mods_list)
            new_range = {'pp_range':pp_range, 'beatmaps': [new_play]}
            db.suggest_std.insert_one(new_range)
            """
            new_range = {'pp_range':pp_range, 'beatmaps': [(play['beatmap_id'], mods_list)]}
            db.suggest_osu.insert_one(new_range)
        else:
            for temp_beatmap, temp_mods in section['beatmaps']:
                if temp_beatmap == play['beatmap_id'] and temp_mods == mods_list:
                    return
            """
            new_play = self._new_database_entry(play, oppai_output, mods_list)
            section['beatmaps'].append(new_play)
            db.suggest_std.update_one({'pp_range':pp_range}, {'$set':{"beatmaps":section['beatmaps']}})
            """
            section['beatmaps'].append((play['beatmap_id'], mods_list))
            db.suggest_osu.update_one({'pp_range':pp_range}, {'$set':{"beatmaps":section['beatmaps']}})
        print("New {}, beatmap_id: {} mods: {}".format(pp_range, play['beatmap_id'], str(mods_list)))

    async def update_leaderboard():
        current_user_ids = [user['id'] for user in user_list]
        new_list = await get_leaderboard(mode = gamemode, country_code = country_code)
        sym_diff = set(current_user_ids).symmetric_difference(set(new_list))

        # replace only what's necessary
        for ids in sym_diff:
            # remove indices !!!!!!!!!!!!11
            pass

### ----------------------- Helper Functions used by both classes -----------------------

# because you people just won't stop bothering me about it
def fix_mods(mods:str):
    if mods == 'PFSOFLNCHTRXDTSDHRHDEZNF':
        return '? KEY'
    else:
        return mods.replace('DTHRHD', 'HDHRDT').replace('DTHD','HDDT').replace('HRHD', 'HDHR')

def get_gamemode(gamemode:int):
    if gamemode == 1:
        gamemode_text = "Taiko"
    elif gamemode == 2:
        gamemode_text = "Catch the Beat!"
    elif gamemode == 3:
        gamemode_text = "osu! Mania"
    else:
        gamemode_text = "osu! Standard"
    return gamemode_text

def get_gamemode_display(gamemode):
    if gamemode == "osu":
        gamemode_text = "osu! Standard"
    elif gamemode == "ctb":
        gamemode_text = "Catch the Beat!"
    elif gamemode == "mania":
        gamemode_text = "osu! Mania"
    elif gamemode == "taiko":
        gamemode_text = "Taiko"
    return gamemode_text

def get_gamemode_number(gamemode:str):
    if gamemode == "taiko":
        gamemode_text = 1
    elif gamemode == "ctb":
        gamemode_text = 2
    elif gamemode == "mania":
        gamemode_text = 3
    else:
        gamemode_text = 0
    return int(gamemode_text)

def calculate_acc(beatmap, gamemode:int):
    if gamemode == 0:
        total_unscale_score = float(beatmap['count300'])
        total_unscale_score += float(beatmap['count100'])
        total_unscale_score += float(beatmap['count50'])
        total_unscale_score += float(beatmap['countmiss'])
        total_unscale_score *=300
        user_score = float(beatmap['count300']) * 300.0
        user_score += float(beatmap['count100']) * 100.0
        user_score += float(beatmap['count50']) * 50.0
    elif gamemode == 1:
        total_unscale_score = float(beatmap['count300'])
        total_unscale_score += float(beatmap['count100'])
        total_unscale_score += float(beatmap['countmiss'])
        total_unscale_score *= 300
        user_score = float(beatmap['count300']) * 1.0
        user_score += float(beatmap['count100']) * 0.5
        user_score *= 300
    elif gamemode == 2:
        total_unscale_score = float(beatmap['count300'])
        total_unscale_score += float(beatmap['count100'])
        total_unscale_score += float(beatmap['count50'])
        total_unscale_score += float(beatmap['countmiss'])
        total_unscale_score += float(beatmap['countkatu'])
        user_score = float(beatmap['count300'])
        user_score += float(beatmap['count100'])
        user_score  += float(beatmap['count50'])
    elif gamemode == 3:
        total_unscale_score = float(beatmap['count300'])
        total_unscale_score += float(beatmap['countgeki'])
        total_unscale_score += float(beatmap['countkatu'])
        total_unscale_score += float(beatmap['count100'])
        total_unscale_score += float(beatmap['count50'])
        total_unscale_score += float(beatmap['countmiss'])
        total_unscale_score *=300
        user_score = float(beatmap['count300']) * 300.0
        user_score += float(beatmap['countgeki']) * 300.0
        user_score += float(beatmap['countkatu']) * 200.0
        user_score += float(beatmap['count100']) * 100.0
        user_score += float(beatmap['count50']) * 50.0

    return (float(user_score)/float(total_unscale_score)) * 100.0

def no_choke_acc(beatmap, gamemode:int):
    if gamemode == 0:
        total_unscale_score = float(beatmap['count300'])
        total_unscale_score += float(beatmap['count100'])
        total_unscale_score += float(beatmap['count50'])
        total_unscale_score += float(beatmap['countmiss'])
        total_unscale_score *=300
        user_score = float(beatmap['count300']) * 300.0
        user_score += (float(beatmap['count100']) + float(beatmap['countmiss'])) * 100.0
        user_score += float(beatmap['count50']) * 50.0
    elif gamemode == 1:
        total_unscale_score = float(beatmap['count300'])
        total_unscale_score += float(beatmap['count100'])
        total_unscale_score += float(beatmap['countmiss'])
        total_unscale_score *= 300
        user_score = float(beatmap['count300']) * 1.0
        user_score += (float(beatmap['count100']) + float(beatmap['countmiss'])) * 0.5
        user_score *= 300
    elif gamemode == 2:
        total_unscale_score = float(beatmap['count300'])
        total_unscale_score += float(beatmap['count100'])
        total_unscale_score += float(beatmap['count50'])
        total_unscale_score += float(beatmap['countmiss'])
        total_unscale_score += float(beatmap['countkatu'])
        user_score = float(beatmap['count300'])
        user_score += (float(beatmap['count100']) + float(beatmap['countmiss']))
        user_score  += float(beatmap['count50'])
    elif gamemode == 3:
        total_unscale_score = float(beatmap['count300'])
        total_unscale_score += float(beatmap['countgeki'])
        total_unscale_score += float(beatmap['countkatu'])
        total_unscale_score += float(beatmap['count100'])
        total_unscale_score += float(beatmap['count50'])
        total_unscale_score += float(beatmap['countmiss'])
        total_unscale_score *=300
        user_score = float(beatmap['count300']) * 300.0
        user_score += float(beatmap['countgeki']) * 300.0
        user_score += float(beatmap['countkatu']) * 200.0
        user_score += (float(beatmap['count100']) + float(beatmap['countmiss'])) * 100.0
        user_score += float(beatmap['count50']) * 50.0

    return (float(user_score)/float(total_unscale_score)) * 100.0

# gives a list of the ranked mods given a peppy number lol
def num_to_mod(number):
    """This is the way pyttanko does it.
    Just as an actual bitwise instead of list.
    Deal with it."""
    number = int(number)
    mod_list = []

    if number & 1<<0:   mod_list.append('NF')
    if number & 1<<1:   mod_list.append('EZ')
    if number & 1<<3:   mod_list.append('HD')
    if number & 1<<4:   mod_list.append('HR')
    if number & 1<<5:   mod_list.append('SD')
    if number & 1<<9:   mod_list.append('NC')
    elif number & 1<<6: mod_list.append('DT')
    if number & 1<<7:   mod_list.append('RX')
    if number & 1<<8:   mod_list.append('HT')
    if number & 1<<10:  mod_list.append('FL')
    if number & 1<<12:  mod_list.append('SO')
    if number & 1<<14:  mod_list.append('PF')
    if number & 1<<15:  mod_list.append('4 KEY')
    if number & 1<<16:  mod_list.append('5 KEY')
    if number & 1<<17:  mod_list.append('6 KEY')
    if number & 1<<18:  mod_list.append('7 KEY')
    if number & 1<<19:  mod_list.append('8 KEY')
    if number & 1<<20:  mod_list.append('FI')
    if number & 1<<24:  mod_list.append('9 KEY')
    if number & 1<<25:  mod_list.append('10 KEY')
    if number & 1<<26:  mod_list.append('1 KEY')
    if number & 1<<27:  mod_list.append('3 KEY')
    if number & 1<<28:  mod_list.append('2 KEY')

    return mod_list

def mod_to_num(mods:str):
    """It works."""
    mods = mods.upper()
    total = 0

    if 'NF' in mods:    total += 1<<0
    if 'EZ' in mods:    total += 1<<1
    if 'HD' in mods:    total += 1<<3
    if 'HR' in mods:    total += 1<<4
    if 'SD' in mods:    total += 1<<5
    if 'DT' in mods:    total += 1<<6
    if 'RX' in mods:    total += 1<<7
    if 'HT' in mods:    total += 1<<8
    if 'NC' in mods:    total += 1<<9
    if 'FL' in mods:    total += 1<<10
    if 'SO' in mods:    total += 1<<12
    if 'PF' in mods:    total += 1<<14
    if '4 KEY' in mods: total += 1<<15
    if '5 KEY' in mods: total += 1<<16
    if '6 KEY' in mods: total += 1<<17
    if '7 KEY' in mods: total += 1<<18
    if '8 KEY' in mods: total += 1<<19
    if 'FI' in mods:    total += 1<<20
    if '9 KEY' in mods: total += 1<<24
    if '10 KEY'in mods: total += 1<<25
    if '1 KEY' in mods: total += 1<<26
    if '3 KEY' in mods: total += 1<<27
    if '2 KEY' in mods: total += 1<<28

    return int(total)

def get_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def compare_val(map_stat, omap, param, dec_places:int = 1, single = False):
    if not omap:
        if dec_places == 0:
            return "{}".format(int(float(map_stat))), int(float(map_stat))
        return "{}".format(round(float(map_stat), dec_places)), round(float(map_stat), dec_places)
    elif omap and not map_stat:
        if dec_places == 0:
            return "{}".format(int(float(omap[param]))), int(float(omap[param]))
        return "{}".format(round(float(omap[param]), dec_places)), round(float(omap[param]), dec_places)
    else:
        map_stat = float(map_stat)
        op_stat = float(omap[param])
        if int(round(op_stat, dec_places)) != 0 and abs(round(map_stat, dec_places) - round(op_stat, dec_places)) > 0.05:
            if single:
                if dec_places == 0:
                    return "{}".format(int(float(op_stat))), int(float(op_stat))
                return "{}".format(round(op_stat, dec_places)), round(op_stat, dec_places)
            else:
                if dec_places == 0:
                    return "{}({})".format(int(float(map_stat)), int(float(op_stat))), int(float(op_stat))
                return "{}({})".format(round(map_stat, dec_places),
                    round(op_stat, dec_places)), round(op_stat, dec_places)
        else:
            if dec_places == 0:
                return "{}".format(int(float(map_stat))), int(float(map_stat))
            return "{}".format(round(map_stat, dec_places)), round(map_stat, dec_places)

def determine_pp_range(pp, range_of_pp = 30):
    nearest_range = int(range_of_pp * round(float(pp)/range_of_pp))

    upper_bound = 0
    lower_bound = 0
    if (nearest_range - pp) > 0:
        lower_bound = nearest_range - range_of_pp
        upper_bound = nearest_range - 1
    else:
        lower_bound = nearest_range
        upper_bound = nearest_range + range_of_pp - 1

    return "{}_{}".format(lower_bound, upper_bound)

def calc_time(total_sec, bpm, factor:float=1):
    m1, s1 = divmod(round(float(total_sec)/factor), 60)
    bpm1 = round(factor*float(bpm), 1)
    return (m1,s1,bpm1)

def time_ago(time1, time2):
    time_diff = time1 - time2
    timeago = datetime.datetime(1,1,1) + time_diff
    time_limit = 0
    time_ago = ""
    if timeago.year-1 != 0:
        time_ago += "{} Year{} ".format(timeago.year-1, determine_plural(timeago.year-1))
        time_limit = time_limit + 1
    if timeago.month-1 !=0:
        time_ago += "{} Month{} ".format(timeago.month-1, determine_plural(timeago.month-1))
        time_limit = time_limit + 1
    if timeago.day-1 !=0 and not time_limit == 2:
        time_ago += "{} Day{} ".format(timeago.day-1, determine_plural(timeago.day-1))
        time_limit = time_limit + 1
    if timeago.hour != 0 and not time_limit == 2:
        time_ago += "{} Hour{} ".format(timeago.hour, determine_plural(timeago.hour))
        time_limit = time_limit + 1
    if timeago.minute != 0 and not time_limit == 2:
        time_ago += "{} Minute{} ".format(timeago.minute, determine_plural(timeago.minute))
        time_limit = time_limit + 1
    if not time_limit == 2:
        time_ago += "{} Second{} ".format(timeago.second, determine_plural(timeago.second))
    return time_ago

# really stevy? yes, really.
def determine_plural(number):
    if int(number) != 1:
        return 's'
    else:
        return ''
###------------------------- Fetching Data -------------------------

async def get_leaderboard(mode = 0, country_code = None, limit = 50):
    users_per_page = 50
    pages = round(limit/50 + .5)
    urls = []
    player_id_list = []
    for i in range(pages):
        country = ''
        if country_code is not None and country_code != 'GLOBAL':
            country = 'country={}&'.format(str(country_code).upper())
        url = 'https://osu.ppy.sh/rankings/{}/performance?{}page={}#jump-target'.format(modes2[mode], country, i+1)

        soup = await get_web(url)
        span_tags = list(soup.findAll('span'))

        for tag in span_tags:
            try:
                if tag['data-user-id']:
                    # username tag.text.replace('\n','')
                    player_id_list.append(tag['data-user-id'])
            except:
                pass

    return player_id_list[:limit]

async def get_top_cc(pages = 1):
    """Get country codes for top 50"""
    target_base = 'https://osu.ppy.sh/rankings/osu/performance?country='

    for i in range(pages):
        url = 'https://osu.ppy.sh/rankings/osu/country?page={}#jump-target'.format(i)
        soup = await get_web(url)
        a_tags = list(soup.findAll('a'))

        cc = []
        for tag in a_tags:
            try:
                if target_base in tag['href']:
                    # username tag.text.replace('\n','')
                    cc.append(tag['href'].replace(target_base, '').upper())
            except:
                pass

    print(cc)
    return cc

# returns an osu-related url from google
async def get_google_search(search_terms:str, include_title = False):
    search_limit = 10
    option = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

    regex = [
            re.compile(",\"ou\":\"([^`]*?)\""),
            re.compile("<h3 class=\"r\"><a href=\"\/url\?url=([^`]*?)&amp;"),
            re.compile("<h3 class=\"r\"><a href=\"([^`]*?)\""),
            re.compile("\/url?url=")
        ]

    url = "https://www.google.com/search?hl=en&q="
    encode = urllib.parse.quote_plus(search_terms, encoding='utf-8',
                                     errors='replace')
    uir = url + encode
    async with aiohttp.request('GET', uir, headers=option) as resp:
        test = str(await resp.content.read())
        query_find = regex[1].findall(test)
        if not query_find:
            query_find = regex[2].findall(test)
            try:
                query_find = query_find[:search_limit]
            except IndexError:
                return []
        elif regex[3].search(query_find[0]):
            query_find = query_find[:search_limit]
        else:
            query_find = query_find[:search_limit]

    final_list = []
    for link in query_find:
        if 'osu.ppy.sh/' in link:
            final_list.append(link)

    return final_list

async def get_web(url, parser = 'html.parser'):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.read()

            return BeautifulSoup(text.decode('utf-8'), parser)

# Gets the beatmap
async def get_beatmap(key, api:str, beatmap_id, session = None, no_cache = False):
    if not no_cache:
        beatmap = await get_beatmap_db(beatmap_id)
        if beatmap:
            return beatmap

    url_params = []
    url_params.append(parameterize_key(key))
    url_params.append(parameterize_id("b", beatmap_id))
    url = build_request(url_params, "https://{}/api/get_beatmaps?".format(api))
    beatmap = await fetch(url, session)
    await cache_beatmap(beatmap)
    return beatmap

# Gets the beatmap set
async def get_beatmapset(key, api:str, set_id, session = None):
    url_params = []
    url_params.append(parameterize_key(key))
    url_params.append(parameterize_id("s", set_id))
    url = build_request(url_params, "https://{}/api/get_beatmaps?".format(api))
    return await fetch(url, session)

# Grabs the scores
async def get_scores(key, api:str, beatmap_id, user_id, mode, session = None):
    url_params = []
    url_params.append(parameterize_key(key))
    url_params.append(parameterize_id("b", beatmap_id))
    url_params.append(parameterize_id("u", user_id))
    url_params.append(parameterize_mode(mode))
    url = build_request(url_params, "https://{}/api/get_scores?".format(api))
    return await fetch(url, session)

async def get_user(key, api:str, user_id, mode, session = None, no_cache = False):
    if not no_cache:
        userinfo = await get_user_db(user_id, mode)
        if userinfo:
            return userinfo

    url_params = []
    url_params.append(parameterize_key(key))
    url_params.append(parameterize_id("u", user_id))
    url_params.append(parameterize_mode(mode))
    url = build_request(url_params, "https://{}/api/get_user?".format(api))
    return await fetch(url, session)

async def get_user_best(key, api:str, user_id, mode, limit, session = None, no_cache = False):
    if not no_cache:
        userbest = await get_user_best_db(user_id, mode, limit)
        if userbest:
            return userbest

    url_params = []
    url_params.append(parameterize_key(key))
    url_params.append(parameterize_id("u", user_id))
    url_params.append(parameterize_mode(mode))
    url_params.append(parameterize_limit(limit))

    url = build_request(url_params, "https://{}/api/get_user_best?".format(api))
    return await fetch(url, session)

# Returns the user's ten most recent plays.
async def get_user_recent(key, api:str, user_id, mode, session = None):
    url_params = []

    url_params.append(parameterize_key(key))
    url_params.append(parameterize_id("u", user_id))
    url_params.append(parameterize_mode(mode))
    url = build_request(url_params, "https://{}/api/get_user_recent?".format(api))
    return await fetch(url, session)

async def fetch(url, session):
    global api_counter
    counter = 0
    while (counter < 5):
        try:
            api_counter += 1
            if session == None:
                async with aiohttp.get(url) as resp:
                    return await resp.json()
            else:
                async with session.get(url) as resp:
                    return await resp.json()
        except:
            counter += 1
            await asyncio.sleep(0.06)

    print("Fetch Failed")
    return None

async def get_beatmap_db(beatmap_id):
    beatmap_id_list = db.beatmap_cache.find_one({'type': 'list'})
    if beatmap_id_list:
        beatmap_id_list = beatmap_id_list['ids']

        if beatmap_id in beatmap_id_list:
            index = beatmap_id_list.index(beatmap_id)
            beatmap_cache = db.beatmap_cache.find_one({'type': 'maps'})
            beatmap_cache = beatmap_cache['maps']
            beatmap = beatmap_cache[index]
            print('Using cached info for {}'.format(beatmap['beatmap_id']))
            return [beatmap]

    return None

async def get_user_db(user_id, mode):
    cached_info_userid = db.track.find_one({'osu_id':user_id})
    cached_info_username = db.track.find_one({'username':user_id})
    for cache_type, data in [('ID', cached_info_userid), ('USERNAME', cached_info_username)]:
        if data:
            try:
                print('{} Using cached info for {}'.format(cache_type, user_id))
                return [data['userinfo'][modes[mode]]]
            except:
                print('Cached data for {} does not exist yet!'.format(user_id))

    return None

async def get_user_best_db(user_id, mode, limit):
    try:
        cached_info_userid = db.track.find_one({'osu_id':user_id})
        cached_info_username = db.track.find_one({'username':user_id})
        for cache_type, data in [('ID', cached_info_userid), ('USERNAME', cached_info_username)]:
            if data:
                print('{} Using cached info for {}'.format(cache_type, user_id))
                return data['userinfo'][modes[mode]]['best_plays'][:limit]
    except:
        print('Cached data for {} does not exist yet!'.format(user_id))
        return None

async def cache_beatmap(beatmaps):
    cache_maxlen = 1000

    for beatmap in beatmaps:
        # cache only ranked, approved
        if int(beatmap['approved']) in [1,2,4]:
            beatmap_id_list = db.beatmap_cache.find_one({'type': 'list'})
            if not beatmap_id_list:
                new_list = {'type': 'list', 'ids': []}
                db.beatmap_cache.insert_one(new_list)

            beatmap_id_list = db.beatmap_cache.find_one({'type': 'maps'})
            if not beatmap_id_list:
                new_list = {'type': 'maps', 'maps': []}
                db.beatmap_cache.insert_one(new_list)

            beatmap_id_list = db.beatmap_cache.find_one({'type': 'list'})
            beatmap_id_list = collections.deque(beatmap_id_list['ids'], maxlen = cache_maxlen)

            if beatmap['beatmap_id'] not in beatmap_id_list:
                beatmap_map_list = db.beatmap_cache.find_one({'type': 'maps'})
                beatmap_map_list = collections.deque(beatmap_map_list['maps'], maxlen = cache_maxlen)

                # append new beatmap id
                beatmap_id_list.append(beatmap['beatmap_id'])
                # append new beatmap
                beatmap_map_list.append(beatmap)

                db.beatmap_cache.update_one({"type":'list'}, {'$set':{
                    'ids': list(beatmap_id_list)
                }})

                db.beatmap_cache.update_one({"type":'maps'}, {'$set':{
                    'maps': list(beatmap_map_list)
                }})

                print('Beatmap {} Cached'.format(beatmap['beatmap_id']))

# Written by Jams
async def get_pyoppai(map_id:str, accs=[100], mods=0, misses=0, combo=None, completion=None, fc=None, plot = False, imgur = None):
    url = 'https://osu.ppy.sh/osu/{}'.format(map_id)

    # try:
    ctx = pyoppai.new_ctx()
    b = pyoppai.new_beatmap(ctx)

    BUFSIZE = 2000000
    buf = pyoppai.new_buffer(BUFSIZE)

    file_path = 'data/osu/temp/{}.osu'.format(map_id) # some unique filepath
    await download_file(url, file_path) # this is the file name that it downloaded
    pyoppai.parse(file_path, b, buf, BUFSIZE, True, 'data/osu/cache/')
    dctx = pyoppai.new_d_calc_ctx(ctx)
    pyoppai.apply_mods(b, mods)

    stars, aim, speed, _, _, _, _ = pyoppai.d_calc(dctx, b)
    cs, od, ar, hp = pyoppai.stats(b)

    if not combo:
        combo = pyoppai.max_combo(b)

    total_pp_list = []
    aim_pp_list = []
    speed_pp_list = []
    acc_pp_list = []

    for acc in accs:
        accurracy, pp, aim_pp, speed_pp, acc_pp = pyoppai.pp_calc_acc(ctx, aim, speed, b, acc, mods, combo, misses)
        total_pp_list.append(pp)
        aim_pp_list.append(aim_pp)
        speed_pp_list.append(speed_pp)
        acc_pp_list.append(acc_pp)

    if fc:
        _, fc_pp, _, _, _ = pyoppai.pp_calc_acc(ctx, aim, speed, b, fc, mods, pyoppai.max_combo(b), 0)
        total_pp_list.append(fc_pp)

    pyoppai_json = {
        'version': pyoppai.version(b),
        'title': pyoppai.title(b),
        'artist': pyoppai.artist(b),
        'creator': pyoppai.creator(b),
        'combo': combo,
        'misses': misses,
        'max_combo': pyoppai.max_combo(b),
        'mode': pyoppai.mode(b),
        'num_objects': pyoppai.num_objects(b),
        'num_circles': pyoppai.num_circles(b),
        'num_sliders': pyoppai.num_sliders(b),
        'num_spinners': pyoppai.num_spinners(b),
        'stars': stars,
        'aim_stars': aim,
        'speed_stars': speed,
        'pp': total_pp_list, # list
        'aim_pp': aim_pp_list,
        'speed_pp': speed_pp_list,
        'acc_pp': acc_pp_list,
        'acc': accs, # list
        'cs': cs,
        'od': od,
        'ar': ar,
        'hp': hp
        }

    if completion:
        try:
            pyoppai_json['map_completion'] = await _map_completion(file_path, int(completion))
        except:
            pass

    if plot:
        pyoppai_json['graph_url'] = await plot_map_stars(file_path, mods, imgur)
        # print(pyoppai_json['graph_url'])

    os.remove(file_path)
    return pyoppai_json
    #except:
        #return None

async def _get_taiko_pp(stars:float, od:float, max_combo:int, accs = [100], misses = 0, mods = []):
    od = float(od)
    stars = float(stars)
    max_combo = int(max_combo)

    strain_value = ((max(1, float(stars)/0.0075) * 5 - 4)**2)/100000
    user_combo = max_combo - misses
    length_bonus = min(1, max_combo/1500) * 0.1 + 1
    strain_value *= length_bonus
    strain_value *= 0.985**misses
    strain_value *= min(user_combo**0.5 / max_combo**0.5, 1)

    # scaling values for some mods
    if "EZ" in mods:
        od /= 2
    if "HR" in mods:
        od *= 1.4
    od = max(min(od, 10), 0)
    max_val = 20
    min_val = 50
    result = min_val + (max_val - min_val) * od / 10
    result = math.floor(result) - 0.5
    if "HT" in mods:
        result /= 0.75
    if "DT" in mods:
        result /= 1.5
    od = round(result * 100) / 100

    pp_values = []
    for acc in accs:
        acc_strainValue = strain_value*(acc/100)

        acc_value = (150/od)**1.1 * ((acc/100)**15) * 22
        acc_value *= min((max_combo/1500)**0.3, 1.15)

        mod_multiplier = 1.10
        if "HD" in mods:
            mod_multiplier *= 1.10
            acc_strainValue *= 1.025
        if "SO" in mods:
            mod_multiplier *= 0.95
        if "NF" in mods:
            mod_multiplier *= 0.90
        if "FL" in mods:
            acc_strainValue *= 1.05 * length_bonus

        total_value = (acc_strainValue**1.1 + acc_value**1.1)**(1.0/1.1) * mod_multiplier
        pp_values.append(round(total_value*100)/100)

    return pp_values

async def _get_mania_pp(stars:float, od:float, max_combo:int, score = None, accs = [100], mods = []):
    stars = float(stars)
    od = float(od)
    max_combo = int(max_combo)

    # score multiplier
    scoreMultiplier = 1
    od_multiplier = 1
    if "EZ" in mods:
        scoreMultiplier *= 0.5
        od_multiplier = 0.5
    if "NF" in mods:
        scoreMultiplier *= 0.5
    if "HT" in mods:
        scoreMultiplier *= 0.5

    # mod multiplier
    modMultiplier = 1.10
    if "NF" in mods:
        modMultiplier *= 0.90
    if "SO" in mods:
        modMultiplier *= 0.95
    if "EZ" in mods:
        modMultiplier *= 0.50

    od *= od_multiplier

    # for each acc
    pp_values = []
    for acc in accs:
        # print(max_combo, acc)
        if score is None:
            score = 1000000 * (acc/100)

        score *= scoreMultiplier

        # compute strain
        if scoreMultiplier <= 0:
            strainValue = 0
            return
        score *= (1 / scoreMultiplier)

        # star scaling
        star_scaling_factor = 0.018
        # print(stars, star_scaling_factor)
        starRate = float(stars) * star_scaling_factor
        strainValue = (((5 * max(1, starRate / 0.0825) - 4) ** 3) / 110000) * (1 + 0.1 * min(1, max_combo / 1500))

        # accValue computation
        hitWindow300 = 34 + 3 * min(10, max(0, 10.0 - float(od)))
        if hitWindow300 <= 0:
            accValue = 0
        else:
            accValue = (((150 / hitWindow300) * ((acc/100)**16))**1.8) * 2.5 * (min(1.15, ((max_combo / 1500)**0.3)))

        if score <= 500000:
            strainValue *= ((score / 500000) * 0.1)
        elif score <= 600000:
            strainValue *= (0.1 + (score - 500000) / 100000 * 0.2)
        elif score <= 700000:
            strainValue *= (0.3 + (score - 600000) / 100000 * 0.35)
        elif score <= 800000:
            strainValue *= (0.65 + (score - 700000) / 100000 * 0.20)
        elif score <= 900000:
            strainValue *=  (0.85 + (score - 800000) / 100000 * 0.1)
        else:
            strainValue *=  (0.95 + (score - 900000) / 100000 * 0.05)

        pp_values.append((((strainValue**1.1) + (accValue** 1.1))** (1 / 1.1)) * modMultiplier)

    return pp_values

async def _get_ctb_pp(stars, ar, max_combo, player_combo = None, accs = [100], misses = 0, mods = []):
    # requires accurate stars for particular mod DT/HT/HR/EZ
    # also takes original ar WITHOUT DT

    # modify ar for dt
    ar = float(ar)
    stars = float(stars)
    max_combo = int(float(max_combo))

    if "DT" in mods:
        if ar > 5:
            ms = 200 + (11-ar) * 100
        else:
            ms = 800 + (5-ar) * 80

        if ms < 300:
            ar = 11
        elif ms < 1200:
            ar = round((11-(ms-300)/150)*100)/100
        else:
            ar = round((5-(ms-1200)/120)*100)/100

    # input filters
    if not player_combo:
        player_combo = max_combo
    if ar > 11:
        ar = 11

    final = (((5*(stars)/ 0.0049)-4)**2)/100000;
    if max_combo > 3000:
        lb_constant = math.log10(max_combo / 3000.0)
    else:
        lb_constant = 0
    length_bonus = (0.95 + 0.4 * min(1, max_combo / 3000.0) + lb_constant)
    final *= length_bonus
    final *= (0.97**misses)
    final *= (player_combo/max_combo)**0.8
    # ar bonus
    if ar > 9:
        final *= 1+  0.1 * (ar - 9.0)
    if ar < 8:
        final *= 1+  0.025 * (8.0 - ar)

    pp_values = []
    for acc in accs:
        # acc Penalty
        pre_acc_final = final
        pre_acc_final *=  (acc/100) ** 5.5
        post_acc_final = pre_acc_final
        if "FL" in mods and "HD" in mods:
            final_pp = round(100 * post_acc_final * 1.35 * length_bonus*(1.05 + 0.075 * (10.0 - min(10, ar))))/100 #HDFL
        elif "HD" in mods:
            final_pp = round(100 * post_acc_final * (1.05 + 0.075 * (10.0 - min(10, ar))))/100; # HD
        elif "FL" in mods:
            final_pp = round(100 * post_acc_final * 1.35 * length_bonus)/100  # FL
        else:
            final_pp = round(100 * post_acc_final)/100
        pp_values.append(final_pp)

    return pp_values

# asynchronously download the file
async def download_file(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            return await response.release()

# Returns url to uploaded stars graph
async def plot_map_stars(beatmap, mods, imgur):
    #try:
    star_list, speed_list, aim_list, time_list = [], [], [], []
    results = oppai(beatmap, mods=mods)
    for chunk in results:
        time_list.append(chunk['time'])
        star_list.append(chunk['stars'])
        aim_list.append(chunk['aim_stars'])
        speed_list.append(chunk['speed_stars'])
    plt.figure(figsize=(10, 5))
    plt.style.use('ggplot')
    plt.plot(time_list, star_list, color='blue', label='Stars', linewidth=3.0)
    plt.plot(time_list, aim_list, color='red', label='Aim Stars', linewidth=3.0)
    plt.plot(time_list, speed_list, color='green', label='Speed Stars', linewidth=3.0)
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(plot_time_format))
    plt.ylabel('Stars')
    plt.legend(loc='best')
    plt.tight_layout()
    filepath = "{}.png".format(beatmap)
    plt.savefig(filepath)
    plt.close()
    print(imgur.credits['ClientRemaining'])
    if int(imgur.credits['ClientRemaining']) < 50:
        return 'http://i.imgur.com/iOA0QMA.png'

    pfile = imgur.upload_from_path(filepath)
    os.remove(filepath)
    return pfile['link']
    #except:
        #return 'http://i.imgur.com/iOA0QMA.png'

def plot_time_format(time, pos=None):
    s, mili = divmod(time, 1000)
    m, s = divmod(s, 60)
    return "%d:%02d" % (m, s)

async def _map_completion(btmap, totalhits=0):
    btmap = open(btmap, 'r').read()
    btmap = Beatmap(btmap)
    good = btmap.parse()
    if not good:
        raise ValueError("Beatmap verify failed. "
                         "Either beatmap is not for osu! standart, or it's malformed")
        return
    hitobj = []
    if totalhits == 0:
        totalhits = len(btmap.hit_objects)
    numobj = totalhits - 1
    num = len(btmap.hit_objects)
    for objects in btmap.hit_objects:
        hitobj.append(objects.time)
    timing = int(hitobj[num - 1]) - int(hitobj[0])
    point = int(hitobj[numobj]) - int(hitobj[0])
    map_completion = (point / timing) * 100
    return map_completion

# Returns the full API request URL using the provided base URL and parameters.
def build_request(url_params, url):
    for param in url_params:
        url += str(param)
        if (param != ""):
            url += "&"
    return url[:-1]

def parameterize_event_days(event_days):
    if (event_days == ""):
        event_days = "event_days=1"
    elif (int(event_days) >= 1 and int(event_days) <= 31):
        event_days = "event_days=" + str(event_days)
    else:
        print("Invalid Event Days")
    return event_days

def parameterize_id(t, id):
    if (t != "b" and t != "s" and t != "u" and t != "mp"):
        print("Invalid Type")
    if (len(str(id)) != 0):
        return t + "=" + str(id)
    else:
        return ""

def parameterize_key(key):
    if (len(key) == 40):
        return "k=" + key
    else:
        print("Invalid Key")

def parameterize_limit(limit):
    ## Default case: 10 scores
    if (limit == ""):
        limit = "limit=10"
    elif (int(limit) >= 1 and int(limit) <= 100):
        limit = "limit=" + str(limit)
    else:
        print("Invalid Limit")
    return limit

def parameterize_mode(mode):
    ## Default case: 0 (osu!)
    if (mode == ""):
        mode = "m=0"
    elif (int(mode) >= 0 and int(mode) <= 3):
        mode = "m=" + str(mode)
    else:
        print("Invalid Mode")
    return mode

###-------------------------Setup-------------------------
def check_folders():
    if not os.path.exists("data/osu"):
        print("Creating data/osu folder...")
        os.makedirs("data/osu")
    if not os.path.exists("data/osu/cache"):
        print("Creating data/osu/cache folder...")
        os.makedirs("data/osu/cache")
    if not os.path.exists("data/osu/temp"):
        print("Creating data/osu/temp folder...")
        os.makedirs("data/osu/temp")

def check_files():
    api_keys = {"osu_api_key" : "", 'imgur_auth_info' : "", "puush_api_key": ""}
    api_file = "data/osu/apikey.json"

    if not fileIO(api_file, "check"):
        print("Adding data/osu/apikey.json...")
        fileIO(api_file, "save", api_keys)
    else:  # consistency check
        current = fileIO(api_file, "load")
        if current.keys() != api_keys.keys():
            for key in current.keys():
                if key not in api_keys.keys():
                    current[key] = api_keys[key]
                    print("Adding " + str(key) +
                          " field to osu apikey.json")
            fileIO(api_file, "save", current)

    # creates file for server to use
    settings_file = "data/osu/osu_settings.json"
    if not fileIO(settings_file, "check"):
        print("Adding data/osu/osu_settings.json...")
        fileIO(settings_file, "save", {
            "type": {
                "default": "osu.ppy.sh",
                "ripple":"ripple.moe"
                },
            "num_track" : 50,
            "num_best_plays": 5,
            })

def setup(bot):
    check_folders()
    check_files()

    global api_counter
    api_counter = 0

    osu = Osu(bot)
    tracking = Tracking(bot)

    loop = asyncio.get_event_loop()
    loop.create_task(tracking.play_tracker())
    bot.add_listener(osu.find_link, "on_message")
    bot.add_cog(osu)
bot.add_cog(tracking)