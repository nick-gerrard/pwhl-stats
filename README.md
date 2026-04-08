# PWHL Stats

A stats tracker for the Professional Women's Hockey League, built as a personal project and portfolio piece. Data is ingested from the PWHL's public API and served through a custom REST API with a SvelteKit frontend.

## Tech Stack

**Backend**
- Python 3.13 / [FastAPI](https://fastapi.tiangolo.com/)
- PostgreSQL with [psycopg3](https://www.psycopg.org/psycopg3/)
- [Alembic](https://alembic.sqlalchemy.org/) for migrations
- [uv](https://docs.astral.sh/uv/) for dependency management

**Frontend**
- [SvelteKit](https://kit.svelte.dev/) (Svelte 5)
- [Tailwind CSS v4](https://tailwindcss.com/)
- TypeScript

## Getting Started

### Prerequisites
- Python 3.13+
- Node 20+
- PostgreSQL 16

### 1. Environment

Create a `.env` file in the project root:

```
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=pwhl

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/pwhl
```

Create a `.env` in `frontend/`:

```
PUBLIC_API_URL=http://localhost:8000
```

### 2. Database

Start PostgreSQL (or use the provided docker-compose):

```bash
docker compose up -d
```

Run migrations:

```bash
cd backend
uv run alembic upgrade head
```

### 3. Ingest data

```bash
cd backend
uv run python ingestions/run.py
```

### 4. Run the backend

```bash
cd backend
uv run uvicorn main:app --reload
```

API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### 5. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:5173`.

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/standings` | Current season standings |
| GET | `/games` | All games for current season |
| GET | `/stats/skaters` | Skater stats for current season |
| GET | `/stats/skaters/{player_id}` | Detailed stats for a skater |
| GET | `/stats/goalies` | Goalie stats for current season |
| GET | `/stats/goalies/{player_id}` | Detailed stats for a goalie |
| GET | `/teams` | All teams |
| GET | `/players` | All players |

## Project Structure

```
pwhl-stats/
├── backend/
│   ├── alembic/          # Database migrations
│   ├── ingestions/       # PWHL API data ingestion scripts
│   ├── queries/          # SQL query functions
│   ├── routers/          # FastAPI route handlers
│   ├── main.py
│   ├── models.py
│   ├── schemas.py        # Pydantic response models
│   └── settings.py
└── frontend/
    └── src/
        ├── lib/
        │   ├── components/
        │   └── types.ts
        └── routes/       # SvelteKit file-based routes
```

## Roadmap

### In progress
- [ ] CI/CD with GitHub Actions (lint, typecheck, deploy to Linode)
- [ ] Integration tests for API routes

### Planned
- [ ] **Player comparison tool** — side-by-side stat comparison between two players
- [ ] **Historical season stats** — season-over-season progression per player, leveraging the existing seasons table
- [ ] **Pace stats** — goals/60, shots/60, normalised across ice time
- [ ] **Stat leaders dashboard** — replace the home page with a proper top-5-per-category overview
- [ ] **Real-time game data** — live score ingestion and in-game stats
- [ ] **Game detail page** — box score view using the existing game_periods table
- [ ] **Team detail page** — roster, record, and stat leaders per team
- [ ] **Game log** — per-player game-by-game stat breakdown
- [ ] **404 handling** — proper error pages for missing players/games

### Deployment
- [ ] Linode Nanode (1GB) with Caddy reverse proxy
- [ ] systemd service for the API
- [ ] Nightly cron for data ingestion
