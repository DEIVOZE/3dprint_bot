from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Создание сетки клавиатуры
def get_main_keyboard(is_paused: bool = False) -> InlineKeyboardMarkup:
    if is_paused:
        pause_text = "Возобновить ▶️"
        pause_cd = "cd_play"
    else:
        pause_text = "Остановить ⏸️"
        pause_cd = "cd_pause"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=pause_text, callback_data=pause_cd),
                InlineKeyboardButton(text="Завершить 🛑", callback_data="cd_stop"),
            ],
            [
                InlineKeyboardButton(text="Снимок 📷", callback_data="cd_cam"),
                InlineKeyboardButton(text="Больше ⚙️", callback_data="cd_more"),
            ],
        ]
    )
    return kb


def get_start_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Статус принтера 📊", callback_data="cd_status"
                )
            ],
        ]
    )
    return kb
