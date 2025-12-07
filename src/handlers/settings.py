from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src.database.requests import get_user_settings, update_user_settings
from src.locales import t, all_t
from src.keyboards.main_kb import get_main_keyboard

settings_router = Router()

class ReminderState(StatesGroup):
    waiting_for_time = State()

# Language selection buttons
lang_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en")],
    [InlineKeyboardButton(text="🇫🇷 Français", callback_data="set_lang_fr")]
])

# Timezone selection buttons (Main ones)
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
    lang, tz, delay = await get_user_settings(message.from_user.id)
    
    text = t("settings_title", lang=lang, tz=tz, delay=delay)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_change_lang", lang), callback_data="change_lang")],
        [InlineKeyboardButton(text=t("btn_change_tz", lang), callback_data="change_tz")],
        [InlineKeyboardButton(text=t("btn_change_reminder", lang), callback_data="change_reminder")]
    ])
    
    await message.answer(text, reply_markup=kb)

# --- Language Change ---
@settings_router.callback_query(F.data == "change_lang")
async def ask_lang(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    await callback.message.edit_text(t("choose_lang", lang), reply_markup=lang_kb)
    await callback.answer()

@settings_router.callback_query(F.data.startswith("set_lang_"))
async def set_lang(callback: CallbackQuery):
    new_lang = callback.data.split("_")[2] # set_lang_en -> en
    
    await update_user_settings(callback.from_user.id, lang=new_lang)
    
    # Edit the old message to confirm the change
    await callback.message.edit_text(t("lang_set", new_lang), reply_markup=None)
    
    # Send a new message with the new main keyboard
    await callback.message.answer("...", reply_markup=get_main_keyboard(new_lang))
    
    await callback.answer()

# --- Timezone Change ---
@settings_router.callback_query(F.data == "change_tz")
async def ask_tz(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    await callback.message.edit_text(t("choose_tz", lang), reply_markup=tz_kb)
    await callback.answer()

@settings_router.callback_query(F.data.startswith("set_tz_"))
async def set_tz(callback: CallbackQuery):
    new_tz = callback.data.replace("set_tz_", "") 
    
    await update_user_settings(callback.from_user.id, tz=new_tz)
    
    lang, _, _ = await get_user_settings(callback.from_user.id)
    await callback.message.edit_text(t("tz_set", lang, tz=new_tz))
    await callback.answer()

# --- Reminder Time Change ---
@settings_router.callback_query(F.data == "change_reminder")
async def ask_reminder_time(callback: CallbackQuery, state: FSMContext):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    await callback.message.edit_text(t("ask_reminder_time", lang))
    await state.set_state(ReminderState.waiting_for_time)
    await callback.answer()

@settings_router.message(ReminderState.waiting_for_time)
async def set_reminder_time(message: Message, state: FSMContext):
    lang, _, _ = await get_user_settings(message.from_user.id)
    try:
        minutes = int(message.text)
        await update_user_settings(message.from_user.id, delay=minutes)
        await message.answer(t("reminder_time_set", lang, minutes=minutes))
        await state.clear()
    except ValueError:
        await message.answer(t("invalid_reminder_time", lang))