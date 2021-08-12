

import asyncio
import inspect

from meval import meval

from userbot import client
from userbot.utils.helpers import get_chat_link
from userbot.utils.events import NewMessage


plugin_category = "calculator"


@client.onMessage(
    command=("`calc` `(Esegui operazioni)`", plugin_category),
    outgoing=True, regex=r"calc(?: |$|\n)([\s\S]*)"
)
async def calc(event: NewMessage.Event) -> None:
    expression = event.matches[0].group(1).strip()
    reply = await event.get_reply_message()
    if not expression:
        await event.answer("__Inserisci parametri validi per fare operazioni!__")
        return

    try:
        result = await meval(
            expression, globals(), client=client, event=event, reply=reply
        )
    except Exception as e:
        await event.answer(
            f"`Operazione non riuscita.`", reply=True)
        return

    extra = await get_chat_link(event, event.id)
    if result:
        if hasattr(result, 'stringify'):
            if inspect.isawaitable(result):
                result = await result.stringify()
            else:
                result = result.stringify()
    result = str(result) if result else "Questa è una risposta ovvia.."
    await event.answer(
        "```Risultato: " + result + "```",
        log=("eval", f"Successfully evaluated {expression} in {extra}!"),
        reply=True
    )
