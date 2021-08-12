
import re
from typing import Union

from telethon.tl import types
from telethon.utils import get_peer_id

from ..utils.events import NewMessage


class Parser:
    """Parse UserFull, ChannelFull and ChatFull objects."""

    @staticmethod
    async def parse_full_user(
        usr_obj: types.UserFull,
        event: NewMessage.Event
    ) -> str:
        """Human-friendly string of an User obj's attributes"""
        user = usr_obj.user

        user_id = get_peer_id(user.id)
        is_self = user.is_self
        contact = user.contact
        mutual_contact = user.mutual_contact
        deleted = user.deleted
        is_bot = user.bot
        verified = user.verified
        restricted = user.restricted
        support = user.support
        scam = user.scam
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        dc_id = user.photo.dc_id if user.photo else None
        common_chats_count = usr_obj.common_chats_count
        blocked = usr_obj.blocked
        about = usr_obj.about
        total_pics = (await event.client.get_profile_photos(user_id)).total

        text = ""#"<b>USER</b>\n\n"
        if first_name:
            text += f"\n  <b>👨🏻‍🔧 Nome:</b> {first_name}"
        if last_name:
            text += f"\n  <b>🤵🏻 Cognome:</b> {last_name}"
        if username:
            text += f"\n  <b>🌐 Username:</b> @{username}"
        text += f'  <b>\n  🆔 ID:</b> <a href="tg://user?id={user_id}">{user_id}</a>'
        if is_bot:
            text += f"\n  <b>🤖 Bot:</b> ✅"
        else:
            text += f"\n  <b>🤖 Bot:</b> ❌"
        if common_chats_count:
            text += f"\n  <b>💬 Chat In Comune:</b> {common_chats_count}"
        if dc_id:
            text += f"\n  <b>🔗 DC:</b> <code>{dc_id}</code>"
        if about:
            about = re.sub(r'(@\w{5,32})', r'`\1`', about, count=0)
            text += re.sub(r'`{2}', r'', f"\n  <b>📕 Bio:\n </b> <code>{about}</code>")
        return text

    @staticmethod
    async def parse_full_chat(
        chat_obj: Union[types.ChatFull, types.ChannelFull],
        event: NewMessage.Event
    ) -> str:
        """Human-friendly string of a Chat/Channel obj's attributes"""
        full_chat = chat_obj.full_chat
        chats = chat_obj.chats[0]
        profile_pic = full_chat.chat_photo

        if isinstance(full_chat, types.ChatFull):
            obj_type = "CHAT"
            participants = len(chats.participants)
        else:
            obj_type = "CHANNEL"
            participants = full_chat.participants_count
            online = full_chat.online_count
        chat_id = get_peer_id(full_chat.id)
        title = chats.title
        username = chats.username
        about = full_chat.about
        bots = len(full_chat.bot_info)

        text = ""# f"<b>{obj_type}</b>\n"
        if title:
            text += f"\n  <b>👨🏻‍🔧 Nome:</b> `{title}`"
        if username:
            text += f"\n  <b>🌐 Username:</b> @{username}"
            text += f'  <b>\n  🆔 ID:</b> <a href="tg://resolve?domain={username}">{chat_id}</a>'
        else:
            text += f"\n  <b>🆔 ID:</b> <code>{chat_id}</code>"
        if participants:
            text += f"\n  <b>🔗 Partecipanti:</b> `{participants}`"
        if bots:
            text += f"\n  <b>🤖 Bots:</b> <code>{bots}</code>"      
        if obj_type == "CHANNEL":
            if online:
                text += f"\n  <b>📯 Online:</b> <code>{online}</code>"
        if about:
            about = re.sub(r'(@\w{5,32})', r'`\1`', about, count=0)
            text += re.sub(r'`{2}', r'', f"\n  <b>📕 Bio:\n</b> <code>{about}</code>")                
        return text
