from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
import os
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict
from fastapi.responses import JSONResponse

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


class GLMSummaryPayload(BaseModel):  # pylint: disable=missing-class-docstring
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
    return {"message": "Hello World"}


@app.get("/modelsummary/glm/{name}/", response_model=List[GLMSummaryPayload])
async def get_glm_summary(name: str):
    criteria = {"name": name}
    client = get_client()
    db = client["models"]
    clcn = db["models"]
    summaries = clcn.find(criteria)

    response: List[GLMSummaryPayload] = []
    for summary in summaries:
        response.append(GLMSummaryPayload(**summary))

    return response
