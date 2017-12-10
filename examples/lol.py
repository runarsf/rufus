@client.command(pass_context=True)
async def addbtc(create_custom_emoji):
    """ Adds the BitCoin emoji """
    dserver = client.get_server_id()
    await create_custom_emoji(dserver, 'BitCoin', 'btc.png')
    await client.say('done')

@client.command(pass_context=True)
async def getid(ctx):
    """ Sends the ID of the specified user. """
    mcont = ctx.message.content
    userid = str('``' + mcont.replace(c.prefix + 'getid <@', '').replace('>', '') + '``')
    await client.say(userid)
    print(userid)