from fastapi.middleware.cors import CORSMiddleware
from importlib import import_module
from routers import MyRouterAPI
from fastapi import FastAPI
import redis
import os


# Define docker-stuff, might be useful to use dotenv file later.
REJSON_HOST = "rejson"
REJSON_PORT = 6379
REJSON_DB_NUM = 0

redis_client = redis.Redis(host=REJSON_HOST, port=REJSON_PORT, db=REJSON_DB_NUM)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Naivly add all routes in routes folder, only need to specify the important FastAPI parts.
for dirpath, _, files in os.walk("routers"):
    if any(("_" == x[0] for x in dirpath.split("\\"))):
        continue
    for module in files:
        # Don't load files/folders starting with '_'.
        # Also works as commenting out routings; _routerNameFolder
        if module[0] == "_":
            continue
        # Each module should create a MyRouterAPI object which adds the routers to a list which the Class contains.
        # This is a very convoluted way to fix the linter to stop yelling at me, and also easier to extend and maintain.
        # The for loop loads the module which creates a router and adds to list in class, which we pop off and include to FastAPI.
        import_module('{}.{}'.format(dirpath.replace("\\", "."), module[:-3]))
        app.include_router(MyRouterAPI.xs.pop())
