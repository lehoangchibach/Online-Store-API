def test_login(client):
    response = client.get("/tokens")
    assert response.status_code == 405

    response = client.put("/tokens")
    assert response.status_code == 405

    response = client.delete("/tokens")
    assert response.status_code == 405

    response = client.post("/tokens")
    assert response.status_code == 400

    response = client.post("/tokens", data={
        "email": "testemail@gmail.com"
    })
    assert response.status_code == 400

    response = client.post("/tokens", data={
        "password": "Password"
    })
    assert response.status_code == 400

    response = client.post("/tokens", data={
        "email": "testemail@gmail.com",
        "password": 123
    })
    assert response.status_code == 400

    response = client.post("/tokens", data={
        "email": "testemail@gmail.com",
        "password": "123"
    })
    assert response.status_code == 400

    response = client.post("/tokens", data={
        "email": "testemail@gmail.com",
        "password": "password"
    })
    assert response.status_code == 400

    response = client.post("/tokens", data={
        "email": "testemail@gmail.com",
        "password": "Password"
    })
    assert response.status_code == 400

    response = client.post("/tokens", data={
        "email": "@gmail.com",
        "password": "Password"
    })
    assert response.status_code == 400

    response = client.post("/tokens", data={
        "email": "testemail@.com",
        "password": "Password"
    })
    assert response.status_code == 400

    response = client.post("/tokens", data={
        "email": "lehoangchibach@gmail.com",
        "password": "Bachbon123"
    })
    assert response.status_code == 200

    response_data = response.get_json()
    assert "access_token" in response_data

