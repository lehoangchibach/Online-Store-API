import uuid


def test_get_items(client):
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
                    ".eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTkzNj" \
                    "k1OCwianRpIjoiMmNiM2Q3ZDMtNzA1NS00YzBjL" \
                    "WFhZGEtYmE2ZmVkYzU2M2M5IiwidHlwZSI6ImFj" \
                    "Y2VzcyIsInN1YiI6MjUsIm5iZiI6MTY4NTkzNjk" \
                    "1OCwiZXhwIjoxNjg1OTM3ODU4fQ.6JtqIH_4GoW" \
                    "T6LGauhQiZZUdpTDkfVOHjAt0Np3p73c"
    response = client.get("/items", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert response.status_code == 401

    token = client.post("/users", json={
        "email": "test_item@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    random_name = uuid.uuid4()
    response = client.post("/categories", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": f"test - {random_name}"
    })
    assert response.status_code == 200
    response_json = response.get_json()
    assert "id" in response_json

    category_id = response_json["id"]

    response = client.get("/items", query_string={
        "category_id": category_id
    })
    response_json = response.get_json()
    assert response.status_code == 200
    assert "items" in response_json
    assert "items_per_page" in response_json
    assert "page" in response_json
    assert "total_items" in response_json

    response = client.get("/items", query_string={
        "category_id": "12a",
        "page_number": "ab",
        "page_size": "ab"
    })
    response_json = response.get_json()
    assert response.status_code == 400
    assert "category_id" in response_json["error_data"]
    assert "items_per_page" in response_json["error_data"]
    assert "page" in response_json["error_data"]


def test_get_item(client):
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
                    ".eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTkzNj" \
                    "k1OCwianRpIjoiMmNiM2Q3ZDMtNzA1NS00YzBjL" \
                    "WFhZGEtYmE2ZmVkYzU2M2M5IiwidHlwZSI6ImFj" \
                    "Y2VzcyIsInN1YiI6MjUsIm5iZiI6MTY4NTkzNjk" \
                    "1OCwiZXhwIjoxNjg1OTM3ODU4fQ.6JtqIH_4GoW" \
                    "T6LGauhQiZZUdpTDkfVOHjAt0Np3p73c"

    # assert token is expired
    response = client.get("/items/20", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert response.status_code == 401

    # assert item_id not a number
    response = client.get("/items/20a")
    assert response.status_code == 400

    # assert item_id not found
    response = client.get("/items/20")
    assert response.status_code == 404


def test_create_item(client):
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
                    ".eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTkzNj" \
                    "k1OCwianRpIjoiMmNiM2Q3ZDMtNzA1NS00YzBjL" \
                    "WFhZGEtYmE2ZmVkYzU2M2M5IiwidHlwZSI6ImFj" \
                    "Y2VzcyIsInN1YiI6MjUsIm5iZiI6MTY4NTkzNjk" \
                    "1OCwiZXhwIjoxNjg1OTM3ODU4fQ.6JtqIH_4GoW" \
                    "T6LGauhQiZZUdpTDkfVOHjAt0Np3p73c"

    # assert do not have jwt token
    response = client.post("/items")
    assert response.status_code == 401

    # assert token is expired
    response = client.post("/items", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert response.status_code == 401

    # get a valid token
    token = client.post("/tokens", json={
        "email": "test_item@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    # create parent category
    random_name = uuid.uuid4()
    response = client.post("/categories", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": f"test - {random_name}"
    })
    assert response.status_code == 200
    response_json = response.get_json()
    assert "id" in response_json
    category_id = response_json["id"]

    # assert request with non-exist body
    response = client.post("/items", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 400

    # assert request with invalid name and description
    response = client.post("/items", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": "    ",
        "description": "     ",
        "category_id": category_id + 1
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "name" in response_json["error_data"]
    assert "description" in response_json["error_data"]

    # assert non-exist category_id
    response = client.post("/items", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": "item_1",
        "description": "description_1",
        "category_id": category_id + 1
    })
    assert response.status_code == 404
    response_json = response.get_json()
    assert "category_id" in response_json["error_data"]

    # assert successful request
    response = client.post("/items", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": "name_1",
        "description": "description_1",
        "category_id": category_id
    })
    assert response.status_code == 200


def test_update_item(client):
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
                    ".eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTkzNj" \
                    "k1OCwianRpIjoiMmNiM2Q3ZDMtNzA1NS00YzBjL" \
                    "WFhZGEtYmE2ZmVkYzU2M2M5IiwidHlwZSI6ImFj" \
                    "Y2VzcyIsInN1YiI6MjUsIm5iZiI6MTY4NTkzNjk" \
                    "1OCwiZXhwIjoxNjg1OTM3ODU4fQ.6JtqIH_4GoW" \
                    "T6LGauhQiZZUdpTDkfVOHjAt0Np3p73c"

    # assert do not have jwt token
    response = client.put("/items/20")
    assert response.status_code == 401

    # assert token is expired
    response = client.put("/items/20", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert response.status_code == 401

    # get a valid token and a forbidden token
    token = client.post("/tokens", json={
        "email": "test_item@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    forbidden_token = client.post("/users", json={
        "email": "test_item2@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    # create parent category
    random_name = uuid.uuid4()
    response = client.post("/categories", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": f"test - {random_name}"
    })
    assert response.status_code == 200
    response_json = response.get_json()
    assert "id" in response_json
    category_id = response_json["id"]

    # create an item
    response = client.post("/items", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": "name_2",
        "description": "description_2",
        "category_id": category_id
    })
    assert response.status_code == 200
    item_id = response.get_json()["id"]

    # assert request with non-exist body
    response = client.put("/items/20", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 400

    # assert request with invalid name and description
    response = client.put("/items/20", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": "    ",
        "description": "     ",
        "category_id": category_id + 1
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "name" in response_json["error_data"]
    assert "description" in response_json["error_data"]

    # assert non-exist category_id
    response = client.put("/items/20", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": "item_1",
        "description": "description_1",
        "category_id": category_id + 1
    })
    assert response.status_code == 404
    response_json = response.get_json()
    assert "category_id" in response_json["error_data"]

    # assert item_id not int
    response = client.put("/items/20a", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": "item_1",
        "description": "description_1",
        "category_id": category_id
    })
    assert response.status_code == 400
    response_json = response.get_json()
    assert "item_id" in response_json["error_data"]

    # assert forbidden action
    response = client.put(f"/items/{item_id}", headers={
        "Authorization": f"Bearer {forbidden_token}"
    }, json={
        "name": "item_3",
        "description": "description_2",
        "category_id": category_id
    })
    assert response.status_code == 403

    # assert successful request
    response = client.put(f"/items/{item_id}", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": "item_3",
        "description": "description_2",
        "category_id": category_id
    })
    assert response.status_code == 200
