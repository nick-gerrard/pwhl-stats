# PWHL Stats

An unofficial stats tracker for the [Professional Women's Hockey League](https://www.thepwhl.com), built as a personal project. Data is ingested from the PWHL's public API and served through a custom REST API with a SvelteKit frontend.

Live at **[pwhl.nickgerrard.dev](https://pwhl.nickgerrard.dev)**

---

## Features

- **Standings** — full league standings with regulation wins, OT/SO splits, and points
- **Schedule & Scores** — game results and upcoming schedule with team filters
- **Live Game Updates** — real-time score, period, clock, power play indicators, and SOG via Server-Sent Events
- **Skater & Goalie Stats** — sortable, filterable stat tables with per-player detail modals
- **Playoff Bracket** — live bracket with series scores and matchup tracking
- **Season Selector** — toggle between seasons on any page
- **Responsive Design** — tailored layouts for mobile and desktop throughout

---

## Tech Stack

**Backend**
- Python 3.13 / [FastAPI](https://fastapi.tiangolo.com/)
- PostgreSQL 16 with [psycopg3](https://www.psycopg.org/psycopg3/) (async)
- [Alembic](https://alembic.sqlalchemy.org/) for migrations
- [uv](https://docs.astral.sh/uv/) for dependency management
- [APScheduler](https://apscheduler.readthedocs.io/) for scheduled ingestion and live polling

**Frontend**
- [SvelteKit](https://kit.svelte.dev/) (Svelte 5)
- [Tailwind CSS v4](https://tailwindcss.com/)
- TypeScript

**Infrastructure**
- Linode Nanode (1 GB) — nginx reverse proxy + systemd service
- GitHub Actions CI/CD — tests on every PR, deploy to Linode on merge to main

---

## Project Structure

```
pwhl-stats/
├── backend/
│   ├── alembic/          # Database migrations
│   ├── ingestions/       # PWHL API ingestion scripts (run daily via cron)
│   ├── live/             # Firebase polling + SSE broadcasting for live games
│   ├── queries/          # Async SQL query functions
│   ├── routers/          # FastAPI route handlers
│   ├── main.py           # App entrypoint, lifespan, scheduler setup
│   ├── models.py
│   ├── schemas.py        # Pydantic response models
│   └── settings.py       # Environment config
└── frontend/
    └── src/
        ├── lib/
        │   ├── components/   # Nav, SeasonSelector, Logo, Pagination
        │   └── types.ts
        └── routes/           # SvelteKit file-based routes
            ├── +page.svelte          # Standings
            ├── games/
            ├── stats/skaters/
            ├── stats/goalies/
            ├── playoffs/
            └── about/
```

---

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/standings` | League standings |
| GET | `/games` | Schedule and scores |
| GET | `/stats/skaters` | Skater stats |
| GET | `/stats/skaters/{player_id}` | Skater detail |
| GET | `/stats/goalies` | Goalie stats |
| GET | `/stats/goalies/{player_id}` | Goalie detail |
| GET | `/playoffs` | Playoff bracket |
| GET | `/live` | SSE stream of live game data |
| GET | `/teams` | All teams |
| GET | `/seasons` | All seasons |
| POST | `/admin/ingest` | Trigger data ingestion (requires `X-Admin-Token` header) |

Interactive docs available at `/docs` when running locally.

---

## Getting Started

### Prerequisites

- Docker (for PostgreSQL)
- Python 3.13+
- Node 22+

### 1. Environment

Root `.env`:
```
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=pwhl

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/pwhl
ADMIN_TOKEN=localdev
```

`frontend/.env`:
```
PUBLIC_API_URL=http://localhost:8000
```

### 2. Database

```bash
docker compose up -d
cd backend && uv run alembic upgrade head
```

### 3. Ingest data

```bash
cd backend
uv run python -m ingestions.run
```

### 4. Backend

```bash
cd backend
uv run uvicorn main:app --reload
```

API at `http://localhost:8000` · Docs at `http://localhost:8000/docs`

### 5. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend at `http://localhost:5173`

---

## Roadmap

- [ ] Player comparison — side-by-side stat view between two players
- [ ] Historical season stats — season-over-season progression per player
- [ ] Pace stats — goals/60, shots/60, normalised across ice time
- [ ] Game detail page — box score using the existing `game_periods` table
- [ ] Team detail page — roster, record, and stat leaders
- [ ] Game log — per-player game-by-game stat breakdown
- [ ] Stat leaders dashboard — top-5-per-category overview on the home page
