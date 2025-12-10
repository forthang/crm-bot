import os
import pytz
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

# Import AI service
from src.services.ai_service import speech_to_text, get_intent_and_entities
from src.database.requests import get_user_settings, get_all_clients, create_client, create_call, find_client_by_exact_name
# Import functions to be called
from src.handlers.clients import show_clients_menu, start_add_client, select_client_to_create_call
from src.handlers.schedule import show_schedule
from src.keyboards.clients_kb import get_clients_list_kb
from src.keyboards.main_kb import get_main_keyboard
# Import locales
from src.locales import t

voice_router = Router()

# FSM for voice command confirmation
class VoiceConfirmation(StatesGroup):
    waiting_for_confirmation = State()

def get_voice_confirmation_kb(lang: str):
    """Returns 'Confirm' and 'Cancel' buttons."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_confirm", lang), callback_data="voice_confirm"),
            InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="voice_cancel")
        ]
    ])

async def select_client_to_update(message: Message):
    lang, _, _ = await get_user_settings(message.from_user.id)
    clients = await get_all_clients()
    
    if not clients:
        await message.answer(t("client_list_empty", lang), reply_markup=get_main_keyboard(lang))
        return

    kb = get_clients_list_kb(clients, lang)
    await message.answer(t("client_list_select_update", lang), reply_markup=kb)

@voice_router.message(F.voice)
async def global_voice_handler(message: Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state is not None:
        return

    lang, tz, _ = await get_user_settings(message.from_user.id)
    status_msg = await message.answer(t("voice_listen", lang))
    
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    
    os.makedirs("media", exist_ok=True)
    file_path = f"media/{file_id}.ogg"
    await bot.download_file(file.file_path, file_path)
    
    # More flexible language detection for STT
    if lang.startswith("fr"):
        lang_code = "fr"
    else:
        lang_code = "en"
    
    text = await speech_to_text(file_path, language=lang_code)
    
    await status_msg.edit_text(t("ai_thinking", lang, text=text))
    
    ai_response = await get_intent_and_entities(text, user_timezone=tz)
    intent = ai_response.get("intent")
    entities = ai_response.get("entities", {})

    if intent == "create_client_and_schedule_call":
        client_name = entities.get("client_name")
        call_datetime_str = entities.get("call_datetime") # Format: YYYY-MM-DD HH:MM
        call_topic = entities.get("call_topic") or t("call_no_topic", lang)

        if not client_name or not call_datetime_str:
            await message.answer(t("ai_missing_data", lang))
            return
        
        # Check if client already exists
        existing_client = await find_client_by_exact_name(client_name)
        
        fsm_data = {
            "client_name": client_name,
            "call_datetime_str": call_datetime_str,
            "call_topic": call_topic,
            "user_timezone": tz,
            "original_text": text,
            "is_new_client": existing_client is None,
            "client_id": existing_client.id if existing_client else None
        }
        
        await state.update_data(**fsm_data)
        await state.set_state(VoiceConfirmation.waiting_for_confirmation)
        
        # Format datetime for confirmation message
        dt_obj = datetime.strptime(call_datetime_str, "%Y-%m-%d %H:%M")
        confirmation_date = dt_obj.strftime("%d.%m.%Y %H:%M")
        
        if existing_client:
            prompt_key = "ai_confirmation_prompt_existing_client"
        else:
            prompt_key = "ai_confirmation_prompt_new_client"
            
        await message.answer(
            t(prompt_key, lang, client_name=client_name, date=confirmation_date, topic=call_topic),
            reply_markup=get_voice_confirmation_kb(lang)
        )

    elif intent == "simple_command":
        command = entities.get("command", "").lower()
        if command in ["clients", "list", "database"]:
            await show_clients_menu(message)
        elif command in ["add", "create", "new"]:
            await start_add_client(message, state)
        elif command in ["schedule", "plan", "calendar"]:
            await show_schedule(message)
        elif command in ["call", "meeting"]:
            await select_client_to_create_call(message)
        elif command in ["update", "change", "edit"]:
            await select_client_to_update(message)
        else:
            await message.answer(t("command_not_recognized", lang))
            
    else:
        await message.answer(t("command_not_recognized", lang))

@voice_router.callback_query(F.data == "voice_confirm", VoiceConfirmation.waiting_for_confirmation)
async def confirm_voice_action(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang, _, _ = await get_user_settings(callback.from_user.id)
    
    await callback.message.edit_text(t("processing_request", lang))

    try:
        client_id = data.get("client_id")
        
        if data.get("is_new_client"):
            client_id = await create_client(
                name=data['client_name'], 
                phone=None, 
                notes=f"Created from voice command: '{data['original_text']}'"
            )
        
        dt_obj = datetime.strptime(data['call_datetime_str'], "%Y-%m-%d %H:%M")
        date_for_db = dt_obj.strftime("%d.%m.%Y %H:%M")

        await create_call(
            client_id=client_id,
            date_str=date_for_db,
            topic=data['call_topic'],
            user_timezone=data['user_timezone']
        )
        
        # Timezone display logic
        user_tz = pytz.timezone(data['user_timezone'])
        aware_dt = user_tz.localize(dt_obj)
        msk_tz = pytz.timezone('Europe/Moscow')
        paris_tz = pytz.timezone('Europe/Paris')
        msk_time_str = aware_dt.astimezone(msk_tz).strftime("%d.%m.%Y %H:%M")
        paris_time_str = aware_dt.astimezone(paris_tz).strftime("%H:%M")

        if data.get("is_new_client"):
            success_key = "ai_client_and_call_created"
        else:
            success_key = "ai_call_created_for_existing_client"

        await callback.message.answer(
            t(success_key, lang, 
              client_name=data['client_name'], 
              msk_time=msk_time_str, 
              paris_time=paris_time_str,
              topic=data['call_topic'])
        )
        
    except Exception as e:
        await callback.message.answer(t("ai_execution_error", lang, error=str(e)))
        print(f"❌ Error executing confirmed AI command: {e}")
    finally:
        await state.clear()
        await callback.answer()

@voice_router.callback_query(F.data == "voice_cancel", VoiceConfirmation.waiting_for_confirmation)
async def cancel_voice_action(callback: CallbackQuery, state: FSMContext):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    await state.clear()
    await callback.message.edit_text(t("action_cancelled", lang))
    await callback.answer()