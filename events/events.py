from enum import Enum
from pydantic import BaseModel
import pandas as pd

# Definicion de los distintos tipos de eventos

class EventType(str, Enum):
    DATA = "DATA"
    SIGNAL = "SIGNAL"


class BaseEvent(BaseModel):
    event_type: EventType

    class Config:
        arbitrary_types_allowed = True



class DataEvent(BaseEvent):
    event_type: EventType = EventType.DATA
    symbol: str
    data: pd.Series