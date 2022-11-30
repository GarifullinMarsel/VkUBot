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
from vkwave.bots.core.dispatching import filters 
from io import StringIO
import sys
import html 
import time

interpreter_router = DefaultRouter()

@simple_user_handler(interpreter_router, EventTypeFilter(MessageEventUser), CommandsFilter("py", prefixes="/"), filters.FromMeFilter(True))
async def main(event:SimpleUserEvent):
    try:
        # сохраняем ссылку, чтобы потом 
        # снова отобразить вывод в консоли.
        tmp_stdout = sys.stdout
        
        # В переменной `result` будет храниться все, 
        # что отправляется на стандартный вывод
        result = StringIO()
        sys.stdout = result
        
        # Здесь все, что отправляется на стандартный вывод, 
        # будет сохранено в переменную `result`.
        
        code = " ".join(html.unescape(event.text).replace("<br>", "\n").split()[1:])
        start = time.time()
        exec(code)
        complite_time = "%s" % (start - time.time())
        # Снова перенаправляем вывод `sys.stdout` на консоль
        sys.stdout = tmp_stdout
        
        # Получаем стандартный вывод как строку!
        result_string = result.getvalue()

        await event.edit(
            f"""
            Code: 
            {code}


            Result:
            {result_string}

            Completed in {complite_time}s.
            """
        )

    except Exception as err:
        await event.edit(err)

        