def test_login(client, session):
    # assert unsuppored endpoint
    response = client.get("/tokens")
    assert response.status_code == 405

    response = client.put("/tokens")
    assert response.status_code == 405

    response = client.delete("/tokens")
    assert response.status_code == 405

    # assert request with no body
    response = client.post("/tokens")
    assert response.status_code == 400
    response_json = response.get_json()

    # assert request with invalid email and password
    response = client.post("/tokens", json={
        "email": "test_token@gmail.com"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    response = client.post("/tokens", json={
        "password": "Password"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "email" in response_json["error_data"]
    assert "password" in response_json["error_data"]

    response = client.post("/tokens", json={
        "email": "test_token@gmail.com",
        "password": 123
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    response = client.post("/tokens", json={
        "email": "test_token@gmail.com",
        "password": "123"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    response = client.post("/tokens", json={
        "email": "test_token@gmail.com",
        "password": "password"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    response = client.post("/tokens", json={
        "email": "test_token@gmail.com",
        "password": "Password"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]

    response = client.post("/tokens", json={
        "email": "@gmail.com",
        "password": "Password"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "email" in response_json["error_data"]
    assert "password" in response_json["error_data"]

    response = client.post("/tokens", json={
        "email": "test_token@.com",
        "password": "Password"
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "email" in response_json["error_data"]
    assert "password" in response_json["error_data"]

    # CREATE USER
    response = client.post("/users", json={
        "email": "test_token@gmail.com",
        "password": "Password123"
    })
    assert response.status_code == 200

    # assert successful request
    response = client.post("/tokens", json={
        "email": "test_token@gmail.com",
        "password": "Password123"
    })
    assert response.status_code == 200
    response_json = response.get_json()
    assert "access_token" in response_json
