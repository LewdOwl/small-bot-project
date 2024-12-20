from abc import ABC, abstractmethod
import json

class personality(ABC):
    name = ""
    context = ""
    temperature = 1
    maxToken = 16384
    emojiMap = {}

    def __init__(self, context, temperature, name) -> None:
        self.name = name
        self.context = context
        self.temperature = temperature
        with open('.json','r') as file:                               # vision of poor design
            data = json.load(file)
        self.emojiMap = {item['key']: item['value'] for item in data['emoji']}
    
    # method =============
    @abstractmethod     #wrapper
    async def query (self, instance, messageAuthor, messageChannel, history, payload): 
        pass
    
    def phrase_swap(self, response, black_list_dict=None):
        if black_list_dict is not None:
            for key in black_list_dict:
                response = response.replace(key, black_list_dict[key])
        return response
    
    def setMaxToken(self,maxToken):
        self.maxToken = maxToken

    async def norm_query_body(self, instance, messageAuthor, messageChannel, history, payload, black_list_dict=None):
        response = await instance.send_message_async(payload)
        response = response.text

        # clearing trash
        response = self.phrase_swap(response,black_list_dict)
        await messageChannel.send(response) 
        
        history+= f"I-19: {response}\n"

        return history        #yep , now it returns stuff
    
