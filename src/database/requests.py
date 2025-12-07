from sqlalchemy import select, and_, update
from src.database.core import async_session
from src.database.models import User, Client, Call
from datetime import datetime, timedelta
import pytz

async def get_user(telegram_id: int):
    """Checks if a user exists in the database."""
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

async def add_user(telegram_id: int, full_name: str, username: str | None):
    """Adds a new user after password validation."""
    async with async_session() as session:
        user = await session.get(User, telegram_id)
        
        if not user:
            user = User(
                telegram_id=telegram_id,
                full_name=full_name,
                username=username
            )
            session.add(user)
            await session.commit()


async def get_user_settings(telegram_id: int):
    """Returns user settings: (lang, tz, reminder_delay)."""
    async with async_session() as session:
        user = await session.get(User, telegram_id)
        if user:
            return user.language, user.timezone, user.reminder_delay
        return "en", "Europe/Moscow", 10 # Default

async def update_user_settings(telegram_id: int, lang=None, tz=None, delay=None):
    """Updates user settings for language, timezone, and reminder delay."""
    async with async_session() as session:
        user = await session.get(User, telegram_id)
        if user:
            if lang: user.language = lang
            if tz: user.timezone = tz
            if delay is not None: user.reminder_delay = delay
            await session.commit()
            
async def create_client(name: str, phone: str | None, notes: str | None) -> int:
    """Creates a client and returns its ID."""
    async with async_session() as session:
        client = Client(
            name=name,
            phone=phone,
            notes=notes
        )
        session.add(client)
        await session.commit()
        return client.id
    
async def get_all_clients():
    """Returns a list of all clients (id, name)."""
    async with async_session() as session:
        result = await session.execute(select(Client.id, Client.name).order_by(Client.name))
        return result.all()
    
async def get_client(client_id: int):
    """Returns full information about a client by ID."""
    async with async_session() as session:
        return await session.get(Client, client_id)

async def delete_client(client_id: int):
    """Deletes a client."""
    async with async_session() as session:
        client = await session.get(Client, client_id)
        if client:
            await session.delete(client)
            await session.commit()

async def update_client_status(client_id: int, status: str):
    """Updates the status of a client."""
    async with async_session() as session:
        client = await session.get(Client, client_id)
        if client:
            client.status = status
            await session.commit()

async def update_client_notes(client_id: int, notes: str):
    """Updates the notes for a client."""
    async with async_session() as session:
        client = await session.get(Client, client_id)
        if client:
            client.notes = notes
            await session.commit()

async def get_call(call_id: int):
    """Returns full information about a call by ID."""
    async with async_session() as session:
        return await session.get(Call, call_id)

async def update_call_status(call_id: int, status: str):
    """Updates the status of a call."""
    async with async_session() as session:
        call = await session.get(Call, call_id)
        if call:
            call.status = status
            await session.commit()


async def create_call(client_id: int, date_str: str, topic: str, user_timezone: str = "Europe/Moscow") -> int | None:
    """
    Creates a call, taking into account the user's timezone.
    
    :param date_str: A string in the format "DD.MM.YYYY HH:MM".
    :param user_timezone: A string representing the user's timezone (e.g., "Europe/Paris").
    """
    async with async_session() as session:
        try:
            local_tz = pytz.timezone(user_timezone)
            naive_dt = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
            aware_dt = local_tz.localize(naive_dt)
        except ValueError:
            print(f"❌ Date format error: {date_str}")
            return None
        except pytz.UnknownTimeZoneError:
            print(f"❌ Unknown timezone: {user_timezone}")
            local_tz = pytz.timezone("Europe/Moscow") # Fallback
            aware_dt = local_tz.localize(datetime.strptime(date_str, "%d.%m.%Y %H:%M"))

        call = Call(
            client_id=client_id,
            title=topic,
            datetime=aware_dt,
            status="wait"
        )
        session.add(call)
        await session.commit()
        return call.id

async def get_calls_in_range(start_date: datetime, end_date: datetime):
    """Returns calls within a specified date range."""
    async with async_session() as session:
        result = await session.execute(
            select(Call).where(
                and_(
                    Call.datetime >= start_date,
                    Call.datetime <= end_date
                )
            ).order_by(Call.datetime)
        )
        return result.scalars().all()
    
async def get_calls_to_remind(minutes: int = 10):
    """Finds calls that are due in <= `minutes` and for which a reminder has not been sent."""
    async with async_session() as session:
        now = datetime.now()
        target_time = now + timedelta(minutes=minutes)
        
        result = await session.execute(
            select(Call).where(
                and_(
                    Call.datetime > now,
                    Call.datetime <= target_time,
                    Call.reminder_sent == False,
                    Call.status == "wait"
                )
            )
        )
        return result.scalars().all()

async def mark_call_as_reminded(call_id: int):
    """Marks that a reminder has been sent for a call."""
    async with async_session() as session:
        await session.execute(
            update(Call).where(Call.id == call_id).values(reminder_sent=True)
        )
        await session.commit()