def test_players_ok(client):
    res = client.get("/players/")
    assert res.status_code == 200


def test_players_return_list(client):
    res = client.get("/players/")
    data = res.json()
    assert isinstance(data, list)


def test_players_shape(client):
    res = client.get("/players/")
    data = res.json()
    assert len(data) > 0
    for row in data:
        assert row["first_name"]
        assert row["last_name"]
