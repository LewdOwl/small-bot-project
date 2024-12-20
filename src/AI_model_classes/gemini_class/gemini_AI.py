import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_class import ai
from datetime import datetime, timedelta
import google.generativeai as genai
import requests
from io import BytesIO
from PIL import Image
import random

# global, so only create 1 instance
class gemini_ai(ai):
    def __init__(self, personalityMap, api_key, REQUESTS_PER_MINUTE):
        self.curIndex = 0
        self.blackListMap ={}
        self.blackListSize = 0

        self.minute_req_count = 0
        self.iniCycleTime = datetime.now()       #to know if a minute is passed
        self.history = ""                        # so it wouldn t add the instruction to history everytime



        self.REQUESTS_PER_MINUTE = REQUESTS_PER_MINUTE
        self.personalityMap = personalityMap
        self.iniTime = datetime.now()

        if self.instance !=0:
            return
        genai.configure(api_key=api_key)

        self.instance = genai.GenerativeModel (
            model_name = "models/gemini-1.5-flash",
            generation_config = {
                "temperature": 0
            }
        )
        self.curIndex = self.selectPersonality()

    #methods ==========================================
    #
    # no sane person would want to download files on their local machine
    def process_attachment(self, attachment = None):
        if attachment:
            # Check if the attachment is an image
            if not attachment.content_type.startswith('image/'):
                print("no sane person would upload audio file")
                return -1
            response = requests.get(attachment.url)
            if response.status_code != 200:
                return -1
            # Convert to PIL Image
            image = Image.open(BytesIO(response.content))
            return image
        return -1               # not image/ none automatically return -1

    # amazing
    def selectPersonality(self)->int:
        num = len(self.personalityMap) - self.blackListSize
        if num == 0:
            self.blackListMap = {}  # clear map
            self.blackListSize = 0  # clear        
            num = len(self.personalityMap) #all items
            
        randIndex = random.randint(0, num-1)
        randIndex2 = randIndex                      #duplicate
        print(f"total personality map size: {len(self.personalityMap)}")
        print(f"random Index: {randIndex}")
        print(f"black list size: {self.blackListSize}")
              
        if randIndex in self.blackListMap:          #if blacklisted
            print(f"edited!! key: {randIndex} value:{self.blackListMap[randIndex]}")
            randIndex = self.blackListMap[randIndex]    #get the mapped instead
        
        if randIndex2 != num-1:          #if it is not end item
            self.blackListMap[randIndex2]= num-1    #try map to the removed item

        if (num - 1 in self.blackListMap) and (self.blackListMap[num-1] in self.blackListMap):   #if the removed item is blacklisted
            self.blackListMap[randIndex2] = self.blackListMap[num-1] # go through the map, map again
            del self.blackListMap[num-1]                                #merged

        self.blackListSize+=1                   #increase
        print(f"updated blackListSize: {self.blackListSize}")
        print(f"Index: {randIndex}, or {self.personalityMap[randIndex].name} is selected")
        return randIndex
    
    # this func can change config
    def resetREAL(self):
        self.iniTime = datetime.now()
        self.curIndex = self.selectPersonality()    #change personality per reset
        
        personalityOBJ = self.personalityMap[self.curIndex] # temp var
        self.instance.generation_config = {"temperature": personalityOBJ.temperature,
                                           "max_output_tokens": personalityOBJ.maxToken
        }
        
    # true = no response, false = can have response
    def maximumReqGuard(self) -> bool:
        timeDiff = datetime.now() - self.iniCycleTime
        if (timeDiff.seconds < 60):
            if (self.minute_req_count >= 15):
                return True
        else:
            self.iniCycleTime = datetime.now()  #reset cycle to 60 sec
            self.minute_req_count = 0        # reset req count
        self.minute_req_count += 1
        return False

    def geminiReset(self, condition):
        if (self.resetCond(timedelta(days=2), timedelta(days=1), 15, condition)):
            print("clearing gemini chat history (reset)")
            self.history = ""
            self.resetREAL()              # what kind of personality will it be next

    def splitUserMsg(self, message):
        return message.content.split("=uh ",1)[1] if len(message.content) > 4 else " "
    
    def updateHistoryPrompt (self, authorName, messageContent, imageMaybe):
        self.history += f"{authorName}: {messageContent} "
        if imageMaybe != -1:                #if image exist
            self.history+= "[image]"        #yea, not getting a ai vision service for this
        pass
    
    async def split_and_send_message(self, channel, message, chunk_size=2000):

        # Initialize variables
        messages_sent = []
    
        # If message is shorter than chunk_size, send it directly
        if len(message) <= chunk_size:
            sent_message = await channel.send(message)
            return [sent_message]
    
        # Split message into chunks
        chunks = []
        for i in range(0, len(message), chunk_size):
            # Get chunk of appropriate size
            chunk = message[i:i + chunk_size]
        
            # If we're splitting mid-word and this isn't the last chunk,
            # try to split at the last space
            if i + chunk_size < len(message) and message[i + chunk_size].isalnum():
                last_space = chunk.rfind(' ')
                if last_space != -1:  # If we found a space
                    # Move the partial word to the next chunk
                    chunk = chunk[:last_space]
                    # Adjust the starting point of the next chunk
                    i = i + last_space - chunk_size
        
            chunks.append(chunk.strip())
    
    # Send each chunk
        for index, chunk in enumerate(chunks):
            # Add a continuation indicator
            if len(chunks) > 1:
                chunk = f"[{index + 1}/{len(chunks)}]\n{chunk}"
        
            # Send the chunk and store the message object
            sent_message = await channel.send(chunk)
            messages_sent.append(sent_message)
        
            # Optional: Add a small delay to prevent rate limiting
            # await asyncio.sleep(0.5)
    
        return messages_sent
    async def query(self, message, attachment=None):
        if (self.maximumReqGuard()):    #this checks for minute cycles
            return
        self.geminiReset(False)             #this checks for overall
        
        personalityOBJ = self.personalityMap[self.curIndex] # temp var

        tempImg = self.process_attachment(attachment)
        messageContant = self.splitUserMsg(message)

        payload = []
        payload.append(f"{personalityOBJ.context}\n\n===history===\n{self.history}===history end===\n\n{message.author.display_name}:{messageContant}")
        if tempImg != -1:    #if it is a real image
            payload.append(tempImg)
        
        self.updateHistoryPrompt(message.author.display_name, messageContant, tempImg)

        # response history need to be updated in query
        self.history = await personalityOBJ.query(self.instance.start_chat(), 
                                 message.author.display_name,
                                 message.channel,
                                 self.history,
                                 payload
                                 )

        self.update_msgCount_and_time()
        return

    # debug methods
    def printHistory(self):
        print(self.history)

    async def squery(self, message, attachment=None):
        if (self.maximumReqGuard()):    #this checks for minute cycles
            return
        self.geminiReset(False)             #this checks for overall

        self.instance.generation_config = {"temperature": 0.0,              #panic
                                           "max_output_tokens": 65536
        }
        tempImg = self.process_attachment(attachment)
        messageContant = message.content.replace("=s","")

        payload = []
        payload.append(f"{self.history}\n{message.author.display_name}:{messageContant}")
        if tempImg != -1:    #if it is a real image
            payload.append(tempImg)
        
        self.updateHistoryPrompt(message.author.display_name, messageContant, tempImg)

        # response history need to be updated here
        response = await self.instance.start_chat().send_message_async(payload)
        response = response.text
        self.history += f"I-19: {response}"
        #await message.channel.send(response)
        await self.split_and_send_message(message.channel,response,1900)

        self.update_msgCount_and_time()
        return
    
    async def ssquery(self, message, attachment=None):
        if (self.maximumReqGuard()):    #this checks for minute cycles
            return
        self.geminiReset(False)             #this checks for overall

        self.instance = genai.GenerativeModel (
            model_name = "models/gemini-1.5-pro",
            generation_config = {
                "temperature": 0
            }
        )
        tempImg = self.process_attachment(attachment)
        messageContant = message.content.replace("=s","")

        payload = []
        payload.append(f"{self.history}\n{message.author.display_name}:{messageContant}")
        if tempImg != -1:    #if it is a real image
            payload.append(tempImg)
        
        self.updateHistoryPrompt(message.author.display_name, messageContant, tempImg)

        # response history need to be updated here
        response = await self.instance.start_chat().send_message_async(payload)
        response = response.text
        self.history += f"I-19: {response}"
        #await message.channel.send(response)
        await self.split_and_send_message(message.channel,response,1900)

        self.update_msgCount_and_time()

        self.instance = genai.GenerativeModel (
            model_name = "models/gemini-1.5-flash",
            generation_config = {
                "temperature": 0
            }
        )
        return