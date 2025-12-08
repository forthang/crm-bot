from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.locales import t

def get_reminder_kb(call_id: int, lang: str = "en"):
    """Keyboard for the reminder message."""
    builder = InlineKeyboardBuilder()
    builder.button(text=t("btn_mark_done", lang), callback_data=f"call_done_{call_id}")
    builder.button(text=t("btn_cancel_call", lang), callback_data=f"call_cancel_{call_id}")
    return builder.as_markup()

def get_post_call_kb(call_id: int, lang: str = "en"):
    """Keyboard for the post-call follow-up."""
    builder = InlineKeyboardBuilder()
    builder.button(text=t("btn_add_call_summary", lang), callback_data=f"add_summary_{call_id}")
    builder.button(text=t("btn_no_changes", lang), callback_data="no_changes")
    builder.adjust(1)
    return builder.as_markup()
