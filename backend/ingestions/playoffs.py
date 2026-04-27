"""Ingest playoff bracket data — rounds, series, and game linkages."""

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
                if season_type != "playoff":
                    continue

                url = f"{BASE_URL}?feed=modulekit&view=brackets&season_id={season_api_id}&{AUTH}"
                response = await client.get(url)
                response.raise_for_status()

                brackets = response.json()["SiteKit"]["Brackets"]
                rounds = brackets.get("rounds", [])

                for round_data in rounds:
                    # Upsert the round, getting back its internal id for use as FK below
                    async with conn.cursor() as cur:
                        await cur.execute(
                            """
                            INSERT INTO playoff_rounds (season_id, round_number, round_name)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (season_id, round_number) DO UPDATE SET
                                round_name = EXCLUDED.round_name
                            RETURNING id
                            """,
                            (season_id, int(round_data["round"]), round_data["round_name"]),
                        )
                        round_id = (await cur.fetchone())[0]

                    for matchup in round_data.get("matchups", []):
                        first_game = matchup["games"][0] if matchup.get("games") else None
                        team1_id = (
                            team_id_map.get(matchup["team1"])
                            or team_id_map.get(first_game["home_team"])
                            if first_game
                            else None
                        )
                        team2_id = (
                            team_id_map.get(matchup["team2"])
                            or team_id_map.get(first_game["visiting_team"])
                            if first_game
                            else None
                        )

                        if team1_id is None or team2_id is None:
                            print(f"Skipping series {matchup['series_letter']} — unknown team")
                            continue

                        feeder1 = (
                            matchup["feeder_series1"]
                            if matchup["feeder_series1"] != "N/A"
                            else None
                        )
                        feeder2 = (
                            matchup["feeder_series2"]
                            if matchup["feeder_series2"] != "N/A"
                            else None
                        )

                        # RETURNING id lets us immediately use the series id to link games below,
                        # without a second query to look it up.
                        async with conn.cursor() as cur:
                            await cur.execute(
                                """
                                INSERT INTO playoff_series (
                                    round_id, season_id, series_letter, series_name,
                                    team1_id, team2_id, team1_wins, team2_wins,
                                    is_active, feeder_series1, feeder_series2
                                )
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (season_id, series_letter) DO UPDATE SET
                                    team1_wins = EXCLUDED.team1_wins,
                                    team2_wins = EXCLUDED.team2_wins,
                                    is_active = EXCLUDED.is_active
                                RETURNING id
                                """,
                                (
                                    round_id,
                                    season_id,
                                    matchup["series_letter"],
                                    matchup["series_name"],
                                    team1_id,
                                    team2_id,
                                    matchup["team1_wins"],
                                    matchup["team2_wins"],
                                    matchup["active"] == "1",
                                    feeder1,
                                    feeder2,
                                ),
                            )
                            series_id = (await cur.fetchone())[0]

                        # Link each game in this series back to the series record
                        for game in matchup.get("games", []):
                            await conn.execute(
                                """
                                UPDATE games SET playoff_series_id = %s
                                WHERE api_id = %s
                                """,
                                (series_id, int(game["game_id"])),
                            )

        await conn.commit()
        print("Playoffs ingestion complete.")


if __name__ == "__main__":
    asyncio.run(run())
