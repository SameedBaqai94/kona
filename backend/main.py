from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.recommend_router import router as recommend_router
from db_config import init_db

app = FastAPI(
    title="Anime Recommender",
    description="Natural language anime recommendations powered by AniList + pgvector",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-railway-frontend-url.up.railway.app",  # add this later when frontend is deployed
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(recommend_router)


@app.get("/")
def root():
    return {"message": "Anime Recommender API is running. Hit /recommend/?q=your+query"}