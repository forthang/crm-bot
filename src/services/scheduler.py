from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from src.database.requests import get_calls_to_remind, mark_call_as_reminded, get_client, get_user_settings
from src.locales import t
from src.config import config

# Создаем объект шедулера
scheduler = AsyncIOScheduler()

async def check_reminders(bot: Bot):
    """Эта функция запускается каждую минуту"""
    calls = await get_calls_to_remind()
    
    if not calls:
        return

    # Предполагаем, что у нас один админ, и напоминания шлем ему
    try:
        admin_id = int(config.ADMIN_IDS.split(",")[0])
    except (ValueError, IndexError):
        print("❌ Ошибка: ADMIN_IDS не настроен или имеет неверный формат.")
        return

    # Получаем язык админа один раз
    lang, _ = await get_user_settings(admin_id)

    for call in calls:
        client = await get_client(call.client_id)
        
        # Формируем текст на языке админа
        text = t("call_reminder", lang, client_name=client.name, topic=call.title)
        
        try:
            await bot.send_message(chat_id=admin_id, text=text)
            await mark_call_as_reminded(call.id)
            print(f"✅ Отправлено напоминание для звонка {call.id} (язык: {lang})")
        except Exception as e:
            print(f"❌ Ошибка отправки напоминания для звонка {call.id}: {e}")

def start_scheduler(bot: Bot):
    scheduler.add_job(check_reminders, 'interval', minutes=1, kwargs={"bot": bot})
    scheduler.start()