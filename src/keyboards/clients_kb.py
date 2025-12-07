from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.locales import t

def get_clients_list_kb(clients: list, lang: str = "ru"):
    builder = InlineKeyboardBuilder()
    
    # Список клиентов
    for client_row in clients:
        builder.button(text=client_row[1], callback_data=f"client_{client_row[0]}")
    
    builder.adjust(1)
    
    # Кнопка экспорта
    builder.row(InlineKeyboardButton(text=t("btn_export_excel", lang), callback_data="export_all_excel"))
    
    return builder.as_markup()

def get_client_card_kb(client_id: int, lang: str = "ru"):
    builder = InlineKeyboardBuilder()
    
    builder.button(text=t("btn_create_call", lang), callback_data=f"add_call_{client_id}")
    builder.button(text=t("btn_export_pdf", lang), callback_data=f"export_pdf_{client_id}")
    builder.button(text=t("btn_delete", lang), callback_data=f"delete_client_{client_id}")
    builder.button(text=t("btn_back_to_list", lang), callback_data="back_to_list")
    
    builder.adjust(1)
    return builder.as_markup()