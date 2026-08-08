import asyncio
from asyncio.log import logging
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import router

load_dotenv()


async def main():
    logging.basicConfig(level=logging.INFO)

    token = getenv("BOT_TOKEN")

    if not token:
        error = "No token provided"
        raise ValueError(error)
    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_router(router)

    print("🚀🚀🚀 Start bot 🚀🚀🚀")
    try:
        await dp.start_polling(bot)  # [9]
    finally:
        print("⛔⛔⛔ Bot stopped ⛔⛔⛔")


if __name__ == "__main__":
    asyncio.run(main())
