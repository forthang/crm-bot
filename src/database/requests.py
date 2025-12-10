from sqlalchemy import select, and_, update, func
from src.database.core import async_session
from src.database.models import User, Client, Call, History, CallNote
from src.database.enums import ClientStatus
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

async def get_all_users():
    """Returns all users from the database."""
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

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
    
async def get_all_clients(limit: int, offset: int):
    """Returns a paginated list of all clients (id, name)."""
    async with async_session() as session:
        result = await session.execute(
            select(Client.id, Client.name)
            .order_by(Client.name)
            .limit(limit)
            .offset(offset)
        )
        return result.all()

async def count_all_clients() -> int:
    """Counts the total number of clients."""
    async with async_session() as session:
        result = await session.execute(select(func.count(Client.id)))
        return result.scalar_one()


async def search_clients_by_name(query: str):
    """Returns a list of clients matching the search query (id, name)."""
    async with async_session() as session:
        result = await session.execute(
            select(Client.id, Client.name)
            .where(Client.name.ilike(f"%{query}%"))
            .order_by(Client.name)
        )
        return result.all()

async def get_clients_by_status(status: str):
    """Returns a list of all clients with a given status (id, name)."""
    async with async_session() as session:
        result = await session.execute(
            select(Client.id, Client.name)
            .where(Client.status == status)
            .order_by(Client.name)
        )
        return result.all()

async def find_client_by_exact_name(name: str):
    """Finds a single client by case-insensitive exact name match."""
    async with async_session() as session:
        result = await session.execute(
            select(Client).where(func.lower(Client.name) == func.lower(name))
        )
        return result.scalar_one_or_none()
    
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
    """Updates the status of a client and logs the change."""
    async with async_session() as session:
        client = await session.get(Client, client_id)
        if client:
            old_status_val = client.status.value if isinstance(client.status, ClientStatus) else client.status
            
            if old_status_val != status:
                client.status = ClientStatus(status) # Assign the enum member
                history_log = History(
                    client_id=client_id,
                    action_type="status_change",
                    text=f"{old_status_val} -> {status}"
                )
                session.add(history_log)
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

async def add_call_note(call_id: int, text: str):
    """Adds a note to a specific call."""
    async with async_session() as session:
        note = CallNote(
            call_id=call_id,
            text=text
        )
        session.add(note)
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

async def get_history_for_client(client_id: int, limit: int, offset: int):
    """Returns a paginated list of history records for a specific client."""
    async with async_session() as session:
        result = await session.execute(
            select(History)
            .where(History.client_id == client_id)
            .order_by(History.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

async def count_history_for_client(client_id: int) -> int:
    """Counts the total number of history records for a client."""
    async with async_session() as session:
        result = await session.execute(
            select(func.count(History.id))
            .where(History.client_id == client_id)
        )
        return result.scalar_one()

async def get_calls_for_today(user_tz: str):
    """Returns calls scheduled for today in the user's timezone."""
    async with async_session() as session:
        try:
            tz = pytz.timezone(user_tz)
        except pytz.UnknownTimeZoneError:
            tz = pytz.timezone("UTC")
            
        now = datetime.now(tz)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        result = await session.execute(
            select(Call)
            .where(
                and_(
                    Call.datetime >= start_of_day,
                    Call.datetime < end_of_day,
                    Call.status == "wait"
                )
            )
            .order_by(Call.datetime)
        )
        return result.scalars().all()

async def get_overdue_calls():
    """Returns calls with 'wait' status that are in the past."""
    async with async_session() as session:
        now = datetime.now(pytz.utc)
        result = await session.execute(
            select(Call)
            .where(
                and_(
                    Call.datetime < now,
                    Call.status == "wait"
                )
            )
            .order_by(Call.datetime.desc())
        )
        return result.scalars().all()

# ==========================================
# 📈 STATISTICS
# ==========================================

async def count_new_clients(start_date: datetime, end_date: datetime) -> int:
    """Counts new clients created within a date range."""
    async with async_session() as session:
        result = await session.execute(
            select(func.count(Client.id))
            .where(and_(Client.created_at >= start_date, Client.created_at <= end_date))
        )
        return result.scalar_one()

async def count_calls(start_date: datetime, end_date: datetime) -> int:
    """Counts calls created within a date range."""
    async with async_session() as session:
        result = await session.execute(
            select(func.count(Call.id))
            .where(and_(Call.datetime >= start_date, Call.datetime <= end_date))
        )
        return result.scalar_one()

async def count_status_changes(start_date: datetime, end_date: datetime, status: str) -> int:
    """Counts how many clients were moved to a specific status within a date range."""
    async with async_session() as session:
        result = await session.execute(
            select(func.count(History.id))
            .where(and_(
                History.created_at >= start_date, 
                History.created_at <= end_date,
                History.action_type == 'status_change',
                History.text.like(f"% -> {status}")
            ))
        )
        return result.scalar_one()