""" admin -- rufus.py """
import os
import ctypes
import config as c

from discord.ext import commands


class Admin:
    """ Admin restricted commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def purge(self, ctx, amount: str):
        """ Deletes messages from current channel.
            >purge <@user | amount: int | 'all'>
        """
        userid = ctx.message.author.id
        usid = int(amount.replace('<@', '').replace('>', ''))
        if userid in str(c.owner_id) or str(c.dev_id) or str(c.admin_id):
            await self.bot.delete_message(ctx.message)
            if '<@' in amount and '>' in amount:
                async for amount in self.bot.logs_from(ctx.message.channel):
                    if amount not in self.bot.logs_from(ctx.message.channel):
                        return
                    else:
                        await self.bot.delete_message(ctx.message.id == usid)
            elif amount == str('all'):
                deleted = await self.bot.purge_from(ctx.message.channel, limit=750)
                await self.bot.say('Bulk-purged **{}** Messages'.format(len(deleted)))
                async for msg in self.bot.logs_from(ctx.message.channel):
                    await self.bot.delete_message(msg)
            elif int(amount) > 0:
                counter = 0
                for counter in range(int(amount)):
                    async for msg in self.bot.logs_from(ctx.message.channel):
                        if int(counter) >= int(amount):
                            return
                        else:
                            await self.bot.delete_message(msg)
                        counter += 1
            else:
                print('purge, error on else')
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def spam(self, ctx, times: int, *, msg: str):
        """ Repeats a message multiple times.
            >spam <message_string>
        """
        if "admin" in [y.name.lower() for y in author.roles]:
            for i in range(times):
                await self.bot.say(msg)
                print(i)
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def invbot(self, ctx, *, userToInvite: str):
        invite = 'https://discordapp.com/oauth2/authorize?client_id=387390496038977536&scope=bot&permissions=2146958591'
        userid = ctx.message.author.id
        if userid in str(c.owner_id) or str(c.dev_id) or str(c.admin_id):
            await self.bot.send_message(ctx.message.server.get_member_named(userToInvite), invite)
            await self.bot.say('Invite link sent to **{}**.'.format(ctx.message.server.get_member_named(userToInvite)))
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """ Stops the bot.
            >stop
        """
        userid = ctx.message.author.id
        if userid in str(c.owner_id) or str(c.dev_id) or str(c.admin_id):
            await self.bot.say('*Goodbye.*')
            await self.bot.logout()
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def restart(self, ctx):
        """ Restarts the bot. Does not apply file changes.
            >restart
        """
        userid = ctx.message.author.id
        if userid in str(c.owner_id) or str(c.dev_id) or str(c.admin_id):
            await self.bot.say('*Restarting bot. Please hold.*')
            await self.bot.logout()
            os.system('python rufus.py')
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def call(self, ctx, *, msg: str):
        """ Send a message via the bot to the author.
            >call
        """
        userid = ctx.message.author.id
        username = ctx.message.author.name
        if userid in str(c.owner_id) or str(c.dev_id) or str(c.admin_id):
            await self.bot.send_message(ctx.message.author,
                                        'You message has been sent to <@{}>. You should receive a reply shortly. '
                                        'Please be patient.'.format(c.owner_id))
            await self.bot.send_message(ctx.message.author, '```Message: {}```'.format(msg))
            await self.bot.send_message(c.owner_id, '```New message from: {}\nContent: {}```'.format(ctx.message.author, msg))
        else:
            await self.bot.say('*Insufficient privileges*')

def setup(bot):
    """ defines setup """
    bot.add_cog(Admin(bot))
