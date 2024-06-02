import redis
from decouple import config

redis_host = config("REDIS_HOST")
redis_port = config("REDIS_PORT")
redis_db = config("REDIS_DB", 0)
redis_password = config("REDIS_PASSWORD", None)

client = redis.StrictRedis(
    host=redis_host, port=redis_port, db=redis_db, password=redis_password
)
