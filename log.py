async def log(ctx, message):
    print(ctx.author.name + " from " + ctx.guild.name + ' ' + message) 
    return