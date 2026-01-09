from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None

class BookOut(BookCreate):
    id: str
    user_id: str
    created_at: datetime
