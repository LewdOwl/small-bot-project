async def textFunctionGemini(message, guildMap):
    async with message.channel.typing():
        guildID = str(message.guild.id)                    #shorthand
        geminiOBJ = guildMap[guildID]["geminiOBJ"]                 #shorthand

        await geminiOBJ.query(message, message.attachments[0] if message.attachments else None)                     #this will send response

        return    