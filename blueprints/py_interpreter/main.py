from vkwave.bots import (
    DefaultRouter,
    SimpleUserEvent,
    simple_user_handler,
    CommandsFilter,
)
from vkwave.bots.core.dispatching.filters.builtin import EventTypeFilter, MessageEventUser
from vkwave.api import API
from config import TOKEN
from vkwave.bots.core.dispatching import filters 
import html 
import aiofiles
import asyncio


interpreter_router = DefaultRouter()


async def start_program(code:str) -> str:
    async with aiofiles.open("main.py", "w") as file:
        await file.write(code)
        result = await asyncio.create_subprocess_shell(
            "python main.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await result.communicate()
    return stdout.decode() if stdout else stderr.decode()


@simple_user_handler(interpreter_router, EventTypeFilter(MessageEventUser), CommandsFilter("py", prefixes="/"), filters.FromMeFilter(True))
async def main(event:SimpleUserEvent):
    code = html.unescape(event.text[3:]).replace("<br>", "\n").replace("~", " ")
    result = await start_program(code)
    print(result)
    await event.edit(f"Code:\n{code}Result:\n{result}")