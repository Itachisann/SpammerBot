import re
from typing import Tuple

from userbot import client
from userbot.core.events import NewMessage

plugin_category: str = "helper"
split_exp: re.Pattern = re.compile(r'\||\/')


@client.createCommand(
    command=("`help`", plugin_category), builtin=True,
    outgoing=True, regex=r"help"
)
async def helper(event: NewMessage.Event) -> None:
    arg = event.matches[0].group(0)
    enabled = await solve_commands(client.commands)
    if arg:
        text = "**🌍 Lista Comandi Spammer🌍**\n\n"
        text += "\n".join([f'.{name}' for name in sorted(enabled)])
    await event.respond(text)


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
