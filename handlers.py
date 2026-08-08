import asyncio
from os import getenv

from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards import get_confirm_keyboard, get_main_keyboard, get_start_keyboard

CONFIRM_MESSAGES = {
    "stop": "⚠️ <b>Вы уверены, что хотите полностью ОСТАНОВИТЬ печать?</b>\n\nПроцесс будет отменен безвозвратно.",
    "pause": "⏸ <b>Приостановить печать?</b>\n\nПринтер поставит процесс на паузу и отведет сопло.",
}

router = Router()


@router.message(Command("start"))
async def start_mes(message: Message):
    is_allowed = str(message.from_user.id) in getenv("ALLOWED_USER_IDS", "").split(",")
    if is_allowed:
        user_name = html.quote(message.from_user.first_name)
        text = (
            f"Привет, <b>{user_name}</b>!\n\n"
            f"Я бот для дистанционного управления процессом печати на 3д принтере.\n"
            f"Для получения сведений о принтере, нажмите кнопку <b>ниже</b>"
        )

        await message.answer(
            text=text, reply_markup=get_start_keyboard(), parse_mode="HTML"
        )
    else:
        await message.answer("К сожалению, вы неавторизованный пользователь")


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


@router.callback_query(F.data.startswith("confirm:"))
async def cofirmation_action(callback: CallbackQuery):
    await callback.answer()

    action = callback.data.split(":")[1]

    text = CONFIRM_MESSAGES.get(
        action, "⚠️ <b>Вы уверены, что хотите выполнить это действие?</b>"
    )

    await callback.message.edit_text(
        text=text, reply_markup=get_confirm_keyboard(action), parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("yes:"))
async def yes_action(callback: CallbackQuery):
    await callback.answer()

    action = callback.data.split(":")[1]

    if action == "stop":
        await callback.message.edit_text(text="Печать завершена 🛑")
    else:
        await callback.message.edit_text(text="Печать остановлена ⏸️")

    await asyncio.sleep(2)

    await show_status_info(callback)
