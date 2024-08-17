#libs
from meta_ai_api import MetaAI
import discord
import os
from dotenv import load_dotenv

#files, functions
from imageFunc import imageFunc
from textFunc import textFunction
from musicGENfunc import musicGENFunc


load_dotenv()                                                 # Load environment variables from .env file
ai = MetaAI()                                                 # new instance

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents) # new client

#prompt engineering
context = os.getenv('context')                            
response = ai.prompt(message= context)                        #in hopes that prompts works

@client.event
async def on_ready():                                         #on_ready is a pre-exist function name
    print('started\nusername: {0.user}'.format(client))       # 0 is replaced as client

@client.event
async def on_message(message):
    msgContent = message.content                             #shorthand for message.content
    if message.author.bot:                                    #add a check to see its its a bot user or is blacklisted
        return
    if msgContent.startswith('=um '):
        print("msg request")
        await textFunction(message,context,ai)            #text helper function
    if msgContent.startswith('=draw '):
        print("img request")
        await imageFunc(message)                                #image gen helper function
    if msgContent.startswith('=make '):
        print("music request")
        await musicGENFunc(message)
    '''
    if message.content == ":3":
        print("meow")
        await message.channel.send("meow")                         # test ping
    '''
#running
client.run(os.getenv('token')) 