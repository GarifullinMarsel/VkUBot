from vkwave.bots import SimpleLongPollUserBot

from config import TOKEN
from blueprints import (
    quote_router,
)

bot = SimpleLongPollUserBot(TOKEN)
bot.dispatcher.add_router(quote_router)

bot.run_forever()     