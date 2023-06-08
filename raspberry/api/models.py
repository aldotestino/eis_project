from typing import Mapping, Any
from pydantic import BaseModel, Field
from datetime import datetime


def decode(document: Mapping[str, Any]):
    return {
        "id": str(document.get("_id")),
        "timestamp": document.get("timestamp"),
        "temperature": document.get("temperature"),
        "humidity": document.get("humidity"),
        "pressure": document.get("pressure")
    }

class Data(BaseModel):
    timestamp: str = Field(...)
    temperature: float = Field(...)
    humidity: float = Field(...)
    pressure: float = Field(...)

    def encode(self):
        return {
         "timestamp": datetime.strptime(self.timestamp[:-5], "%Y-%m-%dT%H:%M:%S"),
         "temperature": self.temperature,
         "humidity": self.humidity,
         "pressure": self.pressure
    }

