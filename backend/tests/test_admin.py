def test_admin_403(client):
    res = client.post("/admin/ingest/", headers={"X-Admin-Token": "wrongtoken"})
    assert res.status_code == 403
