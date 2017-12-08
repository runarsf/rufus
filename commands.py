@client.command(pass_context=True)
async def ping(ctx):
    """ Pings the bot host """
    await client.say('pong')