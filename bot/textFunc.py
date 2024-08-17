import discord

async def textFunction(message, context,ai):
    async with message.channel.typing():  
        userMSG = message.content.split("=um ",1)[1]        #get msg content
        response = ai.prompt(message= context+userMSG)      #get raw AI response
        response = response['message'].replace('\n', '\n')  #process raw response
        await message.channel.send(response)                #send response
        return