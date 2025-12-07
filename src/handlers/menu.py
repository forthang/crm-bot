from aiogram import Router, F
from aiogram.types import Message
from src.keyboards.main_kb import get_main_keyboard
from src.locales import t, all_t
from src.database.requests import get_user_settings

menu_router = Router()

# Этот роутер в текущей конфигурации (в main.py) не используется,
# но был исправлен для поддержки локализации.

@menu_router.message(F.text.in_(all_t("btn_main_menu"))) # Предполагается ключ "btn_main_menu"
@menu_router.message(F.text == "/menu")
async def show_menu(message: Message):
    lang, _ = await get_user_settings(message.from_user.id)
    await message.answer(t("main_menu_title", lang), reply_markup=get_main_keyboard(lang))

# Заглушки для кнопок, которые мы сделаем позже
@menu_router.message(F.text.in_(all_t("btn_schedule"))) # Используем существующий ключ
async def calendar_stub(message: Message):
    lang, _ = await get_user_settings(message.from_user.id)
    await message.answer(t("calendar_stub", lang)) # Ключ "calendar_stub"

@menu_router.message(F.text.in_(all_t("btn_ai_helper"))) # Предполагается ключ "btn_ai_helper"
async def ai_stub(message: Message):
    lang, _ = await get_user_settings(message.from_user.id)
    await message.answer(t("ai_helper_stub", lang)) # Ключ "ai_helper_stub"