from pydantic import BaseModel, Field
from typing import Literal, Optional

Priority = Literal["low", "medium", "high", "critical"]
Status = Literal["open", "in_progress", "resolved", "closed"]

class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=5, max_length=2000)
    priority: Priority
    reporter: str = Field(min_length=2, max_length=100)

class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=120)
    description: Optional[str] = Field(default=None, min_length=5, max_length=2000)
    priority: Optional[Priority] = None
    status: Optional[Status] = None

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=4, max_length=100)
