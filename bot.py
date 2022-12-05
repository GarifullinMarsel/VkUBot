from vkwave.bots import SimpleLongPollUserBot

from config import TOKEN
from blueprints import (
    quote_router,
    wiki_router,
    interpreter_router,
    YouTube_router,
)

bot = SimpleLongPollUserBot(TOKEN)
bot.dispatcher.add_router(quote_router)
bot.dispatcher.add_router(wiki_router)
bot.dispatcher.add_router(interpreter_router)
bot.dispatcher.add_router(YouTube_router)

bot.run_forever()     