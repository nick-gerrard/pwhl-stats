import asyncio

import psycopg

from settings import settings


async def get_latest_playoff_season_id() -> int | None:
    """Gets the most recent playoff season id regardless of staleness — for test use only."""
    async with await psycopg.AsyncConnection.connect(settings.database_url) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT id FROM seasons WHERE season_type = 'playoff' ORDER BY id DESC LIMIT 1"
            )
            row = await cur.fetchone()
            return row[0] if row else None


def test_bracket_ok(client):
    res = client.get("/playoffs/bracket")
    assert res.status_code == 200


def test_bracket_returns_list(client):
    res = client.get("/playoffs/bracket")
    assert isinstance(res.json(), list)


# def test_bracket_default_empty_when_no_current_playoffs(client):
#     # Default endpoint returns [] when no playoffs are active for the current season.
#     # In CI (seeded with current real data) there are no 2025-26 playoffs yet.
#     res = client.get("/playoffs/bracket")
#     assert res.json() == []


def test_bracket_explicit_season_returns_data(client):
    season_id = asyncio.run(get_latest_playoff_season_id())
    assert season_id is not None, "No playoff season in test DB"

    res = client.get(f"/playoffs/bracket?season_id={season_id}")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0


def test_bracket_shape(client):
    season_id = asyncio.run(get_latest_playoff_season_id())
    data = client.get(f"/playoffs/bracket?season_id={season_id}").json()

    round_ = data[0]
    assert "round_number" in round_
    assert "round_name" in round_
    assert "series" in round_
    assert isinstance(round_["series"], list)
    assert len(round_["series"]) > 0


def test_bracket_series_shape(client):
    season_id = asyncio.run(get_latest_playoff_season_id())
    series = client.get(f"/playoffs/bracket?season_id={season_id}").json()[0]["series"][0]

    assert "series_letter" in series
    assert "team1" in series
    assert "team2" in series
    assert "team1_wins" in series
    assert "team2_wins" in series
    assert "is_active" in series
    assert "name" in series["team1"]
    assert "code" in series["team1"]


def test_bracket_invalid_season_returns_empty(client):
    res = client.get("/playoffs/bracket?season_id=99999")
    assert res.status_code == 200
    assert res.json() == []
