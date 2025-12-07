import os
from datetime import datetime
import pytz
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# DB Imports
from src.database.requests import create_call, get_client, get_user_settings, update_call_status, get_call, update_client_notes
# Keyboard Imports
from src.keyboards.clients_kb import get_client_card_kb
from src.keyboards.calendar_kb import get_days_kb, get_hours_kb, get_minutes_kb
from src.keyboards.calls_kb import get_post_call_kb
# ICS Generator Import
from src.services.ics_generator import create_ics_file
# AI Service Import
from src.services.ai_service import speech_to_text
# Localization
from src.locales import t

calls_router = Router()

class AddCallState(StatesGroup):
    waiting_for_topic = State()

class EditNotesState(StatesGroup):
    waiting_for_notes = State()

# ==========================================
# 1. START: Select Day
# ==========================================
@calls_router.callback_query(F.data.startswith("add_call_"))
async def start_add_call(callback: CallbackQuery, state: FSMContext):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    client_id = int(callback.data.split("_")[2])
    await state.update_data(client_id=client_id)
    
    await callback.message.edit_text(
        t("select_call_date", lang),
        reply_markup=get_days_kb(lang)
    )
    await callback.answer()

# ==========================================
# 2. SELECT HOUR
# ==========================================
@calls_router.callback_query(F.data.startswith("date_"))
async def pick_hour(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    date_str = callback.data.split("_")[1]
    
    await callback.message.edit_text(
        t("select_call_hour", lang, date=date_str),
        reply_markup=get_hours_kb(date_str, lang)
    )
    await callback.answer()

# ==========================================
# 3. SELECT MINUTES
# ==========================================
@calls_router.callback_query(F.data.startswith("time_"))
async def pick_minutes(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    parts = callback.data.split("_")
    date_str = parts[1]
    time_str = parts[2]
    
    await callback.message.edit_text(
        t("select_call_minute", lang, date=date_str, time=time_str),
        reply_markup=get_minutes_kb(date_str, time_str, lang)
    )
    await callback.answer()

# ==========================================
# 4. FINALIZE TIME -> REQUEST TOPIC
# ==========================================
@calls_router.callback_query(F.data.startswith("conf_time_"))
async def ask_topic(callback: CallbackQuery, state: FSMContext):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    parts = callback.data.split("_")
    date_str = parts[2]
    time_str = parts[3]
    
    full_dt = f"{date_str} {time_str}"
    await state.update_data(full_dt=full_dt)
    
    await callback.message.edit_text(t("ask_call_topic", lang, dt=full_dt))
    await state.set_state(AddCallState.waiting_for_topic)
    await callback.answer()

# ==========================================
# 5. SAVE (FINAL)
# ==========================================
@calls_router.message(AddCallState.waiting_for_topic)
async def finish_call_creation(message: Message, state: FSMContext):
    data = await state.get_data()
    lang, tz, _ = await get_user_settings(message.from_user.id)
    
    topic = message.text
    if not topic:
        topic = t("call_no_topic", lang)

    # Save to DB
    await create_call(
        client_id=data['client_id'],
        date_str=data['full_dt'],
        topic=topic,
        user_timezone=tz 
    )
    
    client = await get_client(data['client_id'])
    
    # Generate ICS file
    dt_obj = datetime.strptime(data['full_dt'], "%d.%m.%Y %H:%M")
    
    # Convert dt_obj (which is in user's timezone) to UTC first
    user_tz = pytz.timezone(tz)
    dt_obj_aware = user_tz.localize(dt_obj)
    utc_dt = dt_obj_aware.astimezone(pytz.utc)

    # Define timezones for display
    msk_tz = pytz.timezone('Europe/Moscow')
    paris_tz = pytz.timezone('Europe/Paris')

    # Convert to respective timezones for display
    msk_time_str = utc_dt.astimezone(msk_tz).strftime("%d.%m.%Y %H:%M")
    paris_time_str = utc_dt.astimezone(paris_tz).strftime("%H:%M")

    ics_path = create_ics_file(
        title=f"📞 {client.name}",
        description=f"Topic: {topic}\nPhone: {client.phone or '---'}",
        start_time=dt_obj
    )
    
    # Send response
    await message.answer(
        t("call_created", lang, msk_time=msk_time_str, paris_time=paris_time_str) + f"\n📌 {topic}",
        reply_markup=get_client_card_kb(client.id, lang)
    )
    
    ics_file = FSInputFile(ics_path, filename="meeting.ics")
    await message.answer_document(
        ics_file, 
        caption=t("ics_caption", lang)
    )
    
    # Cleanup
    if os.path.exists(ics_path):
        os.remove(ics_path)
    
    await state.clear()

# ==========================================
# 6. POST-CALL FOLLOW-UP
# ==========================================
@calls_router.callback_query(F.data.startswith("call_done_"))
async def call_done(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    call_id = int(callback.data.split("_")[2])
    
    await update_call_status(call_id, "done")
    
    call = await get_call(call_id)
    client = await get_client(call.client_id)
    
    await callback.message.edit_text(
        t("call_follow_up", lang, client_name=client.name),
        reply_markup=get_post_call_kb(client.id, lang)
    )
    await callback.answer(t("call_marked_done", lang))

@calls_router.callback_query(F.data.startswith("call_cancel_"))
async def call_cancel(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    call_id = int(callback.data.split("_")[2])
    
    await update_call_status(call_id, "cancel")
    
    await callback.message.edit_text(t("call_cancelled", lang))
    await callback.answer()

@calls_router.callback_query(F.data == "no_changes")
async def no_changes(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

@calls_router.callback_query(F.data.startswith("edit_notes_"))
async def edit_notes(callback: CallbackQuery, state: FSMContext):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    client_id = int(callback.data.split("_")[2])
    
    await state.update_data(client_id=client_id)
    await callback.message.edit_text(t("edit_notes_prompt", lang))
    await state.set_state(EditNotesState.waiting_for_notes)
    await callback.answer()

@calls_router.message(EditNotesState.waiting_for_notes)
async def process_new_notes(message: Message, state: FSMContext, bot: Bot):
    lang, _, _ = await get_user_settings(message.from_user.id)
    data = await state.get_data()
    note_text = ""

    if message.voice:
        status_msg = await message.answer(t("voice_processing", lang))
        try:
            file_id = message.voice.file_id
            file = await bot.get_file(file_id)
            
            os.makedirs("media", exist_ok=True)
            save_path = f"media/{file_id}.ogg"
            
            await bot.download_file(file.file_path, save_path)
            
            transcribed_text = await speech_to_text(save_path)
            note_text = transcribed_text
            
            if os.path.exists(save_path):
                os.remove(save_path)
                
            await status_msg.delete()
        except Exception as e:
            await status_msg.edit_text(t("voice_error", lang, error=e))
            note_text = t("audio_error_placeholder", lang)
    elif message.text:
        note_text = message.text
    else:
        await message.answer(t("send_text_or_voice", lang))
        return

    await update_client_notes(data['client_id'], note_text)
    
    await message.answer(t("notes_updated", lang))
    await state.clear()