from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.locales import t

def get_days_kb(client_id: int, lang: str = "en"):
    """Day selection: Today, Tomorrow, Day after tomorrow + Days of the week"""
    builder = InlineKeyboardBuilder()
    now = datetime.now()
    
    # Quick buttons
    builder.button(text=t("btn_today", lang), callback_data=f"date_{now.strftime('%d.%m.%Y')}_{client_id}")
    tomorrow = now + timedelta(days=1)
    builder.button(text=t("btn_tomorrow", lang), callback_data=f"date_{tomorrow.strftime('%d.%m.%Y')}_{client_id}")
    
    # Next 5 days
    for i in range(2, 7):
        day = now + timedelta(days=i)
        date_str = day.strftime("%d.%m.%Y")
        btn_text = day.strftime("%a, %d.%m") # Mon, 25.10
        builder.button(text=btn_text, callback_data=f"date_{date_str}_{client_id}")

    builder.adjust(2) # 2 buttons per row
    return builder.as_markup()

def get_hours_kb(date_str: str, client_id: int, lang: str = "en"):
    """Hour selection (09:00 - 20:00)"""
    builder = InlineKeyboardBuilder()
    
    # Working hours
    for hour in range(9, 21):
        # Pass the date along so it's not lost
        builder.button(text=f"{hour}:00", callback_data=f"time_{date_str}_{hour}:00_{client_id}")
        
    builder.adjust(4) # 4 per row
    builder.button(text=t("btn_back", lang), callback_data=f"client_{client_id}")
    return builder.as_markup()

def get_minutes_kb(date_str: str, hour_str: str, client_id: int, lang: str = "en"):
    """Minute selection (00, 15, 30, 45) for a specific hour"""
    builder = InlineKeyboardBuilder()
    hour = hour_str.split(":")[0] # "14:00" -> "14"
    
    for minute in ["00", "15", "30", "45"]:
        full_time = f"{hour}:{minute}"
        # Final callback: save_call_DATE_TIME
        builder.button(
            text=full_time, 
            callback_data=f"conf_time_{date_str}_{full_time}_{client_id}"
        )
        
    builder.adjust(4)
    builder.button(text=t("btn_back", lang), callback_data=f"time_{date_str}_{hour_str}_{client_id}")
    return builder.as_markup()