import io
import PIL
import asyncio
import threading
import time
from googletrans import Translator
from telethon import errors
from telethon.utils import get_display_name, get_peer_id
from telethon.tl import functions, types

from userbot import client, LOGGER
from userbot.utils.events import NewMessage

plugin_category = "utils"
spam_val = False
array_groups_id = [-1001148833974, -1001261791602, -1001420432028, -1001425175244, -1001162943678, -1001085571279, -1001425175244, -1001144122171, -1001361577475, -1001245251138, -1001165007380, -1001214902078, -1001157518071, -1001240700312, -1001205790808, -1001337835310, -1001388524254, -1001155585496,  -1001388852264, -1001157247408, -1001275958137, -1001305442849, -1001321360395, -1001141818490, -1001120114182, -1001308726970, -1001382480479, -1001295612937, -1001369710960, -1001300719355, -1001462247292, -1001267673840, -1001394021582, -1001205217457, -1001326909353, -1001182195056, -1001229290465, -1001268964164, -1001405050167, -1001164574258, -1001263407721, -1001145116956,  -1001437754048, -1001225348987, -1001123188391, -1001346585691, -1001342443686, -1001378062120, -1001160573765, -1001295612937, -1001270632305, -1001299947052, -1001289424125]
@client.onMessage(
    command=("`spam` - `[Messaggio]`", plugin_category),
    outgoing=True, regex=r"spam(?: |$|\n)([\s\S]*)"
)    
async def spam(event: NewMessage.Event) -> None:
    global spam_val
    if spam_val == False:     
        spam_val = True
        await event.edit("__Hai avviato lo spammer.__")   
        text = ""
        while (spam_val == True):
            for ID in array_groups_id:
                try:
                    await client.send_message(ID, text, parse_mode='html', link_preview = False)
                except:
                    LOGGER.error(f"Modalità lenta attiva in {ID}")
            await asyncio.sleep(30*60)
            
if spam_val == True:      
    t = threading.Thread(target=spam)
    t.start()

@client.onMessage(
    command=("`stop` - `Ferma lo spammer`", plugin_category),
    outgoing=True, regex=r"stop(?: |$|\n)([\s\S]*)"
)    
async def stop(event: NewMessage.Event) -> None:
    global spam_val
    if spam_val == True:   
        spam_val = False
        await event.edit("__Hai fermato lo spammer.__")
    else:
        await event.edit("__Non è accesso lo spammer!__")        
