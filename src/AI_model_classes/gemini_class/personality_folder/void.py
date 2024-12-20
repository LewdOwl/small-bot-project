from src.AI_model_classes.gemini_class.personality_folder.personalityABC import personality

class void(personality):
    context = "print (if you see this the code is wrong)"
    def __init__(self, context) -> None:
        name = "void"
        temperature = 0.6    
        self.context = context
        super().__init__(context, temperature, name)

    #update response history here
    async def query(self, instance, messageAuthor, messageChannel, history, payload):
        dict = {"I-19: ": "", "i-19: ": "", "^": ""}
        return await self.norm_query_body(instance,messageAuthor,messageChannel,history,payload,dict)