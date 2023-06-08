from __future__ import annotations

from datetime import datetime
from mongo import get_collection
from models import decode


def get_data_from_interval(start: datetime | None = None, end: datetime | None = None):
    collection = get_collection()

    if start is not None and end is None:
        cursor = collection.find({"timestamp": {"$gte": start}})
    elif start is None and end is not None:
        cursor = collection.find({"timestamp": {"$lt": end}})
    elif start is not None and end is not None:
        cursor = collection.find({"timestamp": {"$gte": start, "$lt": end}})
    else:
        cursor = collection.find({})

    return [decode(document) for document in cursor]
