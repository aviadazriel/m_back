from typing import List
from pydantic import BaseModel
from datetime import date, datetime

class ArticleBase(BaseModel):
    title: str
    description: str
    image_url: str
    published_date: date
    related_articles: List[int]

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
