"""
Redis connection utility module.
"""
import os
import logging
import redis

logger = logging.getLogger(__name__)

def get_redis_client():
    """
    Get a configured Redis client.
    Reads REDIS_URL from environment or defaults to localhost.
    """
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    try:
        return redis.from_url(redis_url, decode_responses=True)
    except Exception as e:
        logger.error("Error connecting to Redis at %s: %s", redis_url, e)
        raise
