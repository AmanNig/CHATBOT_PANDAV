# cache.py
import redis, json
from initialize.config import REDIS_URL

# Connect, auto-decode strings
cache = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_cached(question: str):
    key = question.lower().strip()
    raw = cache.get(key)
    return json.loads(raw) if raw else None

def set_cached(question: str, data: dict, ttl: int = 86400):
    key = question.lower().strip()
    cache.set(key, json.dumps(data), ex=ttl)
