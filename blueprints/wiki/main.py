from logging import error
from vkwave.bots import (
    DefaultRouter,
    SimpleUserEvent,
    simple_user_handler,
    CommandsFilter,
)
from vkwave.bots.core.dispatching.filters.builtin import EventTypeFilter, MessageEventUser
from vkwave.bots import PhotoUploader
from vkwave.client import AIOHTTPClient
from vkwave.api import API
from config import TOKEN
import aiohttp

api = API(clients=AIOHTTPClient(), tokens=TOKEN)
uploader = PhotoUploader(api.get_context())
wiki_router = DefaultRouter()


async def get_data_from_wiki(data):
    async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ru.wikipedia.org/api/rest_v1/page/summary/{' '.join((data.text).split()[1:])}") as resp:
                return await resp.json()


@simple_user_handler(wiki_router, EventTypeFilter(MessageEventUser), CommandsFilter("вики", prefixes="/"))
async def main(event:SimpleUserEvent):
    try:
        text = await get_data_from_wiki(event)
        await event.reply(text["extract"])
    except Exception as err:
        await event.reply("Не удалось найти :(")