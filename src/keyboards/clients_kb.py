from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.locales import t
from src.database.enums import ClientStatus

def get_clients_list_kb(clients: list, lang: str = "en"):
    builder = InlineKeyboardBuilder()
    
    # List of clients
    for client_row in clients:
        builder.button(text=client_row[1], callback_data=f"client_{client_row[0]}")
    
    builder.adjust(1)
    
    # Export button
    builder.row(InlineKeyboardButton(text=t("btn_export_excel", lang), callback_data="export_all_excel"))
    
    return builder.as_markup()

def get_client_card_kb(client_id: int, lang: str = "en"):
    builder = InlineKeyboardBuilder()
    
    builder.button(text=t("btn_create_call", lang), callback_data=f"add_call_{client_id}")
    builder.button(text=t("btn_change_status", lang), callback_data=f"change_status_{client_id}")
    builder.button(text=t("btn_export_pdf", lang), callback_data=f"export_pdf_{client_id}")
    builder.button(text=t("btn_delete", lang), callback_data=f"delete_client_{client_id}")
    builder.button(text=t("btn_back_to_list", lang), callback_data="back_to_list")
    
    builder.adjust(1)
    return builder.as_markup()

def get_status_keyboard(client_id: int, lang: str = "en"):

    builder = InlineKeyboardBuilder()

    for status in ClientStatus:

        builder.button(text=status.value.title(), callback_data=f"set_status_{client_id}_{status.value}")

    builder.adjust(2)

    builder.row(InlineKeyboardButton(text=t("btn_back", lang), callback_data=f"client_{client_id}"))

    return builder.as_markup()



def get_clients_list_for_call_kb(clients: list, lang: str = "en"):

    builder = InlineKeyboardBuilder()

    

    # List of clients

    for client_row in clients:

        builder.button(text=client_row[1], callback_data=f"add_call_{client_row[0]}")

    

    builder.adjust(1)

    

    return builder.as_markup()
