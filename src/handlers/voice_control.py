import os
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# Импортируем сервис ИИ
from src.services.ai_service import speech_to_text
# Импортируем работу с настройками
from src.database.requests import get_user_settings
# Импортируем функции, которые будем вызывать
from src.handlers.clients import show_clients_list, start_add_client
from src.handlers.schedule import show_schedule
# Импортируем локали
from src.locales import t

voice_router = Router()

@voice_router.message(F.voice)
async def global_voice_handler(message: Message, state: FSMContext, bot: Bot):
    # Если мы уже внутри какого-то диалога, игнорируем глобальный голос
    current_state = await state.get_state()
    if current_state is not None:
        return

    # 1. Получаем настройки пользователя
    lang, _ = await get_user_settings(message.from_user.id)
    
    status = await message.answer(t("voice_listen", lang))
    
    # 2. Скачиваем и распознаем файл
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    
    os.makedirs("media", exist_ok=True)
    file_path = f"media/{file_id}.ogg"
    await bot.download_file(file.file_path, file_path)
    
    google_langs = {"ru": "ru-RU", "en": "en-US", "fr": "fr-FR"}
    lang_code = google_langs.get(lang, "ru-RU")
    
    text = await speech_to_text(file_path, language=lang_code)
    text = text.lower()
    
    await status.edit_text(t("voice_recognized", lang, text=text))
    
    if os.path.exists(file_path):
        os.remove(file_path)

    # 3. Ключевые слова для разных языков
    keywords = {
        "ru": {
            "clients": ["клиенты", "список", "база"],
            "add": ["добавь", "создай", "новый"],
            "schedule": ["расписание", "план", "календарь"]
        },
        "en": {
            "clients": ["clients", "list", "database"],
            "add": ["add", "create", "new"],
            "schedule": ["schedule", "plan", "calendar"]
        },
        "fr": {
            "clients": ["clients", "liste", "base"],
            "add": ["ajouter", "créer", "nouveau"],
            "schedule": ["calendrier", "planning", "horaire"]
        }
    }
    
    words = keywords.get(lang, keywords["ru"])

    # 4. СЦЕНАРИИ
    if any(w in text for w in words["clients"]):
        await show_clients_list(message)
    
    elif any(w in text for w in words["add"]):
        await start_add_client(message, state)
        
    elif any(w in text for w in words["schedule"]):
        await show_schedule(message)
        
    else:
        await message.answer(t("command_not_recognized", lang))