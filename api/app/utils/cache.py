import json
import logging
from typing import Any, Optional, List, Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis_client = None
        self.is_redis_available = False
        # In-memory cache as fallback
        self.memory_cache = {}
        self.chat_history = {}
    
    async def initialize(self):
        """Initialize cache (fallback to memory if Redis unavailable)"""
        try:
            import redis.asyncio as redis
            self.redis_client = redis.from_url(self.redis_url)
            await self.redis_client.ping()
            self.is_redis_available = True
            logger.info("✅ Redis cache manager initialized")
        except Exception as e:
            logger.warning(f"⚠️ Redis not available, using memory cache: {e}")
            self.is_redis_available = False
            logger.info("✅ Memory cache manager initialized")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.is_redis_available and self.redis_client:
                value = await self.redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                # Use memory cache
                return self.memory_cache.get(key)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL"""
        try:
            if self.is_redis_available and self.redis_client:
                serialized_value = json.dumps(value, default=str)
                await self.redis_client.setex(key, ttl, serialized_value)
            else:
                # Use memory cache (ignore TTL for simplicity)
                self.memory_cache[key] = value
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def add_to_chat_history(self, session_id: str, user_message: str, assistant_response: str):
        """Add conversation to chat history"""
        try:
            conversation = {
                "user_message": user_message,
                "assistant_response": assistant_response,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            if self.is_redis_available and self.redis_client:
                key = f"chat_history:{session_id}"
                await self.redis_client.lpush(key, json.dumps(conversation))
                await self.redis_client.ltrim(key, 0, 49)
                await self.redis_client.expire(key, 86400)
            else:
                # Use memory cache
                if session_id not in self.chat_history:
                    self.chat_history[session_id] = []
                self.chat_history[session_id].insert(0, conversation)
                # Keep only last 50 messages
                self.chat_history[session_id] = self.chat_history[session_id][:50]
                
        except Exception as e:
            logger.error(f"Failed to add to chat history: {e}")
    
    async def get_chat_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Get chat history for session"""
        try:
            if self.is_redis_available and self.redis_client:
                key = f"chat_history:{session_id}"
                messages = await self.redis_client.lrange(key, 0, limit - 1)
                history = []
                for msg in messages:
                    try:
                        history.append(json.loads(msg))
                    except json.JSONDecodeError:
                        continue
                return list(reversed(history))
            else:
                # Use memory cache
                history = self.chat_history.get(session_id, [])
                return list(reversed(history[:limit]))
                
        except Exception as e:
            logger.error(f"Failed to get chat history: {e}")
            return []
    
    async def clear_chat_history(self, session_id: str):
        """Clear chat history for session"""
        try:
            if self.is_redis_available and self.redis_client:
                key = f"chat_history:{session_id}"
                await self.redis_client.delete(key)
            else:
                # Use memory cache
                if session_id in self.chat_history:
                    del self.chat_history[session_id]
            return True
        except Exception as e:
            logger.error(f"Failed to clear chat history: {e}")
            return False
    
    async def health_check(self) -> bool:
        """Check cache health"""
        try:
            if self.is_redis_available and self.redis_client:
                await self.redis_client.ping()
                return True
            else:
                # Memory cache is always "healthy"
                return True
        except Exception:
            return False
    
    async def close(self):
        """Close connections"""
        if self.is_redis_available and self.redis_client:
            await self.redis_client.close()
