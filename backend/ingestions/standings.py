"""Ingest league standings."""

import asyncio

import httpx

from ingestions.db import get_all_seasons, get_connection, get_team_id_map

BASE_URL = "https://lscluster.hockeytech.com/feed/index.php"
AUTH = "key=446521baf8c38984&client_code=pwhl"


async def run():
    async with get_connection() as conn:
        seasons = await get_all_seasons(conn)
        team_id_map = await get_team_id_map(conn)

        async with httpx.AsyncClient() as client:
            for season_id, season_api_id, season_type in seasons:
                if season_type != "regular":
                    continue

                url = f"{BASE_URL}?feed=modulekit&view=statviewtype&stat=conference&type=standings&season_id={season_api_id}&{AUTH}"
                response = await client.get(url)
                response.raise_for_status()
                entries = response.json()["SiteKit"]["Statviewtype"]

                for entry in entries:
                    # Skip header rows — they have no team_id
                    if "team_id" not in entry:
                        continue

                    team_id = team_id_map.get(entry["team_id"])
                    if team_id is None:
                        print(f"Skipping unknown team_id {entry['team_id']}")
                        continue

                    await conn.execute(
                        """
                        INSERT INTO standings (
                            team_id, season_id, wins, losses,
                            ot_wins, ot_losses, shootout_wins, shootout_losses,
                            games_played, points
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (team_id, season_id) DO UPDATE SET
                            wins = EXCLUDED.wins,
                            losses = EXCLUDED.losses,
                            ot_wins = EXCLUDED.ot_wins,
                            ot_losses = EXCLUDED.ot_losses,
                            shootout_wins = EXCLUDED.shootout_wins,
                            shootout_losses = EXCLUDED.shootout_losses,
                            games_played = EXCLUDED.games_played,
                            points = EXCLUDED.points
                        """,
                        (
                            team_id,
                            season_id,
                            int(entry["wins"]),
                            int(entry["reg_losses"]),
                            int(entry["ot_wins"]),
                            int(entry["ot_losses"]),
                            int(entry["shootout_wins"]),
                            int(entry["shootout_losses"]),
                            int(entry["games_played"]),
                            int(entry["points"]),
                        ),
                    )

        await conn.commit()
        print("Standings ingestion complete.")


if __name__ == "__main__":
    asyncio.run(run())
