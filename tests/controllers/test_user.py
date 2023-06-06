def test_create_user(client, session):
    # assert not support endpoint
    response = client.get("/users")
    assert response.status_code == 405

    response = client.put("/users")
    assert response.status_code == 405

    response = client.delete("/users")
    assert response.status_code == 405

    # assert request with no body
    response = client.post("/users")
    assert response.status_code == 400
    response_json = response.get_json()
    assert "email" in response_json["error_data"]
    assert "password" in response_json["error_data"]

    # assert request with invalid email and password
    response = client.post("/users", json={
        "email": "test_user@gmail.com"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    response = client.post("/users", json={
        "password": "Password"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "email" in response_json["error_data"]
    assert "password" in response_json["error_data"]

    response = client.post("/users", json={
        "email": "test_user@gmail.com",
        "password": 123
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    response = client.post("/users", json={
        "email": "test_user@gmail.com",
        "password": "123"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    response = client.post("/users", json={
        "email": "test_user@gmail.com",
        "password": "password"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    response = client.post("/users", json={
        "email": "test_user@gmail.com",
        "password": "Password"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    response = client.post("/users", json={
        "email": "@gmail.com",
        "password": "Password"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "email" in response_json["error_data"]
    assert "password" in response_json["error_data"]

    response = client.post("/users", json={
        "email": "test_user@.com",
        "password": "Password123"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "email" in response_json["error_data"]

    # assert successful request
    response = client.post("/users", json={
        "email": "test_user@gmail.com",
        "password": "Password123"
    })
    assert response.status_code == 200
    response_json = response.get_json()
    assert "access_token" in response_json

    # assert duplicate email
    response = client.post("/users", json={
        "email": "test_user@gmail.com",
        "password": "Password123"
    })
    assert response.status_code == 400
