import asyncio  # [1]
from os import getenv  # [1]

from aiogram import Bot, Dispatcher, F, Router, html  # [1]
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.enums import parse_mode
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, message
from dotenv import load_dotenv

from keyboards import get_main_keyboard, get_start_keyboard

load_dotenv()

dp = Dispatcher()  # [2]
router = Router()


@router.message(Command("start"))
async def start_mes(message: Message):
    is_allowed = str(message.from_user.id) in getenv("ALLOWED_USER_IDS", "").split(",")
    if is_allowed:
        user_name = html.quote(message.from_user.first_name)
        text = (
            f"Привет, <b>{user_name}</b>!\n\n"
            f"Я бот для дистанционного управления процессом печати на 3д принтере\n"
            f"Для получения сведений о принтере нажмите кнопку <b>ниже</b>"
        )

        await message.answer(
            text=text, reply_markup=get_start_keyboard(), parse_mode="HTML"
        )
    else:
        await message.answer("К сожалению вы не авторизованный пользователь")


@router.callback_query(F.data == "cd_status")
async def show_status_info(callback: CallbackQuery):

    await callback.answer()

    percent_done = 45
    progressbar_done = percent_done // 10
    progressbar = (
        f"{percent_done}% [{'█' * progressbar_done}{'░' * (10 - progressbar_done)}]"
    )

    dashboard_text = (
        f"<b>Статус принтера:</b> Идет печать...\n"
        f"<b>Статус печати:</b>\n"
        f" 🔹 <b>Файл:</b> BANANA.gcode\n"
        f" 🔹 <b>Прогресс:</b> {progressbar}\n"
        f" 🔹 <b>Оставшееся время:</b> 25 мин\n"
        f" 🔹 <b>Время завершения:</b> 15:46"
    )

    await callback.message.edit_text(
        text=dashboard_text, reply_markup=get_main_keyboard(), parse_mode="HTML"
    )


async def main():
    token = getenv("BOT_TOKEN")  # [7]

    if not token:  # [7]
        error = "No token provided"  # [7]
        raise ValueError(error)  # [7]
    bot = Bot(token=token)  # [8]

    dp.include_router(router)

    print("Starting bot...")
    try:
        await dp.start_polling(bot)  # [9]
    finally:
        print("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
