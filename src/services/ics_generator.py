from ics import Calendar, Event
from datetime import datetime
import os

def create_ics_file(title: str, description: str, start_time: datetime, duration_minutes: int = 60) -> str:
    """
    Creates an .ics file and returns the path to it.
    """
    c = Calendar()
    e = Event()
    
    e.name = title
    e.begin = start_time
    e.description = description
    # By default, the meeting lasts 1 hour
    e.duration = {"minutes": duration_minutes}
    
    c.events.add(e)

    # Create the media folder if it doesn't exist
    os.makedirs("media", exist_ok=True)
    
    # Form the filename (using a timestamp to avoid conflicts)
    filename = f"media/invite_{int(start_time.timestamp())}.ics"
    
    with open(filename, 'w') as f:
        f.writelines(c.serialize_iter())
        
    return filename