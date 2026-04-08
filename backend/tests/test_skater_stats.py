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
