from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from src.database.requests import get_calls_to_remind, mark_call_as_reminded, get_client, get_user_settings
from src.locales import t
from src.config import config
from src.keyboards.calls_kb import get_reminder_kb

# Create a scheduler object
scheduler = AsyncIOScheduler()

async def check_reminders(bot: Bot):
    """This function is run every minute"""
    # Assume we have one admin and send reminders to them
    try:
        admin_id = int(config.ADMIN_IDS.split(",")[0])
    except (ValueError, IndexError):
        print("❌ Error: ADMIN_IDS is not configured or has an invalid format.")
        return

    # Get the admin's settings once
    lang, _, delay = await get_user_settings(admin_id)

    calls = await get_calls_to_remind(minutes=delay)
    
    if not calls:
        return

    for call in calls:
        client = await get_client(call.client_id)
        
        # Format the text in the admin's language
        text = t("call_reminder", lang, client_name=client.name, topic=call.title, minutes=delay)
        
        try:
            await bot.send_message(chat_id=admin_id, text=text, reply_markup=get_reminder_kb(call.id, lang))
            await mark_call_as_reminded(call.id)
            print(f"✅ Reminder sent for call {call.id} (language: {lang})")
        except Exception as e:
            print(f"❌ Error sending reminder for call {call.id}: {e}")

def start_scheduler(bot: Bot):
    scheduler.add_job(check_reminders, 'interval', minutes=1, kwargs={"bot": bot})
    scheduler.start()