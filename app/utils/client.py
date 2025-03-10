from redis.asyncio import Redis

r_client: Redis = Redis(
    host="localhost",
    port=6379,
)
