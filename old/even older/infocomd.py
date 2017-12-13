@client.command(pass_context=True)
async def info(ctx):
    """ Shows information about the specified user. """
    await client.say('```' +
                     'Mention     ::		{}'.format(ctx.message.author.mention + '\n' +
                     'Name        ::		{}'.format(ctx.message.author.name + '\n' +
                     'ID          ::		{}'.format(ctx.message.author.id + '```'))))