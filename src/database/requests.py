
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
