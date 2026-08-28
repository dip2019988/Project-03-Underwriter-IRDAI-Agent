import hashlib
import json
from typing import Any

import redis

from config.settings import settings
from utils.logger import logger


class RedisCacheService:
    """Manages fast response retrieval for recurring queries."""

    def __init__(self):
        try:
            self.client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                decode_responses=True,
                socket_timeout=2
            )
            self.client.ping()
            self.is_connected = True
            logger.info("[REDIS] Connected to Redis Cache successfully.")
        except Exception as e:
            self.is_connected = False
            logger.warning(f"[REDIS] Redis server unavailable ({e!s}). Proceeding without cache.")

    def _generate_key(self, query: str, user_id: str) -> str:
        """Generates a deterministic cache key for a given user query."""
        normalized = f"{user_id}:{query.strip().lower()}"
        return f"cache:underwriting:{hashlib.md5(normalized.encode()).hexdigest()}"

    def get_cached_solution(self, query: str, user_id: str) -> dict[str, Any] | None:
        """Retrieves cached underwriting result if available."""
        if not self.is_connected:
            return None

        try:
            key = self._generate_key(query, user_id)
            cached_data = self.client.get(key)
            if cached_data:
                logger.info(f"[REDIS] Cache HIT for key: {key}")
                return json.loads(cached_data)
        except Exception as e:
            logger.error(f"[REDIS] Error reading from cache: {e!s}")

        logger.info("[REDIS] Cache MISS.")
        return None

    def set_cached_solution(
        self,
        query: str,
        user_id: str,
        payload: dict[str, Any]
    ):
        """Caches successful underwriting recommendations in Redis."""

        if not self.is_connected:
            return

        try:

            key = self._generate_key(
                query,
                user_id
            )

            self.client.set(
                key,
                json.dumps(payload),
                ex=settings.REDIS_CACHE_TTL
            )

            logger.info(
                f"[REDIS] Cached solution under key: "
                f"{key} "
                f"(TTL: {settings.REDIS_CACHE_TTL}s)"
            )

        except Exception as e:

            logger.error(
                f"[REDIS] Error writing to cache: {e!s}"
            )


redis_service = RedisCacheService()
