from http import HTTPStatus


def test_get_all_flags_endpoint(client, fake_flags_fixture):
    """
    Given some existing `Flags` in the `database/system`
    When I call the `/flags` endpoint,
    Then I'm expecting a list of `Flags` to be returned,
         and the response status code to be `200`
    """
    # Given
    fake_flags_fixture(10)

    # When
    response = client.get("/flags")

    # Then
    assert response.status_code == HTTPStatus.OK, "Expected status code 200"
    data = response.json()
    assert isinstance(data, list), "Expected response to be a list"
    assert len(data) == 10, "Expected 10 flags in the response"


def test_get_flag_by_id_endpoint(client, fake_flags_fixture):
    """
    Given an existing `Flag` in the `database/system`
    When I call the `/flags/{flag_id}` endpoint,
    Then I'm expecting the `Flag` to be returned,
         and the response status code to be `200`
    """
    # Given
    fake_flags_fixture(1)
    response_all = client.get("/flags")
    flag_id = response_all.json()[0]["id"]

    # When
    response = client.get(f"/flags/{flag_id}")

    # Then
    assert response.status_code == HTTPStatus.OK, "Expected status code 200"
    expected_response = response.json()
    assert expected_response["id"] == flag_id, "Flag ID should match"
    assert "name" in expected_response, "Response should contain flag name"
    assert "value" in expected_response, "Response should contain flag value"
    assert "desc" in expected_response, "Response should contain flag description"


def test_post_new_flag_endpoint(client):
    """
    Given a new `Flag` data
    When I call the `/flags` endpoint with a POST request,
    Then I'm expecting the flag to be created,
         and the response status code to be `201`
    """
    # Given
    new_flag_data = {
        "name": "new_feature",
        "value": True,
        "desc": "A new feature flag for testing",
    }

    # When
    response = client.post("/flags", json=new_flag_data)

    # Then
    assert response.status_code == HTTPStatus.CREATED, "Expected status code 201"
    expected_response = response.json()
    assert expected_response["name"] == new_flag_data["name"], "Flag name should match"
    assert expected_response["value"] == new_flag_data["value"], (
        "Flag value should match"
    )
    assert expected_response["desc"] == new_flag_data["desc"], (
        "Flag description should match"
    )
    assert "id" in expected_response, "Response should contain flag ID"
