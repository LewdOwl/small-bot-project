#libs
from discord.ext import commands
from dotenv import load_dotenv
import discord
import asyncio
import json
import os
# crazy
from src.AI_model_classes.meta_class.meta_AI import meta_ai
from src.AI_model_classes.gemini_class.gemini_AI import gemini_ai
# import pkgutil
# for module in pkgutil.iter_modules(['folder_name']):
#     __import__(f"folder_name.{module.name}")

from imageFunc import imageFunc
from textFuncMeta import textFunctionMeta
from textFuncGemini import textFunctionGemini
from musicGENfunc import musicGENFunc
from log import log
from imageFunc import imageFunc
#personalities from now
from src.AI_model_classes.gemini_class.personality_folder.insult import insult
from src.AI_model_classes.gemini_class.personality_folder.mechanical import mechanical
from src.AI_model_classes.gemini_class.personality_folder.void import void



load_dotenv()                                                 # Load environment variables from .env file
with open('.json','r') as file:                               # vision of poor design
    data = json.load(file)
ownerID = data['friend']


insult_context = data['geminiINSTRUCTIONmap'][0]['insult'][0]['context1']
mechanical_context = data['geminiINSTRUCTIONmap'][0]['mechanical'][0]['context1']
void_context = data['geminiINSTRUCTIONmap'][0]['concise/void'][0]['context1']

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(
    command_prefix = '=',
    owner_ids = ownerID,
    help_command = None,
    strip_after_prefix = True,
    intents = intents
)
guildMap = {}

metaContext = os.getenv('context')
GEMINI_API_KEY = os.getenv('gemToken')                                   #global gemini guide
REQUESTS_PER_MINUTE = int(os.getenv('REQUESTS_PER_MINUTE'))

#really just a list
personalityMap = [
    insult(insult_context),
    mechanical(mechanical_context),
    void(void_context)
]     #really just a list

# update guildMap
@client.event
async def on_ready(): 
    print('started\n{0.user} is online and connected to '.format(client) + str(len(client.guilds)) + " servers: ")
    async for guild in client.fetch_guilds(limit=250):
        guildMap[str(guild.id)] = {"metaOBJ": meta_ai(metaContext),
                                    "geminiOBJ": gemini_ai(personalityMap,GEMINI_API_KEY,REQUESTS_PER_MINUTE)
                                   }

        print(" - " + guild.name + " - " + str(guild.id))                #list every guild it is in

@client.event
async def on_message(message):
    if message.author.bot or isinstance(message.channel, discord.channel.DMChannel):
        return

    if message.content == (":3"):
        with open('nya.txt', 'r') as file:
            content = file.read()
            file.close()
        await message.channel.send(content) 
    await client.process_commands(message)

    if client.user.mentioned_in(message):               # ping = main personality reply
        await textFunctionMeta(message,guildMap)
        await log(message, "generated message (meta)")

# commands
@client.command()
async def um (ctx):
    await textFunctionMeta(ctx.message,guildMap)
    await log(ctx.message, "generated message (meta)")
    return

@client.command()
async def uh (ctx):
    await textFunctionGemini(ctx.message,guildMap)
    await log(ctx.message, "generated message (gemini)")

@client.command()
async def source (ctx):
    await guildMap[str(ctx.message.guild.id)]["metaOBJ"].sendSource(ctx.message)
    await log(ctx.message, "checked source")
    return

@client.command()
async def draw (ctx):
    await log(ctx.message, "generated image")
    asyncio.create_task(imageFunc(ctx.message))

@client.command()
async def make (ctx):
    await log(ctx.message, "generated music")
    asyncio.create_task(musicGENFunc(ctx.message))                            #music gen helper function

@client.command()
async def help (ctx):
    await log(ctx.message, "opened help.txt")
    file = open("help.txt", "r")
    helpContent = file.read()
    file.close()
    await ctx.send(embed = discord.Embed(title = "I-19's commands", description = helpContent, color = 0x155835))

@client.command()
async def change_log(ctx):
    file = open("changeLog.txt", "r")
    await ctx.send(embed = discord.Embed(title = "change log", description = file.read(), color = 0x155835))
    file.close()

#===============# 
# spec commands #
#===============#

@client.command()
@commands.is_owner()
async def resetMeta(ctx):                                                       #force reset chat history
    message = ctx.message
    await guildMap[str(message.guild.id)]["metaOBJ"].resetCheck(message,True)
    return

@client.command()
@commands.is_owner()
async def resetGemini(ctx):                                                       #force reset gemini
    message = ctx.message
    guildMap[str(message.guild.id)]["geminiOBJ"].geminiReset(True)
    return


@client.command()
@commands.is_owner()
async def bail(ctx, *, ID):
    guild = client.get_guild(int(ID))
    try: 
        print("Bailing from " + guild.name)
        await guild.leave()
        await ctx.send("Successfully left " + guild.name)
    except:
        print("Guild does not exist! ID: " + guild.name)
        await ctx.send("I'm not part of this guild! Check the ID please.")

@client.command()
@commands.is_owner()
async def s(ctx):
    message = ctx.message
    guildID = str(message.guild.id)                    #shorthand
    geminiOBJ = guildMap[guildID]["geminiOBJ"]                 #shorthand

    async with message.channel.typing():
        await geminiOBJ.squery(message, message.attachments[0] if message.attachments else None)                     #this will send response


@client.command()
@commands.is_owner()
async def ss(ctx):
    message = ctx.message
    guildID = str(message.guild.id)                    #shorthand
    geminiOBJ = guildMap[guildID]["geminiOBJ"]                 #shorthand

    async with message.channel.typing():
        await geminiOBJ.ssquery(message, message.attachments[0] if message.attachments else None)                     #this will send response


#===============# 
# debug commands#
#===============#
@client.command()
@commands.is_owner()
async def historyGemini(ctx):
    message = ctx.message
    guildMap[str(message.guild.id)]["geminiOBJ"].printHistory()


#running
client.run(os.getenv('token')) 