
async def textFunctionMeta(message, guildMap):
    async with message.channel.typing():
        guildID = str(message.guild.id)                    #shorthand
        metaOBJ= guildMap[guildID]["metaOBJ"]                 #shorthand

        await metaOBJ.ini(message)
        await metaOBJ.resetCheck(message, False)
        await metaOBJ.query(message, 0)                     #this will send response

        return