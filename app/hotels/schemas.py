from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[List[str]] 
    rooms_quantity: int
    image_id: Optional[int]

    class Config:
        orm_mode = True



class RoomInfo(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    price: int
    services: List[str]
    quantity: int
    image_id: Optional[int]

    class Config:
        orm_mode = True


class Hotel(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[dict]
    rooms_quantity: int
    image_id: Optional[int]

    class Config:
        orm_mode = True


class HotelInfo(SHotels):
    rooms: List[RoomInfo]  
