import uuid


def test_get_categories(client):
    # assert success request
    response = client.get("/categories")
    response_json = response.get_json()
    assert response.status_code == 200
    assert "categories" in response_json
    assert "items_per_page" in response_json
    assert "page" in response_json
    assert "total_items" in response_json

    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
                    ".eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTkzNj" \
                    "k1OCwianRpIjoiMmNiM2Q3ZDMtNzA1NS00YzBjL" \
                    "WFhZGEtYmE2ZmVkYzU2M2M5IiwidHlwZSI6ImFj" \
                    "Y2VzcyIsInN1YiI6MjUsIm5iZiI6MTY4NTkzNjk" \
                    "1OCwiZXhwIjoxNjg1OTM3ODU4fQ.6JtqIH_4GoW" \
                    "T6LGauhQiZZUdpTDkfVOHjAt0Np3p73c"

    # assert expired token
    response = client.get("/categories", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert response.status_code == 401

    # assert not valid query parameter
    response = client.get("/categories", query_string={
        "page_number": "asd",
        "page_size": 20,
    })
    response_json = response.get_json()
    assert response.status_code == 400
    assert "page" in response_json["error_data"]

    response = client.get("/categories", query_string={
        "page_number": 0,
        "page_size": "20a",
    })
    response_json = response.get_json()
    assert response.status_code == 400
    assert "items_per_page" in response_json["error_data"]


def test_post_categories(client):
    #     assert no jwt token
    response = client.post("/categories")
    assert response.status_code == 401

    # create new user with a valid token
    token = client.post("/users", json={
        "email": "test_category@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    # assert request with no body
    response = client.post("/categories", headers={
        "Authorization": f"Bearer {token}"
    })
    response_json = response.get_json()
    assert response.status_code == 400
    assert "name" in response_json["error_data"]

    # assert request with invalid name
    response = client.post("/categories", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": "    "
    })
    response_json = response.get_json()
    assert response.status_code == 400
    assert "name" in response_json["error_data"]

    response = client.post("/categories", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                "aaaaaaaaaaa"
    })
    response_json = response.get_json()
    assert response.status_code == 400
    assert "name" in response_json["error_data"]

    # assert successful request
    random_name = uuid.uuid4()
    response = client.post("/categories", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": f"test - {random_name}"
    })
    assert response.status_code == 200
    response_json = response.get_json()
    assert "id" in response_json


def test_delete_categories(client):
    # get a valid token
    token = client.post("/tokens", json={
        "email": "test_category@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    # get a forbidden token (not creator)
    forbidden_token = client.post("/users", json={
        "email": "test_category2@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    # create a category
    random_name = uuid.uuid4()
    response = client.post("/categories", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": f"test - {random_name}"
    })
    assert response.status_code == 200
    category_id = response.get_json()["id"]

    # assert request with no token
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 401

    # assert request with invalid category_id
    response = client.delete(f"/categories/{category_id}a", headers={
        "Authorization": f"Bearer {token}"
    })
    response_json = response.get_json()
    assert response.status_code == 400
    assert "category_id" in response_json["error_data"]

    # assert request with forbidden token
    response = client.delete(f"/categories/{category_id}", headers={
        "Authorization": f"Bearer {forbidden_token}"
    })
    assert response.status_code == 403

    # assert successful request
    response = client.delete(f"/categories/{category_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
