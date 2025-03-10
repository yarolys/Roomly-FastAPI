from datetime import date
from sqlalchemy import select, and_, or_, func

from app.booking.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.models import Hotels, Rooms
from app.database import async_session_maker


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_all_hotels(cls):
        async with async_session_maker() as session:
            query = select(Hotels)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def search_for_hotels(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            # CTE для поиска забронированных номеров
            booked_rooms = (
                select(Rooms.id)
                .join(Bookings)  # Используем связь bookings
                .where(
                    or_(
                        and_(Bookings.date_from <= date_to, Bookings.date_from >= date_from),
                        and_(Bookings.date_from <= date_from, Bookings.date_to > date_from)
                    )
                )
                .cte("booked_rooms")
            )

            # Запрос для поиска отелей с доступными номерами
            query = (
                select(Hotels)
                .join(Rooms, Rooms.hotel_id == Hotels.id)
                .where(
                    and_(
                        Hotels.location.ilike(f"%{location}%"),
                        ~Rooms.id.in_(select(booked_rooms.c.id))  # Исключаем забронированные комнаты
                    )
                )
                .group_by(Hotels.id)
            )

            result = await session.execute(query)
            hotels = result.scalars().all()

            # Добавляем информацию о комнатах для каждого отеля
            hotel_data = []
            for hotel in hotels:
                # Получаем комнаты для текущего отеля
                rooms_query = select(Rooms).where(Rooms.hotel_id == hotel.id)
                rooms_result = await session.execute(rooms_query)
                rooms = rooms_result.scalars().all()

                # Преобразуем комнаты в словари
                rooms_data = [room.to_dict() for room in rooms]

                # Преобразуем отель в словарь и добавляем комнаты
                hotel_dict = hotel.to_dict()
                hotel_dict["rooms"] = rooms_data
                hotel_data.append(hotel_dict)

            return hotel_data