# kona
# Kona

Anime recommendation engine that takes natural language input and returns results based on semantic similarity — think "anime that feels like Chainsaw Man" instead of filtering by genre.

## How it works

Anime metadata (title, genres, tags, synopsis) from AniList is vectorized and stored in a pgvector Postgres database. When you search, your query gets embedded with the same model and the closest vectors are returned.

## Stack

- **Frontend** — React + Vite + TypeScript
- **Backend** — FastAPI
- **Database** — PostgreSQL + pgvector
- **Embeddings** — fastembed (BAAI/bge-small-en-v1.5)
- **Data source** — AniList GraphQL API

## Running locally

**Prerequisites** — Docker, Python 3.10+, Node 18+

1. Start the database
```bash
docker compose up -d
```

2. Seed anime data
```bash
cd backend
pip install -r requirements.txt
python seed.py
```

3. Start the backend
```bash
uvicorn main:app --reload
```

4. Start the frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`, backend on `http://localhost:8000`.

## Project structure

```
Kona/
├── backend/
│   ├── main.py
│   ├── db_config.py
│   ├── seed.py
│   ├── models/
│   ├── routers/
│   └── schemas/
└── frontend/
    └── src/
        ├── pages/
        └── components/
```

## Environment variables

Backend reads `DATABASE_URL` from environment, falls back to local Postgres if not set.

Frontend reads `VITE_API_URL` from `.env` for the backend URL.
