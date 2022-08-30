from vkwave.bots import (
    DefaultRouter,
    SimpleUserEvent,
    simple_user_handler,
    CommandsFilter,
)
from vkwave.bots.core.dispatching import filters
from vkwave.bots.core.dispatching.filters.base import BaseFilter, FilterResult
from vkwave.bots.core.dispatching.filters.builtin import EventTypeFilter, MessageEventUser
from vkwave.bots.core.dispatching.filters import FwdMessagesFilter
from vkwave.bots import PhotoUploader
from vkwave.client import AIOHTTPClient
from vkwave.api import API
from config import TOKEN
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
from textwrap import wrap
import re

api = API(clients=AIOHTTPClient(), tokens=TOKEN)
uploader = PhotoUploader(api.get_context())
quote_router = DefaultRouter()




class User:
    def __init__(self, data, message, avatar, event) -> None:
        self.name = f"{data.response[0].first_name} {data.response[0].last_name}"
        self.id = data.response[0].id
        self.avatar = avatar
        self.message = f"«{self._lines_formatter(message.response.items[0].reply_message.text, 35)}»"
        self.user_command = dict(re.findall(r"(-[\w]+)\s* {,10}\s*([^-{,}]+)", " ".join(user_info.event.text.split()[1:])))


    @staticmethod
    def _justify(line, width):
        gap_width, max_replace = divmod(width - len(line) + line.count(' '), line.count(' '))
        return line.replace(' ', ' ' * gap_width).replace(' ' * gap_width, ' ' * (gap_width + 1), max_replace)

    @classmethod
    def _lines_formatter(cls, text, width):
        lines = wrap(text, width, break_long_words=False)
        for i, line in enumerate(lines[:-1]):
            if len(line) <= width and line.count(' '):
                lines[i] = cls._justify(line, width)
                lines[i].rstrip()
        return '\n'.join(lines)




class Img:
    def __init__(self, user_info):
        self.user_info = user_info
        self.font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', size=50)
        if user_info.user_command.get("-t") != None:
            self.title =user_info.user_command.get("-t")
        else:
            self.title = "Цитаты великих людей."


    async def _draw(self):
        im = Image.new("RGB",(1,1),"black")
        draw = ImageDraw.Draw(im)
        w, h = draw.textsize(self.user_info.message, font=self.font)
        W, H = 1000, h + 400
        im = Image.new("RGB", (W, H),"black")
        draw = ImageDraw.Draw(im)
        draw.multiline_text((50, (H-h)/2), self.user_info.message, fill="white",font=self.font)
        title = draw.textsize(self.title, font=self.font)
        draw.multiline_text(((W-title[0])/2, 30), self.title, fill="white",font=self.font)
        draw.multiline_text((200, H-100), self.user_info.name, fill="white",font=self.font)
        im2 = self.user_info.avatar
        bigsize = im2.size[0] * 3, im2.size[1] * 3
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im2.size, Image.ANTIALIAS)
        im2.putalpha(mask)
        im.paste(im2, (50, im.height-150))
        return im
        
    async def get_bytes(self):
        b = io.BytesIO()
        (await self._draw()).save(b, 'jpeg')
        im_bytes = b.getvalue()
        return im_bytes




@simple_user_handler(quote_router, EventTypeFilter(MessageEventUser), CommandsFilter("цитата", prefixes="/"), filters.ReplyMessageFilter(True))
async def main(event:SimpleUserEvent):
    message = (await api.get_context().messages.get_by_id(message_ids=event.object.object.message_id))
    user_data = await api.get_context().users.get(user_ids=message.response.items[0].reply_message.from_id, fields="photo_100")

    async with aiohttp.ClientSession() as session:
        url = user_data.response[0].photo_100
        async with session.get(url) as resp:
            avatar = Image.open(io.BytesIO(await resp.read()))

    user = User(user_data, message, avatar, event)
    img = Img(user)

    attachment = await uploader.get_attachment_from_io(peer_id=user.id, f=io.BytesIO((await img.get_bytes())))
    await event.answer(attachment=attachment)