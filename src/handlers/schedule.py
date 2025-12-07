from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from src.locales import all_t, t
from src.database.requests import get_calls_in_range, get_client, get_user_settings

schedule_router = Router()

def get_schedule_kb(offset=0, lang: str = "ru"):
    """Кнопки переключения недель. Offset = сдвиг в неделях (0 - текущая)"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_prev", lang), callback_data=f"sched_{offset-1}"),
            InlineKeyboardButton(text=t("btn_next", lang), callback_data=f"sched_{offset+1}")
        ]
    ])

async def generate_schedule_text(offset: int, lang: str = "ru"):
    # 1. Считаем даты
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=offset)
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59)

    # 2. Берем данные
    calls = await get_calls_in_range(start_of_week, end_of_week)

    # 3. Формируем текст
    period = f"{start_of_week.strftime('%d.%m')} - {end_of_week.strftime('%d.%m')}"
    text = t("schedule_title", lang, period=period)

    if not calls:
        text += t("schedule_empty", lang)
    else:
        # Группируем по дням
        current_day = ""
        for call in calls:
            day_str = call.datetime.strftime("%d.%m (%a)")
            if day_str != current_day:
                text += f"\n<b>🗓 {day_str}</b>\n"
                current_day = day_str
            
            client = await get_client(call.client_id)
            time_str = call.datetime.strftime("%H:%M")
            text += f" • <code>{time_str}</code>: {client.name} ({call.title})\n"

    return text

@schedule_router.message(F.text.in_(all_t("btn_schedule")))
async def show_schedule(message: Message):
    lang, _ = await get_user_settings(message.from_user.id)
    text = await generate_schedule_text(0, lang)
    await message.answer(text, reply_markup=get_schedule_kb(0, lang))


@schedule_router.callback_query(F.data.startswith("sched_"))
async def change_week(callback: CallbackQuery):
    lang, _ = await get_user_settings(callback.from_user.id)
    offset = int(callback.data.split("_")[1])
    text = await generate_schedule_text(offset, lang)
    
    await callback.message.edit_text(text, reply_markup=get_schedule_kb(offset, lang))
    await callback.answer()