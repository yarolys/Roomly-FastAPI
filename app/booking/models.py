from sqlalchemy import Column, Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey("rooms.id"))
    user_id = Column(ForeignKey("users.id"))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("(date_to - date_from) * price"))
    total_day = Column(Integer, Computed("date_to - date_from"))

    room = relationship("Rooms", back_populates="bookings")
