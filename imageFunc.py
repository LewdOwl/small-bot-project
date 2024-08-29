import io
import random
from discord import File
import os
import aiohttp

# previous
# def query(payload, API_URL, header):
# 	response = requests.post(API_URL, headers=header, json=payload)
# 	return response.content

async def query(payload, API_URL, header):
	async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=header, json=payload) as response:
                return await response.read()

# require token for api and content for prompt
async def imageCreation(IMGtoken, userContent, counter):
	API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
	headers = {"Authorization": IMGtoken}

	image_bytes = await query({
		"inputs": userContent,
		"seed": random.randint(0, 1e6)
	}, API_URL, headers)
	# send discord file
	
	#I do NOT want JSON
	if image_bytes[:1] == b'{' and counter <= 5:
    	# Code to handle the error
		print("Internal server error... regenerating")
		counter+=1
		await imageCreation(IMGtoken, userContent, counter)
	return File(fp=io.BytesIO(image_bytes), filename='output.png')

#actual function
async def imageFunc(message):
	async with message.channel.typing():                    		  			  #realistic typing
            userMSG = message.content.split("=draw ",1)[1]         		  		  #msg content 
            response = await imageCreation(os.getenv('IMGtoken'), userMSG, 0)   	  #get image
            await message.channel.send(file=response)              				  #send image