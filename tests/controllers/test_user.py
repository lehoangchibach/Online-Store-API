def test_create_user(client):
    response = client.get("/users")
    assert response.status_code == 405

    response = client.put("/users")
    assert response.status_code == 405

    response = client.delete("/users")
    assert response.status_code == 405

    response = client.post("/users")
    assert response.status_code == 400

    response = client.post("/users", data={
        "email": "testemail@gmail.com"
    })
    assert response.status_code == 400

    response = client.post("/users", data={
        "password": "Password"
    })
    assert response.status_code == 400

    response = client.post("/users", data={
        "email": "testemail@gmail.com",
        "password": 123
    })
    assert response.status_code == 400

    response = client.post("/users", data={
        "email": "testemail@gmail.com",
        "password": "123"
    })
    assert response.status_code == 400

    response = client.post("/users", data={
        "email": "testemail@gmail.com",
        "password": "password"
    })
    assert response.status_code == 400

    response = client.post("/users", data={
        "email": "testemail@gmail.com",
        "password": "Password"
    })
    assert response.status_code == 400

    response = client.post("/users", data={
        "email": "@gmail.com",
        "password": "Password"
    })
    assert response.status_code == 400

    response = client.post("/users", data={
        "email": "testemail@.com",
        "password": "Password"
    })
    assert response.status_code == 400

    response = client.post("/users", data={
        "email": "testemail@gmail.com",
        "password": "Password123"
    })
    assert response.status_code == 200

    response_data = response.get_json()
    assert "access_token" in response_data
