def test_get_categories_successfully(client, session):
    # assert success request
    query_string = {
        "page_number": 1,
        "page_size": 23,
    }

    token = client.post("/users", json={
        "email": "test_get_categories_successfully@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    response = client.get("/categories")
    response_json = response.get_json()
    assert response.status_code == 200
    assert "categories" in response_json
    assert "items_per_page" in response_json
    assert "page" in response_json
    assert "total_items" in response_json

    response = client.get("/categories", query_string=query_string)
    response_json = response.get_json()
    assert response.status_code == 200
    assert "categories" in response_json
    assert "items_per_page" in response_json
    assert "page" in response_json
    assert "total_items" in response_json

    response = client.get("/categories", headers={
        "Authorization": f"Bearer {token}"
    })
    response_json = response.get_json()
    assert response.status_code == 200
    assert "categories" in response_json
    assert "items_per_page" in response_json
    assert "page" in response_json
    assert "total_items" in response_json


def test_get_categories_invalid_page(client, session):
    # assert not valid page query parameter
    response = client.get("/categories", query_string={"page": "string"})
    response_json = response.get_json()
    assert response.status_code == 400
    assert "page" in response_json["error_data"]

    response = client.get("/categories", query_string={"page": -4})
    response_json = response.get_json()
    assert response.status_code == 400
    assert "page" in response_json["error_data"]


def test_get_categories_invalid_items_per_page(client, session):
    # assert not valid page query parameter
    response = client.get("/categories", query_string={"items_per_page": "string"})
    response_json = response.get_json()
    assert response.status_code == 400
    assert "items_per_page" in response_json["error_data"]

    response = client.get("/categories", query_string={"items_per_page": -4})
    response_json = response.get_json()
    assert response.status_code == 400
    assert "items_per_page" in response_json["error_data"]


def test_post_categories_successfully(client, session):
    # assert successful request
    token = client.post("/users", json={
        "email": "test_post_categories_successfully@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    response = client.post("/categories", headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "name": f"test - test_post_categories_successfully"
    })
    assert response.status_code == 200
    response_json = response.get_json()
    assert "id" in response_json
    assert "name" in response_json
    assert "is_creator" in response_json


def test_post_categories_invalid_name(client, session):
    token = client.post("/users", json={
        "email": "test_post_categories_invalid_name@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }
    json = {
        "name": ""
    }

    response = client.post("/categories", headers=headers, json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "name" in response_json["error_data"]

    json["name"] = None
    response = client.post("/categories", headers=headers, json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "name" in response_json["error_data"]

    json["name"] = "      "
    response = client.post("/categories", headers=headers, json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "name" in response_json["error_data"]

    json["name"] = "a" * 256
    response = client.post("/categories", headers=headers, json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "name" in response_json["error_data"]


def test_post_categories_duplicate_name(client, session):
    token = client.post("/users", json={
        "email": "test_post_categories_duplicate_name@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }
    json = {
        "name": "category_test_name"
    }

    response = client.post("/categories", headers=headers, json=json)
    assert response.status_code == 200

    response = client.post("/categories", headers=headers, json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "name" in response_json["error_data"]


def test_post_categories_invalid_access_token(client, session):
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." \
                    "eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NjE5" \
                    "NzMxOCwianRpIjoiN2QzMWUyM2UtMmU3MC00" \
                    "ODlmLTkwNWEtNDE0ZDI5MjM4NTM4IiwidHlw" \
                    "ZSI6ImFjY2VzcyIsInN1YiI6MjUsIm5iZiI6" \
                    "MTY4NjE5NzMxOCwiZXhwIjoxNjg2MTk4MjE4" \
                    "fQ.Dj0EKAS0zjz3EbWKEIdReKdrduMPy3RPE" \
                    "UDVg_bEA-k"
    headers = {
        "Authorization": f"Bearer {expired_token}"
    }
    json = {
        "name": "category_test_name"
    }

    response = client.post("/categories", json=json)
    assert response.status_code == 401

    response = client.post("/categories", headers=headers, json=json)
    assert response.status_code == 401


def test_delete_categories_successfully(client):
    token = client.post("/users", json={
        "email": "test_delete_categories_successfully@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }
    json = {
        "name": "test_delete_categories_successfully"
    }

    response = client.post("/categories", headers=headers, json=json)
    assert response.status_code == 200
    assert "id" in response.get_json()
    category_id = response.get_json()["id"]

    response = client.delete(f"/categories/{category_id}", headers=headers)
    assert response.status_code == 200


def test_delete_categories_invalid_access_token(client, session):
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." \
                    "eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NjE5" \
                    "NzMxOCwianRpIjoiN2QzMWUyM2UtMmU3MC00" \
                    "ODlmLTkwNWEtNDE0ZDI5MjM4NTM4IiwidHlw" \
                    "ZSI6ImFjY2VzcyIsInN1YiI6MjUsIm5iZiI6" \
                    "MTY4NjE5NzMxOCwiZXhwIjoxNjg2MTk4MjE4" \
                    "fQ.Dj0EKAS0zjz3EbWKEIdReKdrduMPy3RPE" \
                    "UDVg_bEA-k"
    headers = {
        "Authorization": f"Bearer {expired_token}"
    }

    response = client.delete(f"/categories/{20}")
    assert response.status_code == 401

    response = client.delete(f"/categories/{20}", headers=headers)
    assert response.status_code == 401


def test_delete_categories_invalid_category_id(client, session):
    token = client.post("/users", json={
        "email": "test_delete_categories_invalid_category_id@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.delete(f"/categories/20a", headers=headers)
    assert response.status_code == 400
    assert "category_id" in response.get_json()["error_data"]

    response = client.delete(f"/categories/{-20}", headers=headers)
    assert response.status_code == 400
    assert "category_id" in response.get_json()["error_data"]


def test_delete_categories_not_found_category_id(client, session):
    token = client.post("/users", json={
        "email": "test_delete_categories_not_found_category_id@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.delete(f"/categories/{0}", headers=headers)
    assert response.status_code == 404
    assert "category_id" in response.get_json()["error_data"]


def test_delete_categories_forbidden(client):
    token = client.post("/users", json={
        "email": "test_delete_categories_forbidden@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    forbidden_token = client.post("/users", json={
        "email": "test_delete_categories_forbidden123@gmail.com",
        "password": "Password123"
    }).get_json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }
    json = {
        "name": "test_delete_categories_forbidden"
    }

    response = client.post("/categories", headers=headers, json=json)
    assert response.status_code == 200
    assert "id" in response.get_json()
    category_id = response.get_json()["id"]

    headers = {
        "Authorization": f"Bearer {forbidden_token}"
    }
    response = client.delete(f"/categories/{category_id}", headers=headers)
    assert response.status_code == 403
