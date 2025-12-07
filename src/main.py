import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

# 1. Settings and Database
from src.config import config
from src.database.core import create_tables

# 2. Background tasks (Scheduler)
from src.services.scheduler import start_scheduler

# 3. Routers (Message Handlers)
from src.handlers.start import start_router          # Entry, authorization
from src.handlers.settings import settings_router    # Settings (Language, Timezone)
from src.handlers.clients import client_router       # Clients (CRUD, List)
from src.handlers.calls import calls_router          # Calls (Calendar, ICS)
from src.handlers.schedule import schedule_router    # Schedule (Weeks)
from src.handlers.stats import stats_router          # Statistics
from src.handlers.voice_control import voice_router  # Global voice control

async def main():
    # --- INITIALIZATION ---
    
    # 1. Create tables in the DB (if they don't exist)
    await create_tables()
    print("✅ Database connected. Tables synchronized.")

    # 2. Create the bot
    bot = Bot(
        token=config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    # --- ROUTER REGISTRATION ---
    # ⚠️ The order of connection is critical!
    # Aiogram checks handlers from top to bottom.
    
    dp.include_router(start_router)     # /start and password check
    dp.include_router(settings_router)  # Settings menu (language, timezone)
    dp.include_router(client_router)    # Main client functionality
    dp.include_router(calls_router)     # Call creation
    dp.include_router(schedule_router)  # Schedule view
    dp.include_router(stats_router)     # Statistics view
    
    # Global voice handler is last.
    # It catches voice messages if no FSM (form) is active.
    dp.include_router(voice_router)     

    # --- START BACKGROUND PROCESSES ---
    
    # Start the scheduler (call reminders)
    start_scheduler(bot)
    print("⏰ Task Scheduler started.")

    # --- START THE BOT ---
    
    # Delete old updates (so the bot doesn't respond to messages sent while it was offline)
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("🚀 CRM Bot successfully launched! Awaiting commands...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot stopped by administrator.")