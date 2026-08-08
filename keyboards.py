from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Создание сетки основной клавиатуры
def get_main_keyboard(is_paused: bool = False) -> InlineKeyboardMarkup:
    if is_paused:
        pause_text = "▶️ Возобновить"
        pause_cd = "cd_play"
    else:
        pause_text = "⏸️ Остановить"
        pause_cd = "confirm:pause"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=pause_text, callback_data=pause_cd),
                InlineKeyboardButton(text="🛑 Завершить", callback_data="confirm:stop"),
            ],
            [
                InlineKeyboardButton(text="📷 Снимок", callback_data="cd_cam"),
                InlineKeyboardButton(text="⚙️ Больше", callback_data="cd_more"),
            ],
            [InlineKeyboardButton(text="🔄 Обновить", callback_data="cd_refresh")],
        ]
    )
    return kb


# Создание сетки клавиатуры при старте бота
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


# Клавиатура подтверждения
def get_confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✔️ Да, уверен", callback_data=f"yes:{action}"
                ),
                InlineKeyboardButton(text="❌ Отмена", callback_data="cd_status"),
            ],
        ]
    )
    return kb
