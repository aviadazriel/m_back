from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from app.database import Base
from sqlalchemy import Column, Integer, String, Text, Date, ARRAY, TIMESTAMP


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(Text, nullable=False)
    published_date = Column(Date, nullable=False)
    related_articles = Column(ARRAY(Integer))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))