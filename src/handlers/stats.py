from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

from src.locales import t, all_t
from src.database.requests import get_user_settings, count_new_clients, count_calls, count_status_changes
from src.database.enums import ClientStatus

stats_router = Router()

def get_stats_menu_kb(lang: str):
    """Keyboard with statistics period options."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_stats_week", lang), callback_data="stats_week")],
        [InlineKeyboardButton(text=t("btn_stats_month", lang), callback_data="stats_month")]
    ])

@stats_router.message(F.text.in_(all_t("btn_stats")))
async def show_stats_menu(message: Message):
    lang, _, _ = await get_user_settings(message.from_user.id)
    await message.answer(t("stats_menu_title", lang), reply_markup=get_stats_menu_kb(lang))

@stats_router.callback_query(F.data.startswith("stats_"))
async def show_stats_report(callback: CallbackQuery):
    lang, _, _ = await get_user_settings(callback.from_user.id)
    period = callback.data.split("_")[1]
    
    today = datetime.now()
    if period == "week":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        period_str = f"{start_date.strftime('%d.%m')} - {end_date.strftime('%d.%m')}"
    else: # month
        start_date = today.replace(day=1)
        next_month = start_date.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)
        period_str = start_date.strftime("%B %Y")

    start_date = start_date.replace(hour=0, minute=0, second=0)
    end_date = end_date.replace(hour=23, minute=59, second=59)

    # --- Get data from DB ---
    new_clients = await count_new_clients(start_date, end_date)
    calls_made = await count_calls(start_date, end_date)
    to_deposit = await count_status_changes(start_date, end_date, ClientStatus.DEPOSIT.value)
    to_dead = await count_status_changes(start_date, end_date, ClientStatus.DEAD.value)

    # --- Format report ---
    report_text = t("stats_report_title", lang, period=period_str) + "\n\n"
    report_text += f"<b>{t('stats_new_clients', lang)}:</b> {new_clients}\n"
    report_text += f"<b>{t('stats_calls_made', lang)}:</b> {calls_made}\n"
    report_text += f"<b>{t('stats_to_deposit', lang)}:</b> {to_deposit}\n"
    report_text += f"<b>{t('stats_to_dead', lang)}:</b> {to_dead}\n"

    await callback.message.edit_text(report_text, reply_markup=get_stats_menu_kb(lang))
    await callback.answer()
