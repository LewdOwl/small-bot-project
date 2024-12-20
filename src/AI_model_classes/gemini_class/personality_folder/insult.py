from src.AI_model_classes.gemini_class.personality_folder.personalityABC import personality

class insult(personality):
    context = "print (if you see this the code is wrong)"

    def __init__(self,context) -> None:
        name = "insult"
        temperature = 2.0
        self.context = context
        super().__init__(context, temperature, name)

    async def query(self, instance, messageAuthor, messageChannel, history, payload):

        return await self.norm_query_body(instance,messageAuthor,messageChannel,history,payload,None)