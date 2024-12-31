from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import date, datetime

class NewsBase(BaseModel):
    title: str
    link: HttpUrl
    description: str
    image_url: Optional[HttpUrl]
    source: Optional[str]
    publish_date: date

class NewsCreate(NewsBase):
    pass

class NewsUpdate(NewsBase):
    pass

class NewsResponse(NewsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
