import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from ai_class import ai
from meta_ai_api import MetaAI
from datetime import datetime, timedelta
from log import log

class meta_ai(ai):
    last_msg_source = " "
    context = " "
    instance = 0

    def __init__(self, instruction) -> None:
        super().__init__()          # no argument for parent class
        self.context = instruction  # get instruction

    # methods ======================================================
    async def sendSource(self, message):                                   # send source based of last msg
        await message.channel.send(self.last_msg_source)
        return
    
    async def ini(self, message):                                    # check if need to make a new instance
        currentTime = datetime.now()                       
        if isinstance(self.instance, int):
            self.instance = MetaAI()
            await log(message, "created a new meta AI instance")
            self.iniTime = currentTime
            self.instance.prompt(message = self.context)
        return
    
    async def resetCheck(self, message, condition) -> None:                          # check if it need to reset
        # so this resets either 2 day after iniTime, or 1 day of silence, or 100 message limit
        if self.resetCond(timedelta(days=2), timedelta(days=1), 100, condition):   # reset condition
            await log(message, "caused a reset")
            self.instance = 0       # ... I hate black box
            await self.ini(message)
        return
    
    
    async def query(self, message, counter) -> None:                                 #actual prompt function
        async with message.channel.typing():
            #get msg content
            userMSG = ""
            if message.content[0:4] =="=um ":
                userMSG = message.content.split("=um ",1)[1] if len(message.content) > 4 else " "
            else:
                userMSG = message.content
            self.update_msgCount_and_time()

            response = self.instance.prompt(message=self.context+ message.author.display_name + ": " + userMSG)
            self.last_msg_source = response['sources']          #update source
            response = response['message'].replace('\n', '\n')  #process raw response

            #panic fix for welsh error, maximum 5 rerolls
            if counter <= 5 and "I don’t understand" in response[:30]:
                print("welsh/other msg error trash...")
                counter+=1
                await self.query(message, counter)
                return 
            await message.channel.send(response)                #send response
        return

