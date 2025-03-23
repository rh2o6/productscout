import redis
import os
from dotenv import load_dotenv

print("\n",load_dotenv(dotenv_path='info.env'))

# Load Redis configuration
host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
password = os.getenv("REDIS_PASSWORD")

if host is None or port is None:
    raise ValueError("REDIS_HOST and REDIS_PORT must be set in the environment variables.")

# Convert port to int
try:
    port = int(port)
except ValueError:
    raise ValueError("REDIS_PORT must be an integer.")

try:
    r = redis.Redis(
      host=host,
      port=port,
      password=password or None  # Use None if no password is set
    )
    # Test the connection
    r.ping()
    #print("Connected to Redis")
except redis.ConnectionError as e:
    print(f"Redis connection failed: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
