from sqlalchemy import JSON, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    rooms = relationship("Rooms", back_populates="hotel")

    def to_dict(self):
        """Преобразуем объект в словарь для сериализации."""
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "services": self.services,
            "rooms_quantity": self.rooms_quantity,
            "image_id": self.image_id,
        }


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    bookings = relationship("Bookings", back_populates="room")
    hotel = relationship("Hotels", back_populates="rooms")

    def to_dict(self):
        return {
            "id": self.id,
            "hotel_id": self.hotel_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "services": self.services,
            "quantity": self.quantity,
            "image_id": self.image_id,
        }
