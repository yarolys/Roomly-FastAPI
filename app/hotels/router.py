import asyncio
from datetime import date, datetime, timezone, timedelta
from typing import List, Optional
from pydantic import TypeAdapter

from fastapi import APIRouter, FastAPI, Query

from app.utils.redis_cache import redis_cache
from app.hotels.dao import HotelDAO
from app.hotels.schemas import Hotel, HotelInfo, RoomInfo


app = FastAPI()


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("/{location}")
@redis_cache(ttl=10)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например: {datetime.now(timezone.utc).date()}"),
    date_to: date = Query(..., description=f"Например: {datetime.now(timezone.utc).date()}"),
):
    hotels = await HotelDAO.search_for_hotels(location, date_from, date_to)
    hotel_info_adapter = TypeAdapter(List[HotelInfo])
    hotels_json = hotel_info_adapter.validate_python(hotels)

    return hotels_json


@app.get("/hotels/{hotel_id}")
def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
    has_spa: Optional[int] = Query(None, ge=1, le=5),
):
    return date_from, date_to