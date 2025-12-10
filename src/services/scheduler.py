from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from src.database.requests import get_calls_to_remind, mark_call_as_reminded, get_client, get_all_users
from src.locales import t
from src.keyboards.calls_kb import get_reminder_kb

# Create a scheduler object
scheduler = AsyncIOScheduler()

async def check_reminders(bot: Bot):
    """This function is run every minute to check for and send call reminders to all authenticated users."""
    
    # Get all users who have successfully authenticated
    all_users = await get_all_users()

    if not all_users:
        print("ℹ️ No authenticated users found to send reminders.")
        return

    # We need to check all calls that are due soon, but we should only do it once.
    # Let's find the maximum possible reminder delay to query all relevant calls at once.
    # This is not perfectly efficient if delays are very different, but it's better than querying in a loop.
    # A better approach would be to group users by delay time. For now, we'll keep it simple.
    
    # Let's find all calls that need a reminder within a broad window (e.g., 60 minutes)
    # We will filter them for each user inside the loop.
    calls_to_remind_globally = await get_calls_to_remind(minutes=120) # Using a larger window
    
    if not calls_to_remind_globally:
        return

    # Process reminders for each user individually
    for user in all_users:
        try:
            # Get each user's personal settings
            lang, _, delay = user.language, user.timezone, user.reminder_delay

            for call in calls_to_remind_globally:
                # Check if this specific call is within this specific user's reminder window
                now = datetime.now(call.datetime.tzinfo)
                if not (now < call.datetime <= now + timedelta(minutes=delay)):
                    continue

                client = await get_client(call.client_id)
                
                # Format the reminder text in the user's language
                text = t(
                    "call_reminder", lang, 
                    client_name=client.name, 
                    client_phone=client.phone or '---', 
                    topic=call.title, 
                    minutes=delay
                )
                
                try:
                    # Send the reminder and mark it as sent to avoid duplicates
                    await bot.send_message(
                        chat_id=user.telegram_id, 
                        text=text, 
                        reply_markup=get_reminder_kb(call.id, lang)
                    )
                    # This call has been processed for this user, but we mark it globally.
                    # This means only the first user whose window matches will trigger the reminder.
                    # To fix this, reminder_sent should be a many-to-many relationship between users and calls.
                    # For now, we accept this limitation: a reminder is sent once.
                    if not call.reminder_sent:
                        await mark_call_as_reminded(call.id)
                    
                    print(f"✅ Reminder sent to user {user.telegram_id} for call {call.id} (Language: {lang})")

                except Exception as e:
                    # This might happen if the user blocked the bot
                    print(f"❌ Failed to send reminder for call {call.id} to user {user.telegram_id}: {e}")

        except Exception as e:
            print(f"❌ Error processing reminders for user {user.telegram_id}: {e}")

def start_scheduler(bot: Bot):
    scheduler.add_job(check_reminders, 'interval', minutes=1, kwargs={"bot": bot})
    scheduler.start()