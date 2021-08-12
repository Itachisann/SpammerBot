import io
import PIL
import asyncio

from googletrans import Translator
from telethon import errors
from telethon.utils import get_display_name, get_peer_id
from telethon.tl import functions, types

from userbot import client, LOGGER
from userbot.utils.events import NewMessage

plugin_category = "utils"
spam_val = False

@client.onMessage(
    command=("`spam` - `[Messaggio]`", plugin_category),
    outgoing=True, regex=r"spam(?: |$|\n)([\s\S]*)"
)    
async def spam(event: NewMessage.Event) -> None:
    global spam_val
    if spam_val == False:     
        spam_val = True
        await event.respond("__Hai avviato lo spammer.__")   
        text = ''
        while (spam_val == True):
            await client.send_message(-1001462247292, text, parse_mode='html')
            await client.send_message(-1001267673840, text, parse_mode='html')
            await client.send_message(-1001394021582, text, parse_mode='html')
            await client.send_message(-1001205217457, text, parse_mode='html')
            await client.send_message(-1001326909353, text, parse_mode='html')
            await client.send_message(-1001182195056, text, parse_mode='html')
            await client.send_message(-1001229290465, text, parse_mode='html')
            await client.send_message(-1001268964164, text, parse_mode='html')
            await client.send_message(-1001405050167, text, parse_mode='html')
            await client.send_message(-1001164574258, text, parse_mode='html')
            await client.send_message(-1001263407721, text, parse_mode='html')
            await client.send_message(-1001145116956, text, parse_mode='html')
            await client.send_message(-1001437754048, text, parse_mode='html')
            await client.send_message(-1001225348987, text, parse_mode='html')
            await client.send_message(-1001123188391, text, parse_mode='html')
            await client.send_message(-1001346585691, text, parse_mode='html')
            await client.send_message(-1001342443686, text, parse_mode='html')
            await client.send_message(-1001378062120, text, parse_mode='html')
            await client.send_message(-1001160573765, text, parse_mode='html')
            await client.send_message(-1001295612937, text, parse_mode='html')
            await client.send_message(-1001270632305, text, parse_mode='html')
            await client.send_message(-1001299947052, text, parse_mode='html')
            await client.send_message(-1001289424125, text, parse_mode='html')
            await client.send_message(-1001325753750, text, parse_mode='html')
            await asyncio.sleep(30*60)
    
    
@client.onMessage(
    command=("`stop` - `[Tempo in minuti][Messaggio]`", plugin_category),
    outgoing=True, regex=r"stopspam(?: |$|\n)([\s\S]*)"
)    

async def stop(event: NewMessage.Event) -> None:
    global spam_val
    if spam_val == true:   
        spam_val = False
        await event.respond("__Hai fermato lo spammer.__")
    else:
        await event.respond("__Non è accesso lo spammer!__")        
