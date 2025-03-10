from typing import Optional
from datetime import date
from pydantic import BaseModel

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_cache.backends.inmemory import InMemoryBackend

from redis import asyncio as aioredis

from app.booking.router import router as booking_router
from app.users.router import router as users_router
from app.pages.router import router as pages_router
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield  


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), "static")


app.include_router(users_router)
app.include_router(booking_router)
app.include_router(pages_router)
app.include_router(hotels_router)
app.include_router(images_router)


origins = [
    "https://mysite.com",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"]
)


@app.get("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")