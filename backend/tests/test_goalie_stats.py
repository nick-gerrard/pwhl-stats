def test_goalie_stats_ok(client):
    res = client.get("/stats/goalies/")
    assert res.status_code == 200


def test_goalie_stats_return_list(client):
    res = client.get("/stats/goalies/")
    data = res.json()
    assert isinstance(data, list)


def test_goalie_stats_shape(client):
    res = client.get("/stats/goalies/")
    data = res.json()
    assert len(data) > 0
    for row in data:
        assert row["wins"] >= 0
        assert row["shutouts"] >= 0


def test_goalie_info_not_found(client):
    res = client.get("/stats/goalies/99999")
    assert res.status_code == 404


def test_goalie_info(client):
    res = client.get("/stats/goalies/")
    data = res.json()
    player_id = data[0]["player_id"]
    info_res = client.get(f"/stats/goalies/{player_id}")
    assert info_res.status_code == 200
    info_data = info_res.json()
    assert isinstance(info_data, dict)
    assert "first_name" in info_data
    assert "save_percentage" in info_data
