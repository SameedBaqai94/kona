from pydantic import BaseModel
from typing import List,Optional

class AnimeResult(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    genres: Optional[str] = None
    tags: Optional[str] = None
    score: Optional[float] = None

    class Config:
        from_attributes = True


class RecommendResponse(BaseModel):
    query: str
    results: List[AnimeResult]
