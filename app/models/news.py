from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP
from app.database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    link = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(Text)
    source = Column(String(100))
    publish_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")
