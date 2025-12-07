import os
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Импорты БД
from src.database.requests import create_call, get_client, get_user_settings
# Импорты клавиатур
from src.keyboards.clients_kb import get_client_card_kb
from src.keyboards.calendar_kb import get_days_kb, get_hours_kb, get_minutes_kb
# Импорт генератора ICS
from src.services.ics_generator import create_ics_file
# Локализация
from src.locales import t

calls_router = Router()

class AddCallState(StatesGroup):
    waiting_for_topic = State()

# ==========================================
# 1. СТАРТ: Выбор дня
# ==========================================
@calls_router.callback_query(F.data.startswith("add_call_"))
async def start_add_call(callback: CallbackQuery, state: FSMContext):
    lang, _ = await get_user_settings(callback.from_user.id)
    client_id = int(callback.data.split("_")[2])
    await state.update_data(client_id=client_id)
    
    await callback.message.edit_text(
        t("select_call_date", lang),
        reply_markup=get_days_kb(lang)
    )
    await callback.answer()

# ==========================================
# 2. ВЫБОР ЧАСА
# ==========================================
@calls_router.callback_query(F.data.startswith("date_"))
async def pick_hour(callback: CallbackQuery):
    lang, _ = await get_user_settings(callback.from_user.id)
    date_str = callback.data.split("_")[1]
    
    await callback.message.edit_text(
        t("select_call_hour", lang, date=date_str),
        reply_markup=get_hours_kb(date_str, lang)
    )
    await callback.answer()

# ==========================================
# 3. ВЫБОР МИНУТ
# ==========================================
@calls_router.callback_query(F.data.startswith("time_"))
async def pick_minutes(callback: CallbackQuery):
    lang, _ = await get_user_settings(callback.from_user.id)
    parts = callback.data.split("_")
    date_str = parts[1]
    time_str = parts[2]
    
    await callback.message.edit_text(
        t("select_call_minute", lang, date=date_str, time=time_str),
        reply_markup=get_minutes_kb(date_str, time_str, lang)
    )
    await callback.answer()

# ==========================================
# 4. ФИНАЛИЗАЦИЯ ВРЕМЕНИ -> ЗАПРОС ТЕМЫ
# ==========================================
@calls_router.callback_query(F.data.startswith("conf_time_"))
async def ask_topic(callback: CallbackQuery, state: FSMContext):
    lang, _ = await get_user_settings(callback.from_user.id)
    parts = callback.data.split("_")
    date_str = parts[2]
    time_str = parts[3]
    
    full_dt = f"{date_str} {time_str}"
    await state.update_data(full_dt=full_dt)
    
    await callback.message.edit_text(t("ask_call_topic", lang, dt=full_dt))
    await state.set_state(AddCallState.waiting_for_topic)
    await callback.answer()

# ==========================================
# 5. СОХРАНЕНИЕ (ФИНАЛ)
# ==========================================
@calls_router.message(AddCallState.waiting_for_topic)
async def finish_call_creation(message: Message, state: FSMContext):
    data = await state.get_data()
    lang, tz = await get_user_settings(message.from_user.id)
    
    topic = message.text
    if not topic:
        topic = t("call_no_topic", lang)

    # Сохраняем в БД
    await create_call(
        client_id=data['client_id'],
        date_str=data['full_dt'],
        topic=topic,
        user_timezone=tz 
    )
    
    client = await get_client(data['client_id'])
    
    # Генерируем ICS файл
    dt_obj = datetime.strptime(data['full_dt'], "%d.%m.%Y %H:%M")
    ics_path = create_ics_file(
        title=f"📞 {client.name}",
        description=f"Тема: {topic}\nТелефон: {client.phone or '---'}",
        start_time=dt_obj
    )
    
    # Отправляем ответ
    await message.answer(
        t("call_created", lang, date=data['full_dt'], tz=tz) + f"\n📌 {topic}",
        reply_markup=get_client_card_kb(client.id, lang)
    )
    
    ics_file = FSInputFile(ics_path, filename="meeting.ics")
    await message.answer_document(
        ics_file, 
        caption=t("ics_caption", lang)
    )
    
    # Уборка
    if os.path.exists(ics_path):
        os.remove(ics_path)
    
    await state.clear()