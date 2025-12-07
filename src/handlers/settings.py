from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from src.database.requests import get_user_settings, update_user_settings
from src.locales import t, all_t
from src.keyboards.main_kb import get_main_keyboard

settings_router = Router()

# Кнопки выбора языка
lang_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")],
    [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en")],
    [InlineKeyboardButton(text="🇫🇷 Français", callback_data="set_lang_fr")]
])

# Кнопки выбора пояса (Основные)
tz_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Moscow (UTC+3)", callback_data="set_tz_Europe/Moscow"),
        InlineKeyboardButton(text="Paris (CET)", callback_data="set_tz_Europe/Paris")
    ],
    [
        InlineKeyboardButton(text="London (UTC+0)", callback_data="set_tz_Europe/London"),
        InlineKeyboardButton(text="New York (UTC-5)", callback_data="set_tz_America/New_York")
    ]
])

@settings_router.message(F.text.in_(all_t("btn_settings")))
async def open_settings(message: Message):
    lang, tz = await get_user_settings(message.from_user.id)
    
    text = t("settings_title", lang=lang, tz=tz)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_change_lang", lang), callback_data="change_lang")],
        [InlineKeyboardButton(text=t("btn_change_tz", lang), callback_data="change_tz")]
    ])
    
    await message.answer(text, reply_markup=kb)

# --- Смена языка ---
@settings_router.callback_query(F.data == "change_lang")
async def ask_lang(callback: CallbackQuery):
    lang, _ = await get_user_settings(callback.from_user.id)
    await callback.message.edit_text(t("choose_lang", lang), reply_markup=lang_kb)
    await callback.answer()

@settings_router.callback_query(F.data.startswith("set_lang_"))
async def set_lang(callback: CallbackQuery):
    new_lang = callback.data.split("_")[2] # set_lang_ru -> ru
    
    await update_user_settings(callback.from_user.id, lang=new_lang)
    
    # Редактируем старое сообщение, подтверждая смену
    await callback.message.edit_text(t("lang_set", new_lang), reply_markup=None)
    
    # Отправляем новое сообщение с новой главной клавиатурой
    await callback.message.answer("...", reply_markup=get_main_keyboard(new_lang))
    
    await callback.answer()

# --- Смена пояса ---
@settings_router.callback_query(F.data == "change_tz")
async def ask_tz(callback: CallbackQuery):
    lang, _ = await get_user_settings(callback.from_user.id)
    await callback.message.edit_text(t("choose_tz", lang), reply_markup=tz_kb)
    await callback.answer()

@settings_router.callback_query(F.data.startswith("set_tz_"))
async def set_tz(callback: CallbackQuery):
    new_tz = callback.data.replace("set_tz_", "") 
    
    await update_user_settings(callback.from_user.id, tz=new_tz)
    
    lang, _ = await get_user_settings(callback.from_user.id)
    await callback.message.edit_text(t("tz_set", lang, tz=new_tz))
    await callback.answer()