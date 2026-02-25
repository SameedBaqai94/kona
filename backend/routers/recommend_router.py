from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from fastembed import TextEmbedding
from typing import List


from models.anime_records import AnimeRecord
from db_config import SessionLocal,get_db
from schemas.recommend_schema import RecommendResponse,AnimeResult

router = APIRouter(prefix="/recommend", tags=["recommend"])

model = TextEmbedding("BAAI/bge-small-en-v1.5")

@router.get("/", response_model=RecommendResponse)
def recommend(
    q: str = Query(..., description="Natural language query e.g. 'anime similar to Chainsaw Man'"),
    limit: int = Query(10, ge=1, le=50, description="Number of results to return"),
    db: Session = Depends(get_db),
):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Embed the user query using the same model used during ingest
    query_embedding = list(model.embed([q]))[0].tolist()

    # pgvector cosine distance search — closest vectors = most similar anime
    results = (
        db.query(AnimeRecord)
        .order_by(AnimeRecord.embedding.cosine_distance(query_embedding))
        .limit(limit)
        .all()
    )

    if not results:
        raise HTTPException(status_code=404, detail="No results found")

    return RecommendResponse(
        query=q,
        results=[
            AnimeResult(
                id=r.id,
                title=r.title,
                description=r.description,
                genres=r.genres,
                score=r.score if hasattr(r, "score") else None,
            )
            for r in results
        ],
    )