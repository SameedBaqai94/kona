from sqlalchemy import  Column, Integer, String, Text
from pgvector.sqlalchemy import Vector
from  db_config import Base

class AnimeRecord(Base):
    __tablename__ = "anime_catalog"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    genres = Column(String)
    embedding = Column(Vector(384))
