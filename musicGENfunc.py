from discord import File
import io
import random
import os
import aiohttp


async def query(payload, API_URL, header):
	async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=header, json=payload) as response:
                return await response.read()


async def music_generation(IMGtoken, userContent):
    API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
    headers = {"Authorization": IMGtoken}
	
    audio_bytes = await query({
	    "inputs": userContent,
        "seed": random.randint(0, 1e6)
    }, API_URL, headers)
    
    return File(fp=io.BytesIO(audio_bytes), filename='outputs.ogg') #missing

async def musicGENFunc(message):
	async with message.channel.typing():                    		  	  #realistic typing
            userMSG = message.content.split("=make ",1)[1]         		  #msg content 
            response = await music_generation(os.getenv('IMGtoken'), userMSG)   	  #wait for music
            await message.channel.send("-# this is an experimental command nya-",file=response)              		  #send image