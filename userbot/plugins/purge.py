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


from userbot import client
from userbot.utils.helpers import get_chat_link
from userbot.utils.events import NewMessage


plugin_category = "user"


@client.onMessage(
    command=("`purge` - `Rimuovi messaggi`", "admin"), require_admin=True,
    outgoing=True, regex=r"purge(?: |$)(.*)"
)
async def purge(event: NewMessage.Event) -> None:
    if (
        (event.is_channel or event.is_group) and
        not (event.chat.creator or event.chat.admin_rights.delete_messages)
    ):
        await event.answer(
            "`Non hai messaggi da elimintare qui!`"
        )
        return

    entity = await event.get_chat()
    _, kwargs = await client.parse_arguments(event.matches[0].group(1) or '')
    amount = kwargs.get('amount', None)
    skip = kwargs.get('skip', 0)

    if not event.reply_to_msg_id and not amount:
        await event.answer("__Rispondi dal messaggio da cui cominciare!__", self_destruct=2)
        return

    reverse = True if event.reply_to_msg_id else False
    messages = await client.get_messages(
        entity,
        limit=int(amount) + skip if amount else None,
        max_id=event.message.id,
        offset_id=await _offset(event),
        reverse=reverse
    )
    messages = messages[skip:]

    await client.delete_messages(entity, messages)
    extra = await get_chat_link(entity)
    await event.answer(
        f"`Eliminati {len(messages)} messaggi!`", self_destruct=1,
        log=("purge", f"Purged {len(messages)} message(s) in {extra}")
    )


@client.onMessage(
    command=("`del` - `Rimuovi tutti i tuoi messaggi da una chat`", plugin_category),
    outgoing=True, regex=r"del(?: |$)(.*)"
)
async def delme(event: NewMessage.Event) -> None:

    entity = await event.get_chat()
    _, kwargs = await client.parse_arguments(event.matches[0].group(1) or '')
    amount = kwargs.get('amount', None)
    skip = kwargs.get('skip', 0)

    if not amount:
        amount = 1 if not event.reply_to_msg_id else None

    reverse = True if event.reply_to_msg_id else False
    messages = await client.get_messages(
        entity,
        limit=int(amount) + skip if amount else None,
        max_id=event.message.id,
        offset_id=await _offset(event),
        reverse=reverse,
        from_user="me"
    )
    messages = messages[skip:]

    await client.delete_messages(entity, messages)
    await event.answer(
        f"`Hai eliminato con successo {len(messages)} tuoi messaggi!`",
        self_destruct=2,
    )


async def _offset(event: NewMessage.Event) -> int:
    if event.reply_to_msg_id:
        return event.reply_to_msg_id - 1
    return event.message.id
