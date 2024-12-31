from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.news import NewsCreate, NewsUpdate, NewsResponse
from app.crud.news import get_news, get_all_news, create_news, update_news, delete_news

router = APIRouter()

@router.get("/", response_model=List[NewsResponse])
def read_all_news(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_news(db, skip, limit)

@router.get("/{news_id}", response_model=NewsResponse)
def read_news(news_id: int, db: Session = Depends(get_db)):
    news = get_news(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.post("/", response_model=NewsResponse)
def create_new_news(news_data: NewsCreate, db: Session = Depends(get_db)):
    return create_news(db, news_data)

@router.put("/{news_id}", response_model=NewsResponse)
def update_existing_news(news_id: int, news_data: NewsUpdate, db: Session = Depends(get_db)):
    news = update_news(db, news_id, news_data)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.delete("/{news_id}")
def delete_existing_news(news_id: int, db: Session = Depends(get_db)):
    news = delete_news(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return {"message": f"News with ID {news_id} has been deleted"}
