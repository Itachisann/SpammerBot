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


import os.path
import re
from typing import Tuple

from userbot import client
from userbot.utils.events import NewMessage


plugin_category: str = "helper"
link: str = "https://tg-userbot.readthedocs.io/en/latest/userbot/commands.html"
chunk: int = 5
split_exp: re.Pattern = re.compile(r'\||\/')


@client.onMessage(
    command=("`help`", plugin_category), builtin=True,
    outgoing=True, regex=r"help"
)
async def helper(event: NewMessage.Event) -> None:
    arg = event.matches[0].group(0)
    enabled, senabled = await solve_commands(client.commands)
    disabled, sdisabled = await solve_commands(client.disabled_commands)
    categories = client.commandcategories
    prefix = client.prefix or '.'
    if arg:
      text = "**🌍 Lista Comandi 🌍**\n\n"
      text += "\n".join([f'.{name}' for name in sorted(enabled)])
    await event.answer(text)


async def solve_commands(commands: dict) -> Tuple[dict, dict]:
    new_dict: dict = {}
    com_tuples: dict = {}
    for com_names, command in commands.items():
        splat = split_exp.split(com_names)
        if splat:
            for n in splat:
                com_tuples[n] = command
            new_dict[''.join(splat)] = command
        else:
            new_dict[com_names] = command
    return new_dict, com_tuples
