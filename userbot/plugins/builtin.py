
from userbot import client
from userbot.core.events import NewMessage
from userbot.core.helpers import restart


@client.createCommand(
    command=("`spammer` `(Riavvia l'userbot)`", 'misc'),
    outgoing=True, regex='spammer$', builtin=True
)
async def restarter(event: NewMessage.Event) -> None:
    await restart(event)
