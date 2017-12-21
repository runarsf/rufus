""" NOT RECOMMENDED, WILL CAUSE RAM (<@319005959022313483>) ISSUES
    @commands.command(pass_context=True)
    async def restart(self, ctx):
        \""" Restarts the bot
            >restart
        \"""
        userid = ctx.message.author.id
        if userid == c.owner_id or userid in str(c.dev_id):
            await self.bot.say('*restarting...*')
            clear = lambda: os.system('cls')
            asyncio.sleep(2)
            await self.bot.logout()
            clear()
            print('restarting')
            asyncio.sleep(0.5)
            clear()
            print('restarting.')
            asyncio.sleep(0.5)
            clear()
            print('restarting..')
            asyncio.sleep(0.5)
            clear()
            print('restarting...')
            asyncio.sleep(0.5)
            clear()
            print('restarting.')
            asyncio.sleep(0.5)
            clear()
            print('restarting..')
            asyncio.sleep(0.5)
            clear()
            print('restarting...')
            subprocess.call([sys.executable, 'rufus.py'])
        else:
            self.bot.say('*Insufficient privileges*')
"""