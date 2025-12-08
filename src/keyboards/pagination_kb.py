from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.locales import t

def get_pagination_kb(
    current_page: int, 
    total_pages: int, 
    callback_prefix: str,
    lang: str = "en"
) -> InlineKeyboardBuilder:
    """
    Creates a pagination keyboard.
    
    :param current_page: The current page number (0-indexed).
    :param total_pages: The total number of pages.
    :param callback_prefix: The prefix for the callback data (e.g., "clients_page").
    :param lang: The language for the button text.
    :return: An InlineKeyboardBuilder object with pagination buttons.
    """
    builder = InlineKeyboardBuilder()
    
    if total_pages <= 1:
        return builder # No pagination needed

    # Previous button
    if current_page > 0:
        builder.button(
            text=t("btn_prev", lang), 
            callback_data=f"{callback_prefix}_{current_page - 1}"
        )
    
    # Page indicator
    builder.button(
        text=f"{current_page + 1} / {total_pages}", 
        callback_data="no_action" # A dummy callback
    )

    # Next button
    if current_page < total_pages - 1:
        builder.button(
            text=t("btn_next", lang), 
            callback_data=f"{callback_prefix}_{current_page + 1}"
        )
        
    return builder
