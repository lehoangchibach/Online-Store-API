def test_create_user_invalid_endpoints(client, session):
    # assert not support endpoint
    response = client.get("/users")
    assert response.status_code == 405

    response = client.put("/users")
    assert response.status_code == 405

    response = client.delete("/users")
    assert response.status_code == 405


def test_create_user_successfully(client, session):
    # assert successful request
    response = client.post("/users", json={
        "email": "test_create_user_successfully@gmail.com",
        "password": "Password123"
    })
    assert response.status_code == 200
    response_json = response.get_json()
    assert "access_token" in response_json


def test_create_user_request_body_not_json(client, session):
    # assert request body not json
    response = client.post("/users")
    assert response.status_code == 400


def test_create_user_invalid_password(client, session):
    json = {
        "email": "test_user@gmail.com"
    }

    response = client.post("/users", json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    json["password"] = "Password"
    response = client.post("/users", json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    json["password"] = "password123"
    response = client.post("/users", json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    json["password"] = "Pd123"
    response = client.post("/users", json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    json["password"] = "       "
    response = client.post("/users", json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]


def test_create_user_invalid_email(client, session):
    # assert request with invalid email
    json = {
        "password": "Password"
    }

    response = client.post("/users", json=json)
    assert response.status_code == 400
    assert "email" in response.get_json()["error_data"]

    json["email"] = "@gmail.com"
    response = client.post("/users", json=json)
    assert response.status_code == 400
    assert "email" in response.get_json()["error_data"]

    json["email"] = "bachle@.com"
    response = client.post("/users", json=json)
    assert response.status_code == 400
    assert "email" in response.get_json()["error_data"]

    json["email"] = "bachle@gmail."
    response = client.post("/users", json=json)
    assert response.status_code == 400
    assert "email" in response.get_json()["error_data"]

    json["email"] = "  sdf "
    response = client.post("/users", json=json)
    assert response.status_code == 400
    assert "email" in response.get_json()["error_data"]

