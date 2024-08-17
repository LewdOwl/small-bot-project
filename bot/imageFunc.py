import requests
import io
import random
import discord
from discord import File
import os


# helper function, not written by me
def query(payload, API_URL, header):
	response = requests.post(API_URL, headers=header, json=payload)
	return response.content

# require token for api and content for prompt
def imageCreation(IMGtoken, userContent):
	API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
	headers = {"Authorization": IMGtoken}

	image_bytes = query({
		"inputs": userContent,
		"seed": random.randint(0, 1e6)
	}, API_URL, headers)
	# send discord file
	return File(fp=io.BytesIO(image_bytes), filename='output.png')

#actual function
async def imageFunc(message):
	async with message.channel.typing():                    		  	  #realistic typing
            userMSG = message.content.split("=draw ",1)[1]         		  #msg content 
            response = imageCreation(os.getenv('IMGtoken'), userMSG)   	  #get image
            await message.channel.send(file=response)              		  #send image
            return