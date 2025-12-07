from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Импортируем настройки (для проверки пароля)
from src.config import config
# Импортируем работу с БД
from src.database.requests import get_user, add_user, get_user_settings
# Импортируем клавиатуру и локали
from src.keyboards.main_kb import get_main_keyboard
from src.locales import t

# Создаем роутер
start_router = Router()

# Состояния для авторизации
class AuthState(StatesGroup):
    waiting_for_password = State()

# --- Хендлер команды /start ---
@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    # 1. Сначала проверяем, есть ли такой пользователь в Базе Данных
    user = await get_user(message.from_user.id)
    
    if user:
        # Если пользователь уже есть — получаем его язык и показываем меню
        lang, _ = await get_user_settings(user.telegram_id)
        await message.answer(
            t("welcome_back", lang, name=user.full_name),
            reply_markup=get_main_keyboard(lang)
        )
        return

    # 2. Если пользователя нет — включаем защиту (язык по умолчанию "ru")
    await message.answer(t("auth_required", "ru"))
    
    # Устанавливаем состояние ожидания пароля
    await state.set_state(AuthState.waiting_for_password)

# --- Хендлер проверки пароля ---
@start_router.message(AuthState.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    input_password = message.text.strip()
    
    # Сравниваем введенный текст с паролем из .env
    if input_password == config.BOT_PASSWORD.get_secret_value():
        
        # Пароль верный -> сохраняем пользователя в БД
        await add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )
        
        # Приветствуем на языке по умолчанию ("ru")
        await message.answer(
            t("auth_success", "ru"),
            reply_markup=get_main_keyboard("ru")
        )
        
        # Сбрасываем состояние (больше не ждем пароль)
        await state.clear()
        
    else:
        # Пароль неверный (язык по умолчанию "ru")
        await message.answer(t("auth_failed", "ru"))