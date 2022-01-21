from datetime import datetime
import pickle
import redis
import time

# Docker hostnames is the address. Configure docker-compose for private/public access.
REDIS_HOST = "redis"
REDIS_PORT = 6379

# Redis has default 0-15 databases configured to be able to use the same host for multiple projects
# Select 0 for now.
REDIS_DB_NUM = 0


def main():
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_NUM)

    while(True):
        fetched_data = get_data()

        # Alt 1 - Pickle. Data keeps data in python form. Just unpack it later.
        # Alt 2 - Unpack using for and dict.items(), set each value to each key in redis.
        client.set("data", pickle.dumps(fetched_data))

        time.sleep(2)

# Only for demostration purposes. Global variables/function should be replaced with real fetched values.
key_x = 0
key_y = 1000


def get_data() -> dict:
    global key_x, key_y
    data = {"key_x": key_x, "key_y": key_y, "time": datetime.utcnow().isoformat("T")}

    key_x += 1
    key_y += 5
    if key_x == 1000:
        key_x = 0
    if key_y == 2000:
        key_y = 1000

    return data


if __name__ == "__main__":
    main()
