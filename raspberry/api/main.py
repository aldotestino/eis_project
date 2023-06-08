from __future__ import annotations
import datetime
from models import Data, decode
from fastapi import FastAPI, status, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mongo import get_collection
from datetime import datetime
from utils import get_data_from_interval
from neural_net import NeuralNet
import joblib
import torch
import pandas as pd

collection = get_collection()

SHAPE = 6
PORT = 8080

scaler: MinMaxScaler = joblib.load("scaler.save")
neuralNet = NeuralNet(SHAPE)
neuralNet.load_state_dict(torch.load("model", map_location=torch.device('cpu')))

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def make_prediction(records):
    df = pd.DataFrame(data=records)
    columns = ["temperature", "humidity", "pressure"]
    for col in columns:
        df[f"{col}_diff"] = df[col].diff(periods=1)
    
    X = df.values
    X = scaler.transform(X)
    X = torch.from_numpy(X).float()
    prediction = neuralNet(X)
    return prediction.view(-1)[-1].item()


@app.get("/api/data", status_code=status.HTTP_200_OK)
def get_api_data(start: str | None = None, end: str | None = None):
    if start is not None:
        start = datetime.fromisoformat(start)
    if end is not None:
        end = datetime.fromisoformat(end)

    return get_data_from_interval(start=start, end=end)


@app.post("/api/data", status_code=status.HTTP_201_CREATED)
def post_api_data(data: Data = Body(...)):
    result = collection.insert_one(data.encode())
    document = collection.find_one(
        {"_id": result.inserted_id}
    )

    return decode(document)

@app.get("/api/prediction", status_code=status.HTTP_200_OK)
def get_api_prediction():
    documents = collection.find({}).sort("_id", -1).limit(3)
    last_records = [decode(document) for document in documents]
    last_records.reverse()
    last_records = [{"temperature": x["temperature"], "humidity": x["humidity"], "pressure": x["pressure"]} for x in last_records]
    prediction = make_prediction(last_records)
    return {
        "prediction": prediction
    }

@app.get("/api/home", status_code=status.HTTP_200_OK)
def get_api_home():
    documents = collection.find({}).sort("_id", -1).limit(24)
    documents = [decode(document) for document in documents]
    documents.reverse()
    last_records = [{"temperature": x["temperature"], "humidity": x["humidity"], "pressure": x["pressure"]} for x in documents[-2:]]
    prediction = make_prediction(last_records)
    return {
        "timestamps": [x["timestamp"] for x in documents],
        "temperatures": [x["temperature"] for x in documents],
        "humidities": [x["humidity"] for x in documents],
        "pressures": [x["pressure"] for x in documents],
        "prediction": prediction
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
