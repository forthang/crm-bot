from datetime import datetime
from sqlalchemy import BigInteger, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

# --- Таблица Пользователей (Админы/Юзеры) ---
class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    
    # Новые поля
    language: Mapped[str] = mapped_column(String(10), default="ru")
    timezone: Mapped[str] = mapped_column(String(50), default="Europe/Moscow")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

# --- Таблица Клиентов ---
class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255)) # Имя клиента
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    # Описание от ИИ или пользователя
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Теги (храним строкой через запятую: "VIP,Теплый")
    tags: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Связи (чтобы удобно получать созвоны клиента)
    calls = relationship("Call", back_populates="client", cascade="all, delete-orphan")
    history = relationship("History", back_populates="client", cascade="all, delete-orphan")

# --- Таблица Созвонов ---
class Call(Base):
    __tablename__ = 'calls'

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    
    title: Mapped[str] = mapped_column(String(255)) # Тема созвона
    datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True)) # type: ignore # Когда
    
    # Статусы: wait (ждет), done (выполнен), cancel (отменен)
    status: Mapped[str] = mapped_column(String(50), default="wait") 
    
    reminder_sent: Mapped[bool] = mapped_column(Boolean, default=False) # Отправили ли напоминание?

    client = relationship("Client", back_populates="calls")

# --- История действий (Логи) ---
class History(Base):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    
    # Тип действия: "voice_note", "manual_edit", "call_status"
    action_type: Mapped[str] = mapped_column(String(50))
    text: Mapped[str] = mapped_column(Text) # Текст события
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="history")