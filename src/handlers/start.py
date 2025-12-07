from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Import settings for password checking
from src.config import config
# Import database functions
from src.database.requests import get_user, add_user, get_user_settings
# Import keyboards and locales
from src.keyboards.main_kb import get_main_keyboard
from src.locales import t

# Create a router
start_router = Router()

# States for authorization
class AuthState(StatesGroup):
    waiting_for_password = State()

# --- Handler for the /start command ---
@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    # 1. First, check if the user is in the database
    user = await get_user(message.from_user.id)
    
    if user:
        # If the user exists, get their language and show the menu
        lang, _ = await get_user_settings(user.telegram_id)
        await message.answer(
            t("welcome_back", lang, name=user.full_name),
            reply_markup=get_main_keyboard(lang)
        )
        return

    # 2. If the user is not found, enable protection (default language "en")
    await message.answer(t("auth_required", "en"))
    
    # Set the state to wait for the password
    await state.set_state(AuthState.waiting_for_password)

# --- Handler for password processing ---
@start_router.message(AuthState.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    input_password = message.text.strip()
    
    # Compare the input text with the password from .env
    if input_password == config.BOT_PASSWORD.get_secret_value():
        
        # Correct password -> save the user to the DB
        await add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )
        
        # Greet in the default language ("en")
        await message.answer(
            t("auth_success", "en"),
            reply_markup=get_main_keyboard("en")
        )
        
        # Clear the state (no longer waiting for a password)
        await state.clear()
        
    else:
        # Incorrect password (default language "en")
        await message.answer(t("auth_failed", "en"))