from sqlalchemy import select, and_, update
from src.database.core import async_session
from src.database.models import User, Client, Call
from datetime import datetime, timedelta
import pytz
async def get_user(telegram_id: int):
    """Проверяем, есть ли пользователь в базе"""
    async with async_session() as session:
        # Делаем запрос: найти юзера по ID
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

async def add_user(telegram_id: int, full_name: str, username: str | None):
    """Добавляем нового пользователя (после ввода пароля)"""
    async with async_session() as session:
        # Проверяем, может он уже есть (на всякий случай)
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
    """Возвращает настройки пользователя: (lang, tz)"""
    async with async_session() as session:
        user = await session.get(User, telegram_id)
        if user:
            return user.language, user.timezone
        return "ru", "Europe/Moscow" # Дефолт

async def update_user_settings(telegram_id: int, lang=None, tz=None):
    async with async_session() as session:
        user = await session.get(User, telegram_id)
        if user:
            if lang: user.language = lang
            if tz: user.timezone = tz
            await session.commit()
            
async def create_client(name: str, phone: str | None, notes: str | None) -> int:
    """Создает клиента и возвращает его ID"""
    async with async_session() as session:
        client = Client(
            name=name,
            phone=phone,
            notes=notes,
            tags="Новый" # Тег по умолчанию
        )
        session.add(client)
        await session.commit()
        return client.id
    
async def get_all_clients():
    """Возвращает список всех клиентов (id, name)"""
    async with async_session() as session:
        # Берем только ID и Имя, чтобы не грузить всю базу
        result = await session.execute(select(Client.id, Client.name).order_by(Client.name))
        return result.all()
    
async def get_client(client_id: int):
    """Возвращает полную информацию о клиенте по ID"""
    async with async_session() as session:
        return await session.get(Client, client_id)

async def delete_client(client_id: int):
    """Удаляет клиента"""
    async with async_session() as session:
        client = await session.get(Client, client_id)
        if client:
            await session.delete(client)
            await session.commit()



async def create_call(client_id: int, date_str: str, topic: str, user_timezone: str = "Europe/Moscow") -> int | None:
    """
    Создает созвон с учетом часового пояса пользователя.
    
    :param date_str: Строка вида "25.10.2024 15:00"
    :param user_timezone: Строка вида "Europe/Paris" (из настроек юзера)
    """
    async with async_session() as session:
        try:
            # 1. Создаем объект Timezone
            local_tz = pytz.timezone(user_timezone)
            
            # 2. Парсим строку в "наивный" datetime (без пояса)
            naive_dt = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
            
            # 3. "Локализуем" дату - говорим питону: "Это время в Париже"
            aware_dt = local_tz.localize(naive_dt)
            
            # (При сохранении SQLAlchemy сама приведет aware_dt к UTC, 
            # так как поле в БД определено как DateTime(timezone=True))
            
        except ValueError:
            print(f"❌ Ошибка формата даты: {date_str}")
            return None
        except pytz.UnknownTimeZoneError:
            print(f"❌ Неизвестный часовой пояс: {user_timezone}")
            # Фоллбэк на Москву, если пояс кривой
            local_tz = pytz.timezone("Europe/Moscow")
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
    """Возвращает созвоны в диапазоне дат"""
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
    
async def get_calls_to_remind():
    """Ищет созвоны, до которых осталось <= 10 минут и напоминание НЕ отправлено"""
    async with async_session() as session:
        now = datetime.now()
        target_time = now + timedelta(minutes=10) # Смотрим на 10 мин вперед
        
        # Логика: Время созвона больше чем "сейчас", но меньше чем "через 10 мин"
        # И статус reminder_sent = False
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
    """Ставит галочку, что напоминание отправлено"""
    async with async_session() as session:
        await session.execute(
            update(Call).where(Call.id == call_id).values(reminder_sent=True)
        )
        await session.commit()