def test_standings_ok(client):
    res = client.get("/standings/")
    assert res.status_code == 200


def test_standings_return_list(client):
    res = client.get("/standings/")
    data = res.json()
    assert isinstance(data, list)


def test_standings_shap(client):
    res = client.get("/standings")
    data = res.json()
    assert len(data) > 0
    first = data[0]
    assert "team_name" in first
    assert "points" in first
    assert first["points"] >= 0
