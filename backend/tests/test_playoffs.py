def test_bracket_ok(client):
    res = client.get("/playoffs/bracket")
    assert res.status_code == 200


def test_bracket_returns_list(client):
    res = client.get("/playoffs/bracket")
    assert isinstance(res.json(), list)


def test_bracket_shape(client):
    res = client.get("/playoffs/bracket")
    data = res.json()
    assert len(data) > 0

    round_ = data[0]
    assert "round_number" in round_
    assert "round_name" in round_
    assert "series" in round_
    assert isinstance(round_["series"], list)
    assert len(round_["series"]) > 0


def test_bracket_series_shape(client):
    res = client.get("/playoffs/bracket")
    series = res.json()[0]["series"][0]
    assert "series_letter" in series
    assert "team1" in series
    assert "team2" in series
    assert "team1_wins" in series
    assert "team2_wins" in series
    assert "is_active" in series
    assert "name" in series["team1"]
    assert "code" in series["team1"]


def test_bracket_season_id_param(client):
    res = client.get("/playoffs/bracket")
    default_data = res.json()

    # Explicit season_id matching the default should return identical data
    import asyncio
    import psycopg
    from database import get_latest_playoff_season
    from settings import settings

    async def get_id():
        async with await psycopg.AsyncConnection.connect(settings.database_url) as conn:
            return await get_latest_playoff_season(conn)

    season_id = asyncio.run(get_id())
    res2 = client.get(f"/playoffs/bracket?season_id={season_id}")
    assert res2.status_code == 200
    assert res2.json() == default_data


def test_bracket_invalid_season_returns_empty(client):
    res = client.get("/playoffs/bracket?season_id=99999")
    assert res.status_code == 200
    assert res.json() == []
