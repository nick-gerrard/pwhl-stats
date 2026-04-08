"""Ingest season skater statistics."""

import asyncio

import httpx

from ingestions.db import get_all_seasons, get_connection, get_team_id_map

BASE_URL = "https://lscluster.hockeytech.com/feed/index.php"
AUTH = "key=446521baf8c38984&client_code=pwhl"


def strip_jsonp(text: str) -> str:
    text = text.strip()
    if text.startswith("(") and text.endswith(")"):
        return text[1:-1]
    return text


async def run():
    async with get_connection() as conn:
        seasons = await get_all_seasons(conn)
        team_id_map = await get_team_id_map(conn)

        async with conn.cursor() as cur:
            await cur.execute("SELECT api_id, id FROM players")
            rows = await cur.fetchall()
            player_id_map = {str(row[0]): row[1] for row in rows}

        import json

        total = 0
        async with httpx.AsyncClient() as client:
            for season_id, season_api_id, season_type in seasons:
                if season_type != "regular":
                    continue

                url = f"{BASE_URL}?feed=statviewfeed&view=players&season={season_api_id}&team=all&position=skaters&limit=500&{AUTH}"
                response = await client.get(url)
                response.raise_for_status()

                data = json.loads(strip_jsonp(response.text))
                skaters = data[0]["sections"][0]["data"]

                for skater in skaters:
                    row = skater["row"]
                    prop = skater["prop"]

                    player_internal_id = player_id_map.get(row["player_id"])
                    team_internal_id = team_id_map.get(prop["team_code"]["teamLink"])

                    if player_internal_id is None or team_internal_id is None:
                        continue

                    await conn.execute(
                        """
                        INSERT INTO skater_stats (
                            player_id, team_id, season_id,
                            games_played, goals, assists, pim, plus_minus,
                            shots, avg_toi, pp_goals, sh_goals, gw_goals
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (player_id, team_id, season_id) DO UPDATE SET
                            games_played = EXCLUDED.games_played,
                            goals = EXCLUDED.goals,
                            assists = EXCLUDED.assists,
                            pim = EXCLUDED.pim,
                            plus_minus = EXCLUDED.plus_minus,
                            shots = EXCLUDED.shots,
                            avg_toi = EXCLUDED.avg_toi,
                            pp_goals = EXCLUDED.pp_goals,
                            sh_goals = EXCLUDED.sh_goals,
                            gw_goals = EXCLUDED.gw_goals
                        """,
                        (
                            player_internal_id,
                            team_internal_id,
                            season_id,
                            int(row["games_played"]),
                            int(row["goals"]),
                            int(row["assists"]),
                            int(row["penalty_minutes"]),
                            int(row["plus_minus"]),
                            int(row["shots"]),
                            row.get("ice_time_per_game_avg"),
                            int(row["power_play_goals"]),
                            int(row["short_handed_goals"]),
                            0,  # game_winning_goals not in this endpoint
                        ),
                    )
                    total += 1

        await conn.commit()
        print(f"Skater stats ingestion complete — {total} skaters processed.")


if __name__ == "__main__":
    asyncio.run(run())
