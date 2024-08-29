from log import log
from meta_ai_api import MetaAI
from datetime import datetime

async def resetContext(message, sGuildmap, context, condition):
    if isinstance(sGuildmap["instance"],int):
        sGuildmap["instance"] = MetaAI()                #if not ini, make one
        await log(message, "created a new meta AI instance")
        sGuildmap["instance"].prompt(message = context)
    else:
        timeDiff = datetime.now() - sGuildmap["lastMessageTime"]
        if condition == True or (sGuildmap["messageCount"] >= 50 or timeDiff.days >= 1):   # reset condition
            #sGuildmap["instance"] = MetaAI()
            await log(message, "caused a reset")
            sGuildmap["instance"].prompt(message= context, new_conversation=True)
            sGuildmap["messageCount"] = 1