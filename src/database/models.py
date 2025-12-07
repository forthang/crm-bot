from datetime import datetime
from sqlalchemy import BigInteger, String, Text, ForeignKey, DateTime, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from src.database.enums import ClientStatus

class Base(DeclarativeBase):
    pass

# --- Users Table (Admins/Users) ---
class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    
    # New fields
    language: Mapped[str] = mapped_column(String(10), default="en")
    timezone: Mapped[str] = mapped_column(String(50), default="Europe/Moscow")
    reminder_delay: Mapped[int] = mapped_column(Integer, default=10)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

from src.database.enums import ClientStatus
# --- Clients Table ---
class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255)) # Client name
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    # Description from AI or user
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    status: Mapped[ClientStatus] = mapped_column(String(50), default=ClientStatus.NEW)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships (to easily retrieve client calls)
    calls = relationship("Call", back_populates="client", cascade="all, delete-orphan")
    history = relationship("History", back_populates="client", cascade="all, delete-orphan")

# --- Calls Table ---
class Call(Base):
    __tablename__ = 'calls'

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    
    title: Mapped[str] = mapped_column(String(255)) # Call topic
    datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True)) # type: ignore # When
    
    # Statuses: wait, done, cancel
    status: Mapped[str] = mapped_column(String(50), default="wait") 
    
    reminder_sent: Mapped[bool] = mapped_column(Boolean, default=False) # Has a reminder been sent?

    client = relationship("Client", back_populates="calls")

# --- History Table (Logs) ---
class History(Base):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    
    # Action type: "voice_note", "manual_edit", "call_status"
    action_type: Mapped[str] = mapped_column(String(50))
    text: Mapped[str] = mapped_column(Text) # Event text
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="history")