def test_skater_stats_ok(client):
    res = client.get("/stats/skaters/")
    assert res.status_code == 200


def test_skater_stats_return_list(client):
    res = client.get("/stats/skaters/")
    data = res.json()
    assert isinstance(data, list)


def test_skater_stats_shape(client):
    res = client.get("/stats/skaters/")
    data = res.json()
    assert len(data) > 0
    for row in data:
        assert row["goals"] >= 0


def test_player_info_not_found(client):
    res = client.get("/stats/skaters/99999")
    assert res.status_code == 404


def test_player_info(client):
    res = client.get("/stats/skaters/")
    data = res.json()
    player_id = data[0]["player_id"]
    info_res = client.get(f"/stats/skaters/{player_id}")
    assert info_res.status_code == 200
    info_data = info_res.json()
    assert len(info_data) > 0
    assert isinstance(info_data, dict)
