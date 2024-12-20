
async def emojiReaction(message, emojiLookUp, emojiMap):
    if emojiLookUp in emojiMap:
        await message.add_reaction(f"<:{emojiLookUp}:{emojiMap[emojiLookUp]}>")
    else:
        await message.add_reaction(f"<:default:{emojiMap['default']}>")
    return