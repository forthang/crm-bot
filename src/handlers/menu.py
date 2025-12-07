from aiogram import Router, F
from aiogram.types import Message
from src.keyboards.main_kb import get_main_keyboard
from src.locales import t, all_t
from src.database.requests import get_user_settings

menu_router = Router()

# This router is not used in the current configuration (in main.py),
# but it has been corrected to support localization.

@menu_router.message(F.text.in_(all_t("btn_main_menu"))) # Assumes a "btn_main_menu" key
@menu_router.message(F.text == "/menu")
async def show_menu(message: Message):
    lang, _ = await get_user_settings(message.from_user.id)
    await message.answer(t("main_menu_title", lang), reply_markup=get_main_keyboard(lang))

# Stubs for buttons that will be implemented later
@menu_router.message(F.text.in_(all_t("btn_schedule"))) # Uses an existing key
async def calendar_stub(message: Message):
    lang, _ = await get_user_settings(message.from_user.id)
    await message.answer(t("calendar_stub", lang)) # "calendar_stub" key

@menu_router.message(F.text.in_(all_t("btn_ai_helper"))) # Assumes a "btn_ai_helper" key
async def ai_stub(message: Message):
    lang, _ = await get_user_settings(message.from_user.id)
    await message.answer(t("ai_helper_stub", lang)) # "ai_helper_stub" key