from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.locales import t

def get_days_kb(lang: str = "ru"):
    """Выбор дня: Сегодня, Завтра, Послезавтра + Дни недели"""
    builder = InlineKeyboardBuilder()
    now = datetime.now()
    
    # Быстрые кнопки
    builder.button(text=t("btn_today", lang), callback_data=f"date_{now.strftime('%d.%m.%Y')}")
    tomorrow = now + timedelta(days=1)
    builder.button(text=t("btn_tomorrow", lang), callback_data=f"date_{tomorrow.strftime('%d.%m.%Y')}")
    
    # Следующие 5 дней
    for i in range(2, 7):
        day = now + timedelta(days=i)
        date_str = day.strftime("%d.%m.%Y")
        btn_text = day.strftime("%a, %d.%m") # Пн, 25.10
        builder.button(text=btn_text, callback_data=f"date_{date_str}")

    builder.adjust(2) # По 2 кнопки в ряд
    return builder.as_markup()

def get_hours_kb(date_str: str, lang: str = "ru"):
    """Выбор часа (09:00 - 20:00)"""
    builder = InlineKeyboardBuilder()
    
    # Рабочие часы
    for hour in range(9, 21):
        # Передаем дату дальше, чтобы не потерять
        builder.button(text=f"{hour}:00", callback_data=f"time_{date_str}_{hour}:00")
        
    builder.adjust(4) # По 4 в ряд
    builder.button(text=t("btn_back", lang), callback_data="add_call_back")
    return builder.as_markup()

def get_minutes_kb(date_str: str, hour_str: str, lang: str = "ru"):
    """Выбор минут (00, 15, 30, 45) для конкретного часа"""
    builder = InlineKeyboardBuilder()
    hour = hour_str.split(":")[0] # "14:00" -> "14"
    
    for minute in ["00", "15", "30", "45"]:
        full_time = f"{hour}:{minute}"
        # Финальный колбэк: save_call_ДАТА_ВРЕМЯ
        builder.button(
            text=full_time, 
            callback_data=f"conf_time_{date_str}_{full_time}"
        )
        
    builder.adjust(4)
    builder.button(text=t("btn_back", lang), callback_data=f"back_to_hours_{date_str}")
    return builder.as_markup()