"""Ingest season goalie statistics."""

import asyncio
import json

import httpx

from ingestions.db import get_connection, get_current_season, get_team_id_map

BASE_URL = "https://lscluster.hockeytech.com/feed/index.php"
AUTH = "key=446521baf8c38984&client_code=pwhl"


def strip_jsonp(text: str) -> str:
    text = text.strip()
    if text.startswith("(") and text.endswith(")"):
        return text[1:-1]
    return text


def parse_minutes(minutes_str: str) -> int:
    """Convert 'MM:SS' string to total minutes (integer)."""
    if not minutes_str:
        return 0
    try:
        parts = minutes_str.split(":")
        return int(parts[0])
    except (ValueError, IndexError):
        return 0


async def run():
    async with get_connection() as conn:
        season_id, season_api_id = await get_current_season(conn)
        team_id_map = await get_team_id_map(conn)

        async with conn.cursor() as cur:
            await cur.execute("SELECT api_id, id FROM players")
            rows = await cur.fetchall()
            player_id_map = {str(row[0]): row[1] for row in rows}

        url = f"{BASE_URL}?feed=statviewfeed&view=players&season={season_api_id}&team=all&position=goalies&limit=500&{AUTH}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        data = json.loads(strip_jsonp(response.text))
        goalies = data[0]["sections"][0]["data"]

        for goalie in goalies:
            row = goalie["row"]
            prop = goalie["prop"]

            player_internal_id = player_id_map.get(row["player_id"])
            team_internal_id = team_id_map.get(prop["team_code"]["teamLink"])

            if player_internal_id is None or team_internal_id is None:
                continue

            from decimal import Decimal

            save_pct = Decimal(row["save_percentage"]) if row.get("save_percentage") else None
            gaa = (
                Decimal(row["goals_against_average"]) if row.get("goals_against_average") else None
            )

            await conn.execute(
                """
                INSERT INTO goalie_stats (
                    player_id, team_id, season_id,
                    games_played, wins, losses, ot_losses,
                    shutouts, shots_against, goals_against,
                    save_percentage, gaa, minutes_played
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (player_id, team_id, season_id) DO UPDATE SET
                    games_played = EXCLUDED.games_played,
                    wins = EXCLUDED.wins,
                    losses = EXCLUDED.losses,
                    ot_losses = EXCLUDED.ot_losses,
                    shutouts = EXCLUDED.shutouts,
                    shots_against = EXCLUDED.shots_against,
                    goals_against = EXCLUDED.goals_against,
                    save_percentage = EXCLUDED.save_percentage,
                    gaa = EXCLUDED.gaa,
                    minutes_played = EXCLUDED.minutes_played
                """,
                (
                    player_internal_id,
                    team_internal_id,
                    season_id,
                    int(row["games_played"]),
                    int(row["wins"]),
                    int(row["losses"]),
                    int(row["ot_losses"]),
                    int(row["shutouts"]),
                    int(row["shots"]),
                    int(row["goals_against"]),
                    save_pct,
                    gaa,
                    parse_minutes(row.get("minutes_played", "")),
                ),
            )

        await conn.commit()
        print(f"Goalie stats ingestion complete — {len(goalies)} goalies processed.")


if __name__ == "__main__":
    asyncio.run(run())
