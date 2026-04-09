"""Ingest game schedule and results."""

import asyncio
from datetime import datetime, timezone

import httpx

from ingestions.db import get_all_seasons, get_connection, get_team_id_map

BASE_URL = "https://lscluster.hockeytech.com/feed/index.php"
AUTH = "key=446521baf8c38984&client_code=pwhl"


def parse_status(game: dict) -> str:
    if game.get("final") == "1":
        return "final"
    if game.get("started") == "1":
        return "in_progress"
    return "scheduled"


async def run():
    async with get_connection() as conn:
        seasons = await get_all_seasons(conn)
        team_id_map = await get_team_id_map(conn)
        total = 0

        async with httpx.AsyncClient() as client:
            for season_id, season_api_id, _season_type in seasons:
                url = f"{BASE_URL}?feed=modulekit&view=schedule&season_id={season_api_id}&{AUTH}"
                response = await client.get(url)
                response.raise_for_status()
                games = response.json()["SiteKit"]["Schedule"]

                for game in games:
                    home_team_id = team_id_map.get(game["home_team"])
                    visiting_team_id = team_id_map.get(game["visiting_team"])

                    if home_team_id is None or visiting_team_id is None:
                        print(f"Skipping game {game['game_id']} — unknown team")
                        continue

                    status = parse_status(game)
                    home_score = int(game["home_goal_count"]) if status == "final" else None
                    away_score = int(game["visiting_goal_count"]) if status == "final" else None

                    start_time = datetime.fromisoformat(game["GameDateISO8601"])
                    date_played = start_time.astimezone(timezone.utc).date()

                    await conn.execute(
                        """
                        INSERT INTO games (
                            api_id, season_id, home_team_id, visiting_team_id,
                            home_score, away_score, date, status, venue, start_time
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (api_id) DO UPDATE SET
                            home_score = EXCLUDED.home_score,
                            away_score = EXCLUDED.away_score,
                            status = EXCLUDED.status,
                            venue = EXCLUDED.venue,
                            start_time = EXCLUDED.start_time
                        """,
                        (
                            game["game_id"],
                            season_id,
                            home_team_id,
                            visiting_team_id,
                            home_score,
                            away_score,
                            date_played,
                            status,
                            game.get("venue_name"),
                            start_time,
                        ),
                    )
                    total += 1

        await conn.commit()
        print(f"Games ingestion complete — {total} games processed.")


if __name__ == "__main__":
    asyncio.run(run())
