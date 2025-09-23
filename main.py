import aiogram
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import config, LOG_FILE
import logging
import asyncio

from buttons.buttons import router as buttons_router
from buttons.buttons import set_default_commands




bot = Bot(token = config.BOT_API_KEY.get_secret_value())
dp = Dispatcher()

# @dp.message(Command("start"))
# async def start_command(message: Message):
#     await message.reply("Hello! I'm your bot.")

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers={
            logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        }
    )

    await set_default_commands(bot)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")