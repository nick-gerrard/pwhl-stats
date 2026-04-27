---
name: Project Overview
description: Architecture, data sources, key files, and current feature state of the PWHL stats site
type: project
---

**Stack:** FastAPI backend, SvelteKit frontend, PostgreSQL (Docker), uv for Python deps.

**Data sources:**
- HockeyTech API (`lscluster.hockeytech.com`) — schedule, standings, player stats, ingested to DB
- Firebase realtime DB (`leaguestat-b9523.firebaseio.com/svf/pwhl`) — live game data (clock, goals, penalties, shots). Has both `publishedclock` (stoppage-only, richer metadata) and `runningclock` (real-time, has `Running` bool). Use publishedclock for period/status metadata, runningclock for clock time.

**Key backend files:**
- `backend/live/firebase.py` — fetches and parses live game data
- `backend/live/poller.py` — SSE polling loop, starts at game time, stops when all games final
- `backend/routers/live.py` — SSE endpoint, sends cached `live_state` immediately on connect
- `backend/routers/standings.py` — calls `compute_eliminations` before returning standings
- `backend/utils.py` — `compute_eliminations()`: adds `clinched` and `eliminated` flags. `PLAYOFF_CUTOFF = 3` (0-based index, 8 teams, top 4 make playoffs — update when expansion arrives)
- `backend/queries/games.py` — includes `get_remaining_games()` used for elimination calc
- `get_data/` — local scripts for raw API inspection, output gitignored

**Features complete (as of 2026-04-23):**
- Standings with logos, clinched (C) and eliminated (E) badges
- Schedule & scores page with live game cards (SSE), ticking clock, expandable goal log
- Player stats tables with player detail/career pages
- Playoff bracket
- Game date timezone fix — dates stored from local API time, not UTC

**Next most valuable feature:** Game detail pages for past games (click a final game → full goal log + box score). Player pages already exist.

**Why:** `PLAYOFF_CUTOFF` controls both clinch and elimination logic — remember to update it when expansion happens.
