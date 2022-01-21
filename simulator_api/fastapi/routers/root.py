from main import redis_client as client
from fastapi import HTTPException
from pydantic import BaseModel
from . import MyRouterAPI
import pickle

# Settings
PREFIX = ""
TAGS = ["root"]

# To route the routings down the document.
router = MyRouterAPI(prefix=PREFIX, tags=TAGS).router

# Define schema


class Data(BaseModel):
    key_x: int
    key_y: int
    time: str


class ResponseData(BaseModel):
    response: Data


# Define an example response
api_responses = {
    200: {
        "description": "Simulated Quantum Data",
        "content": {
            "application/json": {
                "example": {
                    "key_x": 42,
                    "key_y": 1337,
                    "time": "2000-01-31T11:22:33.444444"
                }
            }
        }
    },
    204: {}
}

# Routing
@router.get("/", response_model=ResponseData,
            responses=api_responses, # type:ignore
            include_in_schema=True)
async def root():
    data = client.get("data")
    if data is not None:
        data = pickle.loads(data)
        if isinstance(data, dict):
            return {"response": data}
    raise HTTPException(status_code=204)
