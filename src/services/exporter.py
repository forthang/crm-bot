import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import urllib.request
from sqlalchemy import select
from src.database.core import async_session, engine
from src.database.models import Client, Call

# Folder for files
MEDIA_DIR = "media"
FONT_PATH = os.path.join(MEDIA_DIR, "DejaVuSans.ttf")
FONT_URL = "https://github.com/py-pdf/fpdf2/raw/master/fpdf/fonts/DejaVuSans.ttf"

def ensure_font_exists():
    """Downloads the font with Cyrillic support if it doesn't exist"""
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)
    
    if not os.path.exists(FONT_PATH):
        print("⏳ Downloading font for PDF (DejaVuSans)...")
        try:
            urllib.request.urlretrieve(FONT_URL, FONT_PATH)
            print("✅ Font downloaded.")
        except Exception as e:
            print(f"❌ Error downloading font: {e}")

# --- 1. EXCEL EXPORT ---
async def export_clients_to_excel() -> str:
    """Exports all clients to Excel and returns the file path"""
    os.makedirs(MEDIA_DIR, exist_ok=True)
    filename = f"{MEDIA_DIR}/clients_base_{int(datetime.now().timestamp())}.xlsx"

    # Using pandas for the SQL query
    # Pandas read_sql works poorly with async engines directly,
    # so we export the data manually through a session
    async with async_session() as session:
        result = await session.execute(select(Client))
        clients = result.scalars().all()
        
        # Convert the list of objects to a list of dictionaries
        data = []
        for c in clients:
            data.append({
                "ID": c.id,
                "Name": c.name,
                "Phone": c.phone,
                "Status": c.status,
                "Notes": c.notes,
                "Creation Date": c.created_at.strftime("%Y-%m-%d %H:%M") if c.created_at else ""
            })

    if not data:
        return None

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename

# --- 2. PDF EXPORT ---
async def export_client_to_pdf(client_id: int) -> str:
    """Generates a PDF dossier for a client"""
    ensure_font_exists() # Check for font
    
    # 1. Get data
    async with async_session() as session:
        client = await session.get(Client, client_id)
        if not client: return None
        
        # Get calls
        res = await session.execute(select(Call).where(Call.client_id == client_id))
        calls = res.scalars().all()

    # 2. Create PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Add font (important for non-latin characters!)
    try:
        pdf.add_font('DejaVu', '', FONT_PATH, uni=True)
        pdf.set_font('DejaVu', '', 14)
    except:
        # If the font didn't download, it will use a standard one
        pdf.set_font('Arial', '', 14)

    # Title
    pdf.set_font_size(20)
    pdf.cell(0, 10, f"Dossier: {client.name}", ln=True, align='C')
    pdf.ln(10)

    # Info
    pdf.set_font_size(12)
    pdf.cell(0, 10, f"Phone: {client.phone or '---'}", ln=True)
    pdf.cell(0, 10, f"Status: {client.status or '---'}", ln=True)
    pdf.ln(5)
    
    # Notes (MultiCell for multi-line text)
    pdf.set_font_size(14)
    pdf.cell(0, 10, "Notes:", ln=True)
    pdf.set_font_size(12)
    pdf.multi_cell(0, 10, client.notes or "No notes.")
    pdf.ln(10)

    # Call History
    if calls:
        pdf.set_font_size(14)
        pdf.cell(0, 10, "Calls & Meetings:", ln=True)
        pdf.set_font_size(10)
        
        # Table header
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(40, 10, "Date", 1, 0, 'C', True)
        pdf.cell(100, 10, "Topic", 1, 0, 'C', True)
        pdf.cell(50, 10, "Status", 1, 1, 'C', True)
        
        for call in calls:
            date_str = call.datetime.strftime("%d.%m.%Y %H:%M")
            pdf.cell(40, 10, date_str, 1)
            pdf.cell(100, 10, str(call.title)[:50], 1) # Truncate if long
            pdf.cell(50, 10, call.status, 1, 1)

    # 3. Save
    os.makedirs(MEDIA_DIR, exist_ok=True)
    filename = f"{MEDIA_DIR}/client_{client.id}.pdf"
    pdf.output(filename)
    
    return filename