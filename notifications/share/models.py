from pydantic import BaseModel, Json, Field
from datetime import datetime
from typing import Any, Dict, Optional
import uuid

class Notification(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    user_id: int = Field(type=int)
    active: bool = Field(type=bool)
    name: str = Field(type=str)
    ts: datetime = Field(type=datetime)
    location: str = Field(nullable=True)
    description: str = Field(type=str)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "user_id": 12,
                "active": True,
                "name": "Test Event",
                "ts": datetime(year=2000, month=4, day=1, hour=4, minute=20, second=59),
                "description": "You need to go there",
                "location": "somewhere"
            }
        }


class UpdateNotification(BaseModel):
    name: Optional[str] = Field(type=str)
    ts: Optional[datetime] = Field(type=datetime)
    user_id: Optional[str] = Field(type=str)
    active: Optional[bool] = Field(type=bool, default=True)
    name: Optional[str] = Field(type=str)
    ts: Optional[datetime] = Field(type=datetime)
    location: Optional[str] = Field(type=str)
    description: Optional[str] = Field(type=str)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "user_id": 12,
                "active": True,
                "name": "Test Event",
                "ts": datetime(year=2000, month=4, day=1, hour=4, minute=20, second=59),
                "description": "You need to go there",
                "location": "somewhere"
            }
        }

class Message(BaseModel):
    origin_id: str = Field(type=str)
    user_id: int = Field(type=int)
    tg_id: int = Field(type=int)
    ts: datetime = Field(type=datetime)
    message: str = Field(type=str)
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "origin_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "user_id": 12,
                "ts": datetime(year=2000, month=4, day=1, hour=4, minute=20, second=59),
                "tg_id": 23453525235235,
                "message": "Well hello there"
            }
        }