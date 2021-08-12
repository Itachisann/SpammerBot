
import aiohttp
import functools
import git
import io
import PIL
import re
import requests

from telethon import utils
from telethon.tl import functions, types

from userbot import client, LOGGER
from userbot.other_funcs import misc
from userbot.utils.helpers import get_chat_link
from userbot.utils.events import NewMessage


plugin_category = "misc"
invite_links = {
    'private': re.compile(r'^(?:https?://)?(t\.me/joinchat/\w+)/?$'),
    'public': re.compile(r'^(?:https?://)?t\.me/(\w+)/?$'),
    'username': re.compile(r'^@?(\w{5,32})$')
}
usernexp = re.compile(r'@(\w{3,32})\[(.+?)\]')
nameexp = re.compile(r'\[([\w\S]+)\]\(tg://user\?id=(\d+)\)\[(.+?)\]')
dogheaders = {
    'Content-type': 'text/plain',
    'Accept': 'application/json',
    'charset': 'utf-8'
}


def removebg_post(API_KEY: str, media: bytes or str):
    image_parameter = 'image_url' if isinstance(media, str) else 'image_file'
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={image_parameter: media},
        data={'size': 'auto'},
        headers={'X-Api-Key': API_KEY},
    )
    return response



async def rmbg(event: NewMessage.Event) -> None:
    """
    Remove the background from an image or sticker.


    `{prefix}rmbg` or **{prefix}rmbg (url)**
    """
    API_KEY = client.config['api_keys'].get('api_key_removebg', False)
    if not API_KEY:
        await event.answer("`You don't have an API key set for remove.bg!`")
        return

    match = event.matches[0].group(1)
    reply = await event.get_reply_message()

    if match:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(match) as response:
                    if not (
                        response.status == 200 and
                        response.content_type.startswith('image/')
                    ):
                        await event.answer(
                            "`The provided link seems to be invalid.`"
                        )
                        return
            except aiohttp.client_exceptions.InvalidURL:
                await event.answer("`Invalid URL provided!`")
                return
            except Exception as e:
                exc = await client.get_traceback(e)
                await event.answer(f"**Unknown exception:**\n```{exc}```")
                return
        media = match
    elif reply and reply.media:
        ext = utils.get_extension(reply.media)
        acceptable = [".jpg", ".png", ".bmp", ".tif", ".webp"]
        if ext not in acceptable:
            await event.answer("`Nice try, fool!`")
            return

        await event.answer("`Downloading media...`")
        media = io.BytesIO()
        await client.download_media(reply, media)
        if ext in [".bmp", ".tif", ".webp"]:
            new_media = io.BytesIO()
            try:
                pilImg = PIL.Image.open(media)
            except OSError as e:
                await event.answer(f'`OSError: {e}`')
                return
            pilImg.save(new_media, format="PNG")
            pilImg.close()
            media.close()
            media = new_media
    else:
        await event.answer("`Reply to a photo or provide a valid link.`")
        return

    response = await client.loop.run_in_executor(
        None, functools.partial(removebg_post, API_KEY, media.getvalue())
    )
    if not isinstance(media, str):
        media.close()
    if response.status_code == 200:
        await event.delete()
        image = io.BytesIO(response.content)
        image.name = "image.png"
        await event.answer(file=image, force_document=True, reply=True)
        image.close()
    else:
        error = response.json()['errors'][0]
        code = error.get('code', False)
        title = error.get('title', 'No title?')
        body = code + ': ' + title if code else title
        text = f"`[{response.status_code}] {body}`"
        await event.answer(text)



async def resolver(event: NewMessage.Event) -> None:
    """
    Resolve an invite link or a username.


    **{prefix}resolve (invite link)**
    """
    link = event.matches[0].group(1)
    chat = None
    if not link:
        await event.answer("`Resolved the void.`")
        return
    text = f"`Couldn't resolve:` {link}"
    for link_type, pattern in invite_links.items():
        match = pattern.match(link)
        if match:
            valid = match.group(1)
            if link_type == "private":
                creatorid, cid, _ = utils.resolve_invite_link(valid)
                if not cid:
                    await event.answer(text)
                    return
                try:
                    creator = await client.get_entity(creatorid)
                    creator = await get_chat_link(creator)
                except (TypeError, ValueError):
                    creator = f"`{creatorid}`"
                text = f"**Link:** {link}"
                text += f"\n**Link creator:** {creator}\n**ID:** `{cid}`"
                try:
                    chat = await client.get_entity(cid)
                except (TypeError, ValueError):
                    break
                except Exception as e:
                    text += f"\n```{await client.get_traceback(e)}```"
                    break

                if isinstance(chat, types.Channel):
                    result = await client(
                        functions.channels.GetFullChannelRequest(
                            channel=chat
                        )
                    )
                    text += await misc.resolve_channel(event.client, result)
                elif isinstance(chat, types.Chat):
                    result = await client(
                        functions.messages.GetFullChatRequest(
                            chat_id=chat
                        )
                    )
                    text += await misc.resolve_chat(event.client, result)
                break
            else:
                try:
                    chat = await client.get_entity(valid)
                except (TypeError, ValueError):
                    continue

                if isinstance(chat, types.User):
                    text = f"**ID:** `{chat.id}`"
                    if chat.username:
                        text += f"\n**Username:** @{chat.username}"
                    text += f"\n{await get_chat_link(chat)}"

                if isinstance(chat, types.ChatForbidden):
                    text += f"\n`Not allowed to view {chat.title}.`"
                elif isinstance(chat, types.ChatEmpty):
                    text += "\n`The chat is empty.`"
                elif isinstance(chat, types.Chat):
                    text = f"**Chat:** @{valid}"
                    result = await client(
                        functions.messages.GetFullChatRequest(
                            chat_id=chat
                        )
                    )
                    text += await misc.resolve_chat(event.client, result)

                if isinstance(chat, types.ChannelForbidden):
                    text += f"\n`Not allowed to view {chat.title}.`"
                elif isinstance(chat, types.Channel):
                    text = f"**Channel:** @{valid}"
                    result = await client(
                        functions.channels.GetFullChannelRequest(
                            channel=chat
                        )
                    )
                    text += await misc.resolve_channel(event.client, result)
    await event.answer(text, link_preview=False)

