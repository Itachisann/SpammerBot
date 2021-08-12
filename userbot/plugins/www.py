
import asyncio
import concurrent
import sys
from typing import Tuple

from speedtest import Speedtest

from telethon.tl import functions

from userbot import client
from userbot.utils.helpers import get_chat_link, format_speed
from userbot.utils.events import NewMessage


plugin_category = "www"
DCs = {
    1: "149.154.175.50",
    2: "149.154.167.51",
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.149"
}
testing = "`Speedtest cominciato` [🇮🇹]"
download = "`Download: %0.2f %s%s/s`"
upload = "`Upload: %0.2f %s%s/s`"



@client.onMessage(
    command=("`speedtest` - `Esegui uno speedtest`", plugin_category),
    outgoing=True, regex=r"speedtest(?: |$)(bit|byte)?s?$"
)
async def speedtest(event: NewMessage.Event) -> None:
    unit = ("bit", 1)
    arg = event.matches[0].group(1)
    if arg and arg.lower() == "byte":
        unit = ("byte", 8)

    s = Speedtest()
    speed_event = await event.answer(testing % s.results.client)
    await _run_sync(s.get_servers)


    await _run_sync(s.download)
    down, unit0, unit1 = await format_speed(s.results.download, unit)
    text = (f"{speed_event.text}\n{download % (down, unit0, unit1)}")
    speed_event = await event.answer(text)

    await _run_sync(s.upload)
    up, unit0, unit1 = await format_speed(s.results.upload, unit)
    text = (f"{speed_event.text}\n{upload % (up, unit0, unit1)}")
    extra = await get_chat_link(event, event.id)
    await event.answer(
        text,
        log=("speedtest", f"Performed a speedtest in {extra}.")
    )


async def _sub_shell(cmd: str) -> Tuple[str, str]:
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    return stdout.decode("UTF-8"), stderr.decode("UTF-8")


async def _run_sync(func: callable):
    return await client.loop.run_in_executor(
        concurrent.futures.ThreadPoolExecutor(), func
    )
