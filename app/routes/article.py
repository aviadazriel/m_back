from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse
from app.crud.article import get_articles, get_article, create_article, update_article, delete_article
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ArticleResponse])
def read_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_articles(db, skip=skip, limit=limit)

@router.post("/", response_model=ArticleResponse)
def create_new_article(article: ArticleCreate, db: Session = Depends(get_db)):
    return create_article(db, article)
