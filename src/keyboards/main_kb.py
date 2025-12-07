from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.locales import t

def get_main_keyboard(lang: str = "en"):
    """
    Main keyboard.
    The button text depends on the selected language (lang).
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t("btn_clients", lang)),
                KeyboardButton(text=t("btn_add", lang))
            ],
            [
                KeyboardButton(text=t("btn_schedule", lang)),
                KeyboardButton(text=t("btn_settings", lang)),
                KeyboardButton(text=t("btn_stats", lang))
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Menu..."
    )

def get_cancel_keyboard(lang: str = "en"):
    """Cancel button"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t("btn_cancel", lang))]],
        resize_keyboard=True
    )