from pydantic import BaseModel
from typing import Optional
from datetime import date


class SessionCreate(BaseModel):
    subject_id: int
    duration_minutes: int
    notes: Optional[str] = None
    date: Optional[date] = None


class SubjectCreate(BaseModel):
    name: str
    daily_goal_minutes: int


class SubjectOut(SubjectCreate):
    id: int

    class Config:
        from_attributes = True


class SessionOut(BaseModel):
    id: int
    subject_id: int
    duration_minutes: int
    notes: Optional[str] = None
    date: date  # ← remove Optional, it WILL always have a date

    class Config:
        from_attributes = True