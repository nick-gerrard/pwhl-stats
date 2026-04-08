def test_games_ok(client):
    res = client.get("/games/")
    assert res.status_code == 200


def test_games_return_list(client):
    res = client.get("/games/")
    data = res.json()
    assert isinstance(data, list)


def test_games_shape(client):
    res = client.get("/games/")
    data = res.json()
    assert len(data) > 0
    for row in data:
        assert row["home_team"] and row["visiting_team"]
