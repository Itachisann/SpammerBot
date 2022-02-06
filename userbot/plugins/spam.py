import asyncio
import threading

from userbot import LOGGER, client
from userbot.core.events import NewMessage
from params import array_groups_id, spam_message, mode, link_preview, tag_message, every

plugin_category = "utils"
spam_val = False


@client.createCommand(
    command=("`spam` - `Inizia lo spam`", plugin_category),
    outgoing=True, regex=r"spam(?: |$|\n)([\s\S]*)"
)
async def spam(event: NewMessage.Event) -> None:
    global spam_val
    if spam_val == False:
        spam_val = True
        await event.edit("__Hai avviato lo spammer.__")
        while (spam_val == True):
            if tag_message == False:
                for ID in array_groups_id:
                    try:
                        await client.send_message(ID, spam_message, parse_mode=mode, link_preview=link_preview)
                    except:
                        LOGGER.error(f"Modalità lenta attiva in {ID}")
            else:
                for ID in array_groups_id:
                    try:
                        async for x in event.client.iter_participants(ID, 10000):
                            text = spam_message
                            text += f"[\u2063](tg://user?id={x.id})"
                        await client.send_message(ID, text, parse_mode=mode, link_preview=link_preview)
                    except:
                        LOGGER.error(f"Modalità lenta attiva in {ID}")
            await asyncio.sleep(every*60)

if spam_val == True:
    t = threading.Thread(target=spam)
    t.start()


@client.createCommand(
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
