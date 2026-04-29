# PWHL Stats

An unofficial stats tracker for the [Professional Women's Hockey League](https://www.thepwhl.com), built as a personal project. Data is ingested from the PWHL's public API and served through a custom REST API with a SvelteKit frontend.

Live at **[pwhl.nickgerrard.dev](https://pwhl.nickgerrard.dev)**

---

## Features

- **Standings** — full league standings with regulation wins, OT/SO splits, points, and clinch/elimination indicators
- **Schedule & Scores** — game results and upcoming schedule with team filters
- **Live Game Updates** — real-time score, period, clock, power play indicators, shots on goal, and goal log via Server-Sent Events
- **Skater Stats** — sortable, filterable stat tables; click any player to open a side drawer with season stats, shooting stats, profile, and photo
- **Goalie Stats** — sortable, filterable stat tables with the same side drawer treatment
- **Player & Goalie Career Pages** — full season-by-season career stats with career totals
- **Stat Leaders** — top-5 leaderboard cards for goals, assists, points, and save percentage
- **Head-to-Head Compare** — side-by-side career stat comparison for two skaters or two goalies
- **Playoff Bracket** — live bracket with series scores, team logos, and TBD placeholders
- **Season Selector** — toggle between regular seasons on any stats page
- **PWA Support** — installable via Safari → Share → Add to Home Screen
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
- GitHub Actions CI/CD — deploy to Linode on merge to main

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
│   ├── schemas.py        # Pydantic response models
│   └── settings.py       # Environment config
└── frontend/
    └── src/
        ├── lib/
        │   ├── components/   # Nav, SeasonSelector, Logo, Pagination
        │   └── types.ts
        └── routes/
            ├── +page.svelte                      # Standings
            ├── games/                            # Schedule & scores
            ├── playoffs/                         # Playoff bracket
            ├── about/
            └── stats/
                ├── skaters/                      # Skater stats table
                ├── skaters/[player_id]/          # Skater career page
                ├── goalies/                      # Goalie stats table
                ├── goalies/[player_id]/          # Goalie career page
                ├── leaders/                      # Stat leaders
                └── compare/                      # Head-to-head comparison
```

---

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/standings` | League standings |
| GET | `/games` | Schedule and scores |
| GET | `/stats/skaters` | Skater stats (current season) |
| GET | `/stats/skaters/all` | All skaters as `{player_id, name}` (for search) |
| GET | `/stats/skaters/leaderboard` | Top skaters by stat category |
| GET | `/stats/skaters/{player_id}` | Skater season detail |
| GET | `/stats/skaters/{player_id}/career` | Skater career history |
| GET | `/stats/goalies` | Goalie stats (current season) |
| GET | `/stats/goalies/all` | All goalies as `{player_id, name}` (for search) |
| GET | `/stats/goalies/leaderboard` | Top goalies by stat category |
| GET | `/stats/goalies/{player_id}` | Goalie season detail |
| GET | `/stats/goalies/{player_id}/career` | Goalie career history |
| GET | `/playoffs/bracket` | Playoff bracket |
| GET | `/live` | SSE stream of live game data |
| GET | `/teams` | All teams |
| GET | `/seasons` | All seasons |
| GET | `/players` | All players |
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

- [ ] Game detail page — score summary, venue, attendance, and goal log for completed games
- [ ] Team detail page — roster, record, and stat leaders per team
- [ ] Game log — per-player game-by-game stat breakdown
- [ ] Pace stats — goals/60, shots/60, normalised across ice time
