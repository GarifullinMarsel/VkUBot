from vkwave.bots import (
    DefaultRouter,
    SimpleUserEvent,
    simple_user_handler,
    CommandsFilter,
)
from vkwave.bots.core.dispatching.filters.builtin import EventTypeFilter, MessageEventUser
from vkwave.bots.utils import DocUploader
from vkwave.client import AIOHTTPClient
from vkwave.api import API
from config import TOKEN
from pytube import YouTube
import asyncio
import os 

api = API(clients=AIOHTTPClient(), tokens=TOKEN)
uploader = DocUploader(api.get_context())
YouTube_router = DefaultRouter()


def save(link:str) -> str:
    yt = YouTube(link)
    stream = yt.streams.get_by_itag(22)
    return stream.download(os.path.dirname(__file__))

@simple_user_handler(YouTube_router, EventTypeFilter(MessageEventUser), CommandsFilter("save", prefixes="/"))
async def main(event:SimpleUserEvent):
    path = await asyncio.to_thread(save, "".join(event.text.split()[1:]))
    print(path)
    attachment_video = await uploader.get_attachment_from_path(file_path=path, peer_id=event.peer_id)
    await event.reply(attachment=attachment_video)