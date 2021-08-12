


import datetime
import io
import logging
import os
import sys

from userbot import client, LOGGER, loggingHandler
from userbot.utils.events import NewMessage
from userbot.utils.helpers import restart

@client.onMessage(
    command=("`spammer` `(Riavvia l'userbot)`", 'misc'),
    outgoing=True, regex='spammer$', builtin=True
)
async def restarter(event: NewMessage.Event) -> None:
    await restart(event)


