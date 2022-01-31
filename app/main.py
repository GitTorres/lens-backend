from datetime import datetime
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional, Tuple
from pymongo import MongoClient
from pymongo.cursor import Cursor
import os
import time
from fastapi.encoders import jsonable_encoder
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict
from functools import reduce
from utils.query import build_filter_query
from bson.binary import Binary, UuidRepresentation
from bson import decode
from uuid import uuid4
from models.types import RegressionSummaryPayload

# read tomorrow
# https://medium.com/codex/python-typing-and-validation-with-mypy-and-pydantic-a2563d67e6d

local_dev_origins = ["http://0.0.0.0:3000", "http://localhost:3000"]
local_prod_origins = ["http://0.0.0.0:8080", "http://localhost:8080"]
origins = local_dev_origins + local_prod_origins

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
mongo_client: Optional[MongoClient] = None


def get_client() -> MongoClient:
    """
    Setup a mongo client for the site
    :return:
    """
    global mongo_client

    if mongo_client is None:
        host: str = os.getenv("MONGODB_HOST", "mongo")
        username: str = quote_plus(os.getenv("MONGODB_USER", ""))
        password: str = quote_plus(os.getenv("MONGODB_PASSWORD", ""))
        port: int = int(os.getenv("MONGODB_PORT", 27017))
        uri: str = f"mongodb://{username}:{password}@{host}:{port}"
        mongo_client = MongoClient(uri, serverSelectionTimeoutMS=1000)

    return mongo_client


@app.get("/")
async def root():
    return {"message": "Udabest"}


@app.get("/modelsummary/regression", response_model=List[RegressionSummaryPayload])
async def get_regression_summary(
    name: Optional[str] = Query(None),
    desc: Optional[str] = Query(None),
    min_explained_variance: Optional[float] = Query(None, ge=0, le=1),
    max_explained_variance: Optional[float] = Query(None, ge=0, le=1),
    features: Optional[List[str]] = Query(None),
):

    # name filter
    name_filter: Optional[Tuple] = ("name", name, "$eq") if name else None

    # description filter
    desc_filter: Optional[Tuple] = ("desc", desc, "$regex") if desc else None

    # min variance filter
    min_var_filter: Optional[Tuple] = (
        ("explained_variance", min_explained_variance, "$gte")
        if min_explained_variance
        else None
    )

    # max variance filter
    max_var_filter: Optional[Tuple] = (
        ("explained_variance", max_explained_variance, "$lte")
        if max_explained_variance
        else None
    )

    # feature filter
    feature_filter: Optional[Tuple] = (
        ("feature_summary.name", features, "$in") if features else None
    )

    params: List[Tuple] = [
        param
        for param in [
            name_filter,
            desc_filter,
            min_var_filter,
            max_var_filter,
            feature_filter,
        ]
        if param
    ]

    print(params)

    # map supplied param filters to valid Object Notation
    query: Dict = build_filter_query(params) if len(params) > 0 else {}

    print(query)

    client = get_client()
    db = client["models"]
    clcn = db["models"]
    summaries: Cursor = clcn.find(query)  # cursors are not awaitable

    response: List[RegressionSummaryPayload] = []
    for summary in summaries:
        response.append(RegressionSummaryPayload(**summary))

    return response


# references to overcome issues encoding UUID as binary and encoding pydantic types as json

# https://stackoverflow.com/questions/23983079/using-pythons-uuid-to-generate-unique-ids-should-i-still-check-for-duplicates
# https://fastapi.tiangolo.com/tutorial/encoder/
# https://pymongo.readthedocs.io/en/stable/examples/uuid.html
# https://pymongo.readthedocs.io/en/stable/api/bson/binary.html


@app.put("/modelsummary/regression", response_model=str)
async def insert_regression_summary(summary: RegressionSummaryPayload):
    client = get_client()
    db = client["models"]
    clcn = db["models"]

    # generate unique id
    binary_uuid = Binary.from_uuid(
        uuid=uuid4(), uuid_representation=UuidRepresentation.STANDARD
    )

    # created at
    inserted_time = time.time()

    # add summary to database
    try:
        _ = clcn.insert_one(
            {
                "_id": binary_uuid,
                "inserted_time": inserted_time,
                **jsonable_encoder(summary),
            }
        )

        response_msg = "ok"
    except:
        response_msg = "error"

    return response_msg
