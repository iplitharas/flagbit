def test_get_all_flags_endpoint(client, fake_flags_fixture):
    fake_flags_fixture(10)
    response = client.get("/flags")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(response.json(), list)
    assert len(data) == 10
