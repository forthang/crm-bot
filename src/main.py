import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

# 1. Настройки и База данных
from src.config import config
from src.database.core import create_tables

# 2. Фоновые задачи (Планировщик)
from src.services.scheduler import start_scheduler

# 3. Роутеры (Обработчики сообщений)
from src.handlers.start import start_router          # Вход, авторизация
from src.handlers.settings import settings_router    # Настройки (Язык, Часовой пояс)
from src.handlers.clients import client_router       # Клиенты (CRUD, Список)
from src.handlers.calls import calls_router          # Созвоны (Календарь, ICS)
from src.handlers.schedule import schedule_router    # Расписание (Недели)
from src.handlers.voice_control import voice_router  # Глобальное голосовое управление

async def main():
    # --- ИНИЦИАЛИЗАЦИЯ ---
    
    # 1. Создаем таблицы в БД (если их нет)
    await create_tables()
    print("✅ База данных подключена. Таблицы синхронизированы.")

    # 2. Создаем бота
    bot = Bot(
        token=config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    # --- РЕГИСТРАЦИЯ РОУТЕРОВ ---
    # ⚠️ Порядок подключения критически важен!
    # Aiogram проверяет хендлеры сверху вниз.
    
    dp.include_router(start_router)     # /start и проверка пароля
    dp.include_router(settings_router)  # Меню настроек (язык, пояс)
    dp.include_router(client_router)    # Основной функционал клиентов
    dp.include_router(calls_router)     # Создание созвонов
    dp.include_router(schedule_router)  # Просмотр расписания
    
    # Глобальный голос ставим В КОНЦЕ.
    # Он ловит голосовые, если ни один FSM (анкета) не активен.
    dp.include_router(voice_router)     

    # --- ЗАПУСК ФОНОВЫХ ПРОЦЕССОВ ---
    
    # Запускаем планировщик (напоминания о звонках)
    start_scheduler(bot)
    print("⏰ Планировщик задач (Scheduler) запущен.")

    # --- СТАРТ БОТА ---
    
    # Удаляем старые апдейты (чтобы бот не отвечал на сообщения, присланные, пока он спал)
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("🚀 CRM Бот успешно запущен! Ожидаю команды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Настройка логов
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен администратором.")