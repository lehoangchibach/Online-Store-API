def test_get_categories(client):
    response = client.get("/users", data={
        "email": "testemail@gmail.com"
    })
    assert response.status_code == 400

    response = client.post("/users", data={
        "email": "testemail@gmail.com"
    })
    assert response.status_code == 400
