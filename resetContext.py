from meta_ai_api import MetaAI
from datetime import datetime
from log import log

async def resetContext(message, sGuildmap, context, condition):
    if isinstance(sGuildmap["instance"],int):
        sGuildmap["instance"] = MetaAI()                #if not ini, make one
        await log(message, "created a new meta AI instance")
        sGuildmap["instance"].prompt(message = context)
    else:
        timeDiff = datetime.now() - sGuildmap["lastMessageTime"]
        if condition == True or (sGuildmap["messageCount"] >= 50 or timeDiff.days >= 1):   # reset condition
            del sGuildmap["instance"]
            sGuildmap["instance"] = MetaAI()
            await log(message, "caused a reset")
            sGuildmap["instance"].prompt(message= context)
            sGuildmap["messageCount"] = 1