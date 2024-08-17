import discord
from discord import File
import io
import random
import requests
import os

def query(payload, API_URL, header):
	response = requests.post(API_URL, headers=header, json=payload)
	return response.content

def music_generation(IMGtoken, userContent):
    API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
    headers = {"Authorization": IMGtoken}
	
    audio_bytes = query({
	    "inputs": userContent,
        "seed": random.randint(0, 1e6)
    }, API_URL, headers)
    
    return File(fp=io.BytesIO(audio_bytes), filename='outputs.ogg') #missing

async def musicGENFunc(message):
	async with message.channel.typing():                    		  	  #realistic typing
            userMSG = message.content.split("=make ",1)[1]         		  #msg content 
            response = music_generation(os.getenv('IMGtoken'), userMSG)   	  #get image
            await message.channel.send("-# this is an experimental command nya-",file=response)              		  #send image
            return