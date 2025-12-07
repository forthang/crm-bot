from ics import Calendar, Event
from datetime import datetime
import os

def create_ics_file(title: str, description: str, start_time: datetime, duration_minutes: int = 60) -> str:
    """
    Создает файл .ics и возвращает путь к нему.
    """
    c = Calendar()
    e = Event()
    
    e.name = title
    e.begin = start_time
    e.description = description
    # По умолчанию встреча длится 1 час
    e.duration = {"minutes": duration_minutes}
    
    c.events.add(e)

    # Создаем папку media, если нет
    os.makedirs("media", exist_ok=True)
    
    # Формируем имя файла (используем timestamp, чтобы имена не путались)
    filename = f"media/invite_{int(start_time.timestamp())}.ics"
    
    with open(filename, 'w') as f:
        f.writelines(c.serialize_iter())
        
    return filename