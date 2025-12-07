import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import urllib.request
from sqlalchemy import select
from src.database.core import async_session, engine
from src.database.models import Client, Call

# Папка для файлов
MEDIA_DIR = "media"
FONT_PATH = os.path.join(MEDIA_DIR, "DejaVuSans.ttf")
FONT_URL = "https://github.com/py-pdf/fpdf2/raw/master/fpdf/fonts/DejaVuSans.ttf"

def ensure_font_exists():
    """Скачивает шрифт с поддержкой кириллицы, если его нет"""
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)
    
    if not os.path.exists(FONT_PATH):
        print("⏳ Скачиваю шрифт для PDF (DejaVuSans)...")
        try:
            urllib.request.urlretrieve(FONT_URL, FONT_PATH)
            print("✅ Шрифт скачан.")
        except Exception as e:
            print(f"❌ Ошибка скачивания шрифта: {e}")

# --- 1. EXCEL EXPORT ---
async def export_clients_to_excel() -> str:
    """Выгружает всех клиентов в Excel и возвращает путь к файлу"""
    os.makedirs(MEDIA_DIR, exist_ok=True)
    filename = f"{MEDIA_DIR}/clients_base_{int(datetime.now().timestamp())}.xlsx"

    # Используем pandas для SQL запроса
    # Pandas read_sql плохо работает с async движком напрямую, 
    # поэтому выгружаем данные вручную через сессию
    async with async_session() as session:
        result = await session.execute(select(Client))
        clients = result.scalars().all()
        
        # Преобразуем список объектов в список словарей
        data = []
        for c in clients:
            data.append({
                "ID": c.id,
                "Имя": c.name,
                "Телефон": c.phone,
                "Теги": c.tags,
                "Заметки": c.notes,
                "Дата создания": c.created_at.strftime("%Y-%m-%d %H:%M") if c.created_at else ""
            })

    if not data:
        return None

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename

# --- 2. PDF EXPORT ---
async def export_client_to_pdf(client_id: int) -> str:
    """Генерирует PDF-досье клиента"""
    ensure_font_exists() # Проверка шрифта
    
    # 1. Получаем данные
    async with async_session() as session:
        client = await session.get(Client, client_id)
        if not client: return None
        
        # Получаем созвоны
        res = await session.execute(select(Call).where(Call.client_id == client_id))
        calls = res.scalars().all()

    # 2. Создаем PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Подключаем шрифт (важно для русского!)
    try:
        pdf.add_font('DejaVu', '', FONT_PATH, uni=True)
        pdf.set_font('DejaVu', '', 14)
    except:
        # Если шрифт не скачался, будет стандартный (без кириллицы)
        pdf.set_font('Arial', '', 14)

    # Заголовок
    pdf.set_font_size(20)
    pdf.cell(0, 10, f"Dossier: {client.name}", ln=True, align='C')
    pdf.ln(10)

    # Инфо
    pdf.set_font_size(12)
    pdf.cell(0, 10, f"Phone: {client.phone or '---'}", ln=True)
    pdf.cell(0, 10, f"Tags: {client.tags or '---'}", ln=True)
    pdf.ln(5)
    
    # Заметки (MultiCell для многострочного текста)
    pdf.set_font_size(14)
    pdf.cell(0, 10, "Notes / Заметки:", ln=True)
    pdf.set_font_size(12)
    pdf.multi_cell(0, 10, client.notes or "No notes.")
    pdf.ln(10)

    # История созвонов
    if calls:
        pdf.set_font_size(14)
        pdf.cell(0, 10, "Calls & Meetings:", ln=True)
        pdf.set_font_size(10)
        
        # Шапка таблицы
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(40, 10, "Date", 1, 0, 'C', True)
        pdf.cell(100, 10, "Topic", 1, 0, 'C', True)
        pdf.cell(50, 10, "Status", 1, 1, 'C', True)
        
        for call in calls:
            date_str = call.datetime.strftime("%d.%m.%Y %H:%M")
            pdf.cell(40, 10, date_str, 1)
            pdf.cell(100, 10, str(call.title)[:50], 1) # Обрезаем если длинное
            pdf.cell(50, 10, call.status, 1, 1)

    # 3. Сохраняем
    os.makedirs(MEDIA_DIR, exist_ok=True)
    filename = f"{MEDIA_DIR}/client_{client.id}.pdf"
    pdf.output(filename)
    
    return filename