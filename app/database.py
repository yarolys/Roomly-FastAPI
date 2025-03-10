import os
from dotenv import load_dotenv

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker



load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) # noqa
metadata = MetaData()

class Base(DeclarativeBase):
    pass
