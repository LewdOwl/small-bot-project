from datetime import datetime
from resetContext import resetContext

async def textFunction(message, context, guildMap, counter):
    async with message.channel.typing():
        guildID = str(message.guild.id)                    #shorthand
        sGuildmap = guildMap[guildID]                      #shorthand

        await resetContext(message, sGuildmap, context, False)#check if it needs to reset
        ai = sGuildmap["instance"]                         #shorthand
        
        userMSG = message.content.split("=um ",1)[1]        #get msg content
        response = ai.prompt(message= context+userMSG)      #get raw AI response
        sGuildmap["lastMessageTime"] = datetime.now()

        sGuildmap["messageCount"] += 1                      # message counter add 1
        sGuildmap["source"] = response['sources']           #update source
        response = response['message'].replace('\n', '\n')  #process raw response

        #panic fix for welsh error, maximum 5 rerolls
        if counter <= 5 and "I don’t understand" in response[:30]:
            print("welsh/other msg error trash...")
            counter+=1
            await textFunction(message, context, guildMap, counter)
            return 
        
        sGuildmap["messageCount"] += 1                      # message counter add 1
        await message.channel.send(response)                #send response
        return