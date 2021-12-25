from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Tuple
from pymongo import MongoClient
from pymongo.cursor import Cursor
import os
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict
from functools import reduce
from utils.query import build_filter_query

# read tomorrow
# https://medium.com/codex/python-typing-and-validation-with-mypy-and-pydantic-a2563d67e6d

origins = ["http://0.0.0.0:3000", "http://localhost:3000"]


class FeatureSummaryData(BaseModel):  # pylint: disable=missing-class-docstring
    bin_edge_right: List[float]
    sum_target: List[float]
    sum_prediction: List[float]
    sum_weight: List[float]
    wtd_avg_prediction: List[float]
    wtd_avg_target: List[float]


class FeatureSummary(BaseModel):  # pylint: disable=missing-class-docstring
    name: str
    data: FeatureSummaryData


class RegressionSummaryPayload(BaseModel):  # pylint: disable=missing-class-docstring
    name: str
    desc: str
    target: str
    prediction: str
    var_weights: str
    link_function: str
    error_dist: str
    explained_variance: float
    feature_summary: List[FeatureSummary]


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
    name: Optional[str] = None,
    desc: Optional[str] = None,
    min_explained_variance: Optional[float] = None,
    max_explained_variance: Optional[float] = None,
):

    # name filter
    name_filter: Tuple = ("name", name, "$eq")

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

    params: List[Tuple] = [
        param
        for param in [name_filter, desc_filter, min_var_filter, max_var_filter]
        if param
    ]

    # map supplied param filters to valid Object Notation
    query: Dict = build_filter_query(params)

    print(query)

    client = get_client()
    db = client["models"]
    clcn = db["models"]
    summaries: Cursor = clcn.find(query)  # cursors are not awaitable

    response: List[RegressionSummaryPayload] = []
    for summary in summaries:
        response.append(RegressionSummaryPayload(**summary))

    return response
