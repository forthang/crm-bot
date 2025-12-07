from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from src.database.requests import get_user

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        # Получаем данные пользователя
        user_id = event.from_user.id
        
        # Стучимся в базу: знает ли она такого?
        user = await get_user(user_id)

        # Если пользователь есть в базе — пропускаем дальше
        if user:
            return await handler(event, data)

        # Если пользователя нет, пропускаем только команду /start или ввод пароля
        # Но логику ввода пароля мы обработаем в хендлере, так что 
        # здесь мы просто разрешаем проход, чтобы хендлер сам решил, что делать.
        # В более сложных системах тут можно блокировать апдейты.
        
        return await handler(event, data)