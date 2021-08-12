# TG-UserBot - A modular Telegram UserBot script for Python.
# Copyright (C) 2019  Kandarp <https://github.com/kandnub>
#
# TG-UserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TG-UserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TG-UserBot.  If not, see <https://www.gnu.org/licenses/>.


import datetime
import io
import logging
import os
import sys

from userbot import client, LOGGER, loggingHandler
from userbot.utils.events import NewMessage
from userbot.utils.helpers import restart


@client.onMessage(
    command=('`ping` `(Ottieni il tuo ping)`', 'www'),
    outgoing=True, regex='ping$', builtin=True
)
async def ping(event: NewMessage.Event) -> None:
    """
    Check how long it takes to get an update and respond to it.


    `{prefix}ping`
    """
    start = datetime.datetime.now()
    await event.answer("**Ping**")
    duration = (datetime.datetime.now() - start)
    milliseconds = duration.microseconds / 1000
    await event.answer(f"**Ping:** `{milliseconds}ms`")


@client.onMessage(
    command=("`restart` `(Riavvia l'userbot)`", 'misc'),
    outgoing=True, regex='restart$', builtin=True
)
async def restarter(event: NewMessage.Event) -> None:
    await restart(event)


