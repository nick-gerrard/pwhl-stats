def test_teams_ok(client):
    res = client.get("/teams/")
    assert res.status_code == 200


def test_teams_return_list(client):
    res = client.get("/teams/")
    data = res.json()
    assert isinstance(data, list)


def test_teams_shape(client):
    res = client.get("/teams/")
    data = res.json()
    assert len(data) > 0
    for row in data:
        assert row["name"]
        assert row["city"]
