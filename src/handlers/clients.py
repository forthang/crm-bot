import os
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Import keyboards and locales
from src.locales import t, all_t
from src.keyboards.main_kb import get_main_keyboard, get_cancel_keyboard
from src.keyboards.clients_kb import get_clients_list_kb, get_client_card_kb, get_status_keyboard, get_clients_list_for_call_kb
from src.services.exporter import export_clients_to_excel, export_client_to_pdf
# Import database functions
from src.database.requests import (
    create_client, 
    get_all_clients, 
    get_client, 
    delete_client,
    get_user_settings,
    update_client_status
)

# Import AI service
from src.services.ai_service import speech_to_text

client_router = Router()

# --- Define FSM states for the client form ---
class AddClientParams(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_notes = State()

# ==========================================
# ➕ ADD CLIENT LOGIC
# ==========================================

@client_router.message(F.text.in_(all_t("btn_add")))
async def start_add_client(message: Message, state: FSMContext):
    lang, _, _ = await get_user_settings(message.from_user.id)
    await message.answer(
        t("add_client_name", lang), 
        reply_markup=get_cancel_keyboard(lang)
    )
    await state.set_state(AddClientParams.waiting_for_name)

# --- Cancel button ---
@client_router.message(F.text.in_(all_t("btn_cancel")))
async def cancel_action(message: Message, state: FSMContext):
    lang, _, _ = await get_user_settings(message.from_user.id)
    await state.clear()
    await message.answer(t("action_cancelled", lang), reply_markup=get_main_keyboard(lang))

# --- Step 1: Name ---
@client_router.message(AddClientParams.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    lang, _, _ = await get_user_settings(message.from_user.id)
    if not message.text:
        await message.answer(t("enter_name_text", lang))
        return
        
    await state.update_data(name=message.text)
    
    await message.answer(t("add_client_phone", lang))
    await state.set_state(AddClientParams.waiting_for_phone)

# --- Step 2: Phone ---
@client_router.message(AddClientParams.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    lang, _, _ = await get_user_settings(message.from_user.id)
    phone = message.text
    if phone == ".": 
        phone = None
    
    await state.update_data(phone=phone)
    
    await message.answer(t("add_client_notes", lang))
    await state.set_state(AddClientParams.waiting_for_notes)

# --- Step 3: Note (Text or Voice) ---
@client_router.message(AddClientParams.waiting_for_notes)
async def process_notes(message: Message, state: FSMContext, bot: Bot):
    lang, _, _ = await get_user_settings(message.from_user.id)
    data = await state.get_data()
    note_text = ""

    # OPTION A: User sent a VOICE message
    if message.voice:
        status_msg = await message.answer(t("voice_processing", lang))
        
        try:
            file_id = message.voice.file_id
            file = await bot.get_file(file_id)
            
            os.makedirs("media", exist_ok=True)
            save_path = f"media/{file_id}.ogg"
            
            await bot.download_file(file.file_path, save_path)
            
            transcribed_text = await speech_to_text(save_path)
            note_text = transcribed_text
            
            if os.path.exists(save_path):
                os.remove(save_path)
                
            await status_msg.delete()

        except Exception as e:
            await status_msg.edit_text(t("voice_error", lang, error=e))
            note_text = t("audio_error_placeholder", lang)

    # OPTION B: User sent TEXT
    elif message.text:
        note_text = message.text
    
    else:
        await message.answer(t("send_text_or_voice", lang))
        return

    # --- Final: Save to DB ---
    try:
        await create_client(
            name=data['name'],
            phone=data['phone'],
            notes=note_text
        )
        
        await message.answer(
            t("client_created_success", lang, name=data['name'], notes=note_text),
            reply_markup=get_main_keyboard(lang)
        )
    except Exception as e:
        await message.answer(t("db_save_error", lang, error=e), reply_markup=get_main_keyboard(lang))
    
    await state.clear()


# ==========================================
# 👥 CLIENT LIST
# ==========================================

@client_router.message(F.text.in_(all_t("btn_clients")))
async def show_clients_list(message: Message):
    lang, _, _ = await get_user_settings(message.from_user.id)
    clients = await get_all_clients()
    
    if not clients:
        await message.answer(t("client_list_empty", lang), reply_markup=get_main_keyboard(lang))
        return

    kb = get_clients_list_kb(clients, lang)
    await message.answer(t("client_list_select", lang), reply_markup=kb)

async def select_client_to_create_call(message: Message):
    lang, _, _ = await get_user_settings(message.from_user.id)
    clients = await get_all_clients()
    
    if not clients:
        await message.answer(t("client_list_empty", lang), reply_markup=get_main_keyboard(lang))
        return

    kb = get_clients_list_for_call_kb(clients, lang)
    await message.answer(t("client_list_select_call", lang), reply_markup=kb)


# ==========================================
# 🖱 CALLBACK HANDLING
# ==========================================

# 1. Open client card (clicked on name)
@client_router.callback_query(F.data.startswith("client_"))
async def open_client_card(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    try:
        client_id = int(callback.data.split("_")[1])
    except:
        await callback.answer(t("id_error", lang))
        return
    
    client = await get_client(client_id)
    
    if not client:
        await callback.message.edit_text(t("client_not_found", lang))
        await callback.answer()
        return

    # Format the card text
    info = t("client_card_template", lang,
             name=client.name,
             phone=client.phone or '---',
             status=client.status or '---',
             notes=client.notes or '---'
    )

    await callback.message.edit_text(
        text=info,
        reply_markup=get_client_card_kb(client.id, lang)
    )
    await callback.answer()

# 2. "Back to list" button
@client_router.callback_query(F.data == "back_to_list")
async def back_to_list(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    clients = await get_all_clients()
    
    if not clients:
        await callback.message.edit_text(t("list_empty", lang))
    else:
        await callback.message.edit_text(
            t("select_client", lang),
            reply_markup=get_clients_list_kb(clients, lang)
        )
    await callback.answer()

# 3. "Delete" button
@client_router.callback_query(F.data.startswith("delete_client_"))
async def process_delete_client(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    client_id = int(callback.data.split("_")[2]) # delete_client_123
    
    await delete_client(client_id)
    
    await callback.answer(t("client_deleted", lang))
    # Return to the list
    await back_to_list(callback)

@client_router.callback_query(F.data == "export_all_excel")
async def process_export_excel(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    await callback.message.answer(t("generating_excel", lang))
    
    path = await export_clients_to_excel()
    
    if not path:
        await callback.message.answer(t("db_empty", lang))
        await callback.answer()
        return

    file = FSInputFile(path, filename="clients_base.xlsx")
    await callback.message.answer_document(file, caption=t("excel_caption", lang))
    await callback.answer()
    
    os.remove(path)

# 5. Export PDF (One client)
@client_router.callback_query(F.data.startswith("export_pdf_"))
async def process_export_pdf(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    client_id = int(callback.data.split("_")[2])
    
    await callback.answer(t("generating_pdf", lang))
    
    path = await export_client_to_pdf(client_id)
    
    if not path:
        await callback.message.answer(t("generation_error", lang))
        return

    file = FSInputFile(path, filename=f"client_{client_id}.pdf")
    await callback.message.answer_document(file, caption=t("pdf_caption", lang))
    
    os.remove(path)

# 6. Change status
@client_router.callback_query(F.data.startswith("change_status_"))
async def change_status(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    client_id = int(callback.data.split("_")[1])
    
    await callback.message.edit_text(
        t("select_status", lang),
        reply_markup=get_status_keyboard(client_id, lang)
    )
    await callback.answer()

# 7. Set status
@client_router.callback_query(F.data.startswith("set_status_"))
async def set_status(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    client_id = int(callback.data.split("_")[2])
    status = callback.data.split("_")[3]
    
    await update_client_status(client_id, status)
    
    client = await get_client(client_id)
    
    await callback.answer(t("status_changed", lang, name=client.name, status=status))
    
    await open_client_card(callback)