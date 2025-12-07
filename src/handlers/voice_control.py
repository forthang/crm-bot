import os
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# Import AI service
from src.services.ai_service import speech_to_text
from src.database.requests import get_user_settings, get_all_clients
# Import functions to be called
from src.handlers.clients import show_clients_list, start_add_client, select_client_to_create_call
from src.handlers.schedule import show_schedule
from src.keyboards.clients_kb import get_clients_list_kb
from src.keyboards.main_kb import get_main_keyboard
# Import locales
from src.locales import t

voice_router = Router()

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
    # If we are already in a dialog, ignore global voice commands
    current_state = await state.get_state()
    if current_state is not None:
        return

    # 1. Get user settings
    lang, _, _ = await get_user_settings(message.from_user.id)
    
    status = await message.answer(t("voice_listen", lang))
    
    # 2. Download and recognize the file
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    
    os.makedirs("media", exist_ok=True)
    file_path = f"media/{file_id}.ogg"
    await bot.download_file(file.file_path, file_path)
    
    openai_langs = {"en": "en", "fr": "fr"}
    lang_code = openai_langs.get(lang, "en")
    
    text = await speech_to_text(file_path, language=lang_code)
    text = text.lower()
    
    # The audio file is removed inside speech_to_text, so no need to remove it here.
    
    await status.edit_text(t("voice_recognized", lang, text=text))
    

    # 3. Keywords for different languages
    keywords = {
        "en": {
            "clients": ["clients", "list", "database"],
            "add": ["add", "create", "new"],
            "schedule": ["schedule", "plan", "calendar"],
            "update": ["update", "change", "edit"],
            "call": ["call", "meeting"]
        },
        "fr": {
            "clients": ["clients", "liste", "base"],
            "add": ["ajouter", "créer", "nouveau"],
            "schedule": ["calendrier", "planning", "horaire"],
            "update": ["modifier", "changer", "éditer"],
            "call": ["appel", "réunion"]
        }
    }
    
    words = keywords.get(lang, keywords["en"])

    # 4. SCENARIOS
    if any(w in text for w in words["clients"]):
        await show_clients_list(message)
    
    elif any(w in text for w in words["add"]):
        await start_add_client(message, state)
        
    elif any(w in text for w in words["schedule"]):
        await show_schedule(message)

    elif any(w in text for w in words["update"]):
        await select_client_to_update(message)

    elif any(w in text for w in words["call"]):
        await select_client_to_create_call(message)
        
    else:
        await message.answer(t("command_not_recognized", lang))