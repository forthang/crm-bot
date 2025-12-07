from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.locales import t

def get_reminder_kb(call_id: int, lang: str = "en"):
    """Keyboard for the reminder message."""
    builder = InlineKeyboardBuilder()
    builder.button(text=t("btn_mark_done", lang), callback_data=f"call_done_{call_id}")
    builder.button(text=t("btn_cancel_call", lang), callback_data=f"call_cancel_{call_id}")
    return builder.as_markup()

def get_post_call_kb(client_id: int, lang: str = "en"):
    """Keyboard for the post-call follow-up."""
    builder = InlineKeyboardBuilder()
    builder.button(text=t("btn_change_status", lang), callback_data=f"change_status_{client_id}")
    builder.button(text=t("btn_edit_notes", lang), callback_data=f"edit_notes_{client_id}")
    builder.button(text=t("btn_no_changes", lang), callback_data="no_changes")
    builder.adjust(1)
    return builder.as_markup()
