#libs
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
import discord
import asyncio
import json
import os

#files, functions
from imageFunc import imageFunc
from textFunc import textFunction
from musicGENfunc import musicGENFunc
from log import log
from imageFunc import imageFunc
from resetContext import resetContext

load_dotenv()                                                 # Load environment variables from .env file
with open('.json','r') as file:
    ownerID = json.load(file)['friend']
    file.close()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(
    command_prefix = '=',
    owner_ids = ownerID,
    help_command = None,
    strip_after_prefix = True,
    intents = intents
)


# client = discord.Client(intents = intents) # new client

#prompt engineering
context = os.getenv('context')                            
guildMap = {}                                                            #instance for each guild

@client.event
async def on_ready(): 
    print('started\n{0.user} is online and connected to '.format(client) + str(len(client.guilds)) + " servers: ")
    async for guild in client.fetch_guilds(limit=250): 

        guildMap[str(guild.id)] = {"instance": 6, 
                                   "source": "", 
                                   "lastMessageTime": datetime.now(), 
                                   "messageCount": 1                     #first message is the context file
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

# commands
@client.command()
async def um (ctx):
    await log(ctx.message, "generated message")
    await textFunction(ctx.message, context, guildMap, 0)                    #text helper function, update source

@client.command()
async def source (ctx):
    await log(ctx.message, "checked source")
    await ctx.message.channel.send(guildMap[str(ctx.message.guild.id)]["source"])

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
# spec commands # does not work rn
#===============#

@client.command()
@commands.is_owner()
async def reset(ctx):                                                       #force reset chat history
    sGuildMap = guildMap[str(ctx.message.guild.id)]
    await resetContext(ctx.message, sGuildMap, context, True)


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


#running
client.run(os.getenv('token')) 