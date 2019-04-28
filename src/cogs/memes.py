import PIL.Image as Image
import random
import os
import re
import discord
import requests
import random
import string
import asyncio
import datetime
from discord.ext import commands
from PIL import Image
from io import BytesIO

import config as c
from cogs.utils import checks
from cogs.utils import deeppyer

class MemesCog(commands.Cog, name="Memes"):
    """ MemesCog """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pfp')
    async def _emote_avatar(self, ctx, asEmotes: bool = True):
        """ Print a happy dog in emotes.
        """
        rufusEmotes = [
            '<:r0_0:567445956417552396>', '<:r1_0:567445959454490644>', '<:r2_0:567445960993669140>', '<:r3_0:567445963917099089>', '<:r4_0:567445963875287059>', '<:r5_0:567445965531906068>', '\n',
            '<:r0_1:567445956841308160>', '<:r1_1:567445958888259614>', '<:r2_1:567445961018834944>', '<:r3_1:567445963225169920>', '<:r4_1:567445964902891522>', '<:r5_1:567445965506740260>', '\n',
            '<:r0_2:567445956694507549>', '<:r1_2:567445959647166485>', '<:r2_2:567445961073491985>', '<:r3_2:567445963032100875>', '<:r4_2:567445965364133888>', '<:r5_2:567445965494026271>', '\n',
            '<:r0_3:567445958510641162>', '<:r1_3:567445959672463381>', '<:r2_3:567445961962553409>', '<:r3_3:567445963384291330>', '<:r4_3:567445965448020002>', '<:r5_3:567445966853111864>', '\n',
            '<:r0_4:567445958191743028>', '<:r1_4:567445960813314068>', '<:r2_4:567445961635266636>', '<:r3_4:567445963879219200>', '<:r4_4:567445965993279508>', '<:r5_4:567445965917913119>', '\n',
            '<:r0_5:567445958821150721>', '<:r1_5:567445960914108416>', '<:r2_5:567445961715089428>', '<:r3_5:567445963501731850>', '<:r4_5:567445965607272478>', '<:r5_5:567445965984890900>'
        ]
        message = ''
        for emote in rufusEmotes:
            message += emote
        await ctx.send(message)

    @commands.command(name='search')
    async def _reddit_search(self, ctx, *, query: str):
        """ Search reddit.
            https://stackoverflow.com/questions/21458102/reddit-search-api-url
        """
        pass

    @commands.command(name='meme', aliases=['reddit'])
    async def _reddit_meme(self, ctx, subreddit: str = 'random', section: str = 'random'):
        """ Get memes (images, gifs, videos) from a subreddit.
            Sections:
                - random
                - new
                - top
                - controversial
                - hot
                - rising
        """
        try:
            reddits = ['PewdiepieSubmissions', 'memes', 'dankmemes', 'me_irl']
            if subreddit.lower() == 'random':
                subreddit = random.choice(reddits)
            if section.lower() == 'random' or subreddit.lower() == 'random':
                num: int = random.randint(0, 24)
                section = 'new'
            else:
                num: int = 0
            # requests
            # reddit has blocked the curl user agent, change it
            headers = {'User-Agent': 'rufus-agent'}
            url = f'https://reddit.com/r/{subreddit}/new/.json'
            data = requests.get(url, headers=headers).json()
            aboutUrl = f'https://reddit.com/r/{subreddit}/about.json'
            aboutData = requests.get(aboutUrl, headers=headers).json()
            userUrl = f"https://reddit.com/user/{data['data']['children'][num]['data']['author']}/about.json"
            userData = requests.get(userUrl, headers=headers).json()

            # check if the post is a video
            if bool(data['data']['children'][num]['data']['is_video']):
                mediaUrl = str(data['data']['children'][num]['data']['media']['reddit_video']['fallback_url'])
            else:
                mediaUrl = str(data['data']['children'][num]['data']['url'])

            selftext = str(data['data']['children'][num]['data']['selftext'])
            description = selftext if bool(selftext) else ''
            try:
                icon = str(userData['data']['icon_img']).split('?')[0]
            except:
                icon = ''
            embed = discord.Embed(title=str(data['data']['children'][num]['data']['title']), timestamp=datetime.datetime.fromtimestamp(int(data['data']['children'][num]['data']['created_utc'])), description=description, color=checks.getDominantColor(str(mediaUrl)), url='https://reddit.com' + data['data']['children'][num]['data']['permalink'])
            embed.set_author(name='u/'+str(data['data']['children'][num]['data']['author']), icon_url=icon)
            embed.set_footer(text=str(data['data']['children'][num]['data']['subreddit_name_prefixed']), icon_url=str(aboutData['data']['icon_img']))

            if bool(data['data']['children'][num]['data']['over_18']) and not ctx.message.channel.is_nsfw():
                embed.add_field(name="NSFW", value=str(mediaUrl), inline=False)
            else:
                try:
                    embed.set_image(url=mediaUrl)
                except:
                    pass

            await ctx.send(embed=embed)
        except:
            # CommandInvokeError: Command raised an exception: KeyError: 'is_video' (subreddit doesn't exist)
            # CommandInvokeError: Command raised an exception: KeyError: 'data' (subreddit is restricted)
            await ctx.send('```Subreddit restricted or non-existent.```')

    @commands.command(name='fry')
    async def _deepfry_image(self, ctx, image: str = 'previousMessage'):
        """ Deepfry an image.
        """
        async for message in ctx.channel.history(limit=2):
            imgUrl = message.attachments
        imgUrl = imgUrl[0].url

        response = requests.get(imgUrl)
        img = Image.open(BytesIO(response.content))
        img = await deeppyer.deepfry(img)
        await ctx.send(file=discord.File(Image.open(img)))

    @commands.command(name='love')
    async def _love(self, ctx, member: str = '', *, message: str = ''):
        """ Share your love
        """
        try:
            member = await discord.ext.commands.UserConverter().convert(ctx, member)
        except discord.ext.commands.BadArgument:
            if str(member) == 'me':
                await ctx.message.add_reaction('💖')
                return
        if not member:
            await ctx.send('*...is a great thing...*')
        else:
            if not message:
                await ctx.send(f'*{ctx.message.author.name} shared their love with {member} and probably likes them!*')
            else:
                await self.bot.say(f'*{ctx.message.author.name} shared their love with {member} {message}*')

    @commands.command(name=':(', hidden=True)
    async def _angry_face(self, ctx):
        """ Don't be angry.
        """
        await ctx.message.add_reaction('😲')

    @commands.command(name='kms')
    async def _self_kill(self, ctx):
        """ End it all.
        """
        await ctx.send(file=discord.File(f'{str(os.path.dirname(os.path.realpath(__file__)))}/../img/anoose.jpg'))
        await ctx.send(f'Come {ctx.message.author.mention}. *~~He?~~* She\'s waiting for you!')

    @commands.command(name='lenny')
    async def _lennyface(self, ctx):
        """ Replaces user message with lennyface.
        """
        await ctx.send('( ͡° ͜ʖ ͡°)')
        await ctx.message.delete()

    @commands.command(name='kys')
    async def _member_kill(self, ctx, *, member: discord.Member = ''):
        """ Please be cautious when using this command.
        """
        await ctx.message.delete()
        await ctx.send(f'Hey {member}. {ctx.message.author.name} is implying *he/she/it/social construct*' +
                        'wants you to cease existing, however,' +
                        'for their will to be fulfilled,' +
                        'the death needs to be inflicted by yourself and yourself alone.')

    @commands.command(name='tocch', aliases=['touch', 'spaghetti', 'spaghett'])
    async def _touch_spaghetti(self, ctx):
        """ DOON NOTT TOCCH S P A G O O T
        """
        channel = ctx.message.channel
        await ctx.message.add_reaction('🍝')
        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '🍝'
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.message.remove_reaction('🍝', self.bot.user)
        else:
            await channel.send(random.choice(['***DOON NOTT TOCCH S P A G O O T***', '***SOMEBODY TOUCHE MY SPAGHETT***', ':⁽']))
            await ctx.message.remove_reaction('🍝', user)

    @commands.command(name='knuckles')
    async def _ugandan_knuckles(self, ctx):
        """ DO YOU KNO DE WAE?
        """
        knuckles = ['ALL HEIL DE QUEEN BRUDDERS',
                    '*spit*',
                    'WE MUST PROTECC DE QUEEN',
                    'DO YOU KNO DE WAE?',
                    'WE MUST RETURN TO UGANDA',
                    'YOU MUST BOW DOWN TO DE QUEEN',
                    'I DON\'T KNOW DE WAE',
                    'MY BRUDDERS THE QUEEN WILL MAKE A SPEECH',
                    'SPIT ON HIM',
                    'DO NOT DISRESPEC DE QUEEN',
                    'WHY AR U RUNNIN?'
		    ]
        await ctx.send(random.choice(knuckles))

    @commands.command(name='owo', aliases=['uwu'])
    async def _owo(self, ctx, *, message: str = 'owo'):
        """ owo~ify text.
        """
        owolist = ['(・`ω´・)', ';;w;;', ';w;', 'owo', 'OwO', 'Owo', 'owO', 'uwu', 'UwU', '>w<', '^w^']
        replacers = [',', '.', '!', '?']
        message = message.replace('l', 'w').replace('L', 'W').replace('r', 'w').replace('R', 'W')
        newmessage = message
        for index, letter in enumerate(str(message)):
            if letter in replacers:
                if str(message)[index-1:index] == ' ':
                    newmessage = newmessage.replace(letter, random.choice(owolist), 1)
                else:
                    newmessage = newmessage.replace(letter, f' {random.choice(owolist)}', 1)
        await ctx.send(f'```{newmessage}```')

    @commands.command(name='mock')
    async def _mock(self, ctx, *, string: str = ''):
        """ Convert string to mock(str)ing.
        """
        def mockify(string: str):
            outstr=''
            for index, letter in enumerate(string):
                if index % 2 == 0:
                    outstr += letter.lower()
                else:
                    outstr += letter.upper()
            return outstr
        if string:
            _noTestsPassed: bool = True
            try:
                int(string)
            except ValueError:
                pass # is not an integer, pass this, intentional™ error
            else:
                # is an integer
                _noTestsPassed: bool = False
                iterator = 0
                async for message in ctx.channel.history(limit=int(string)+1):
                    if iterator == int(string):
                        await ctx.send(mockify(str(message.content)))
                    iterator += 1
            try:
                member = await discord.ext.commands.UserConverter().convert(ctx, string)
            except discord.ext.commands.BadArgument:
                pass # is not type discord.Member, pass this, intentional™ error
            else:
                # is type discord.Member
                _noTestsPassed: bool = False
                async for message in ctx.channel.history(limit=100):
                    if message.author == member:
                        await ctx.send(mockify(str(message.content)))
                        break
            if _noTestsPassed:
                await ctx.send(mockify(str(string)))
        else:
            await ctx.message.delete()
            async for message in ctx.channel.history(limit=1):
                await ctx.send(mockify(str(message.content)))


    @commands.command(name='pat')
    async def _pat(self, ctx, member: str = '', *, message: str = ''):
        """ Pat uwu.
        """
        try:
            member = await discord.ext.commands.UserConverter().convert(ctx, member)
        except discord.ext.commands.BadArgument:
            if str(member) == 'me':
                await ctx.send(f'*I gently pat {ctx.message.author.name}...*')
                return
        if member == '':
            await ctx.send('uwu')
        else:
            if message == '':
                await ctx.send(f'*{ctx.message.author.name} patted {member} and is probably a disgusting weeb!*')
            else:
                await self.bot.say(f'*{ctx.message.author.name} patted {member} {message}*')

    @commands.command(name='hug')
    async def _hug(self, ctx, *, member: str = ''):
        """ Hug user.
        """
        try:
            member = await discord.ext.commands.UserConverter().convert(ctx, member)
        except discord.ext.commands.BadArgument:
            if str(member) == 'me':
                await ctx.send(f'*Hugs {ctx.message.author.name}...*')
                return
        if member == '':
            await ctx.send(f'*{ctx.message.author.name} tries to hug the air*')
        elif member == ctx.message.author or member == 'me':
            await ctx.send(random.choice(['Aaaaaaall by myseeeeeeeelf.', '*hugs you*']))
        elif member == self.bot.user:
            await ctx.send('OwO wat dis? Am I being hugger?')
        else:
            await ctx.send(f'{ctx.message.author.name} hugged {member} :hearts:')

    @commands.command(name='slap')
    async def _slap(self, ctx, member: str, *item):
        """ Slap a person. They probably deserve it.
        """
        try:
            member = await discord.ext.commands.UserConverter().convert(ctx, member)
        except discord.ext.commands.BadArgument:
            if str(member) == 'me':
                await ctx.send(f'*SLAP!*')
                return
        _slap_item: str = ''
        if item:
            _slap_item = f' with {" ".join(item)}.'
        await ctx.send(f'{ctx.message.author.mention} slapped {member.mention}{_slap_item}')


def setup(bot):
    bot.add_cog(MemesCog(bot))
