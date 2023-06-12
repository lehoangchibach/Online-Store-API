import pytest


def test_get_items_successfully(client):
    response = client.get("/items")
    response_json = response.get_json()
    assert response.status_code == 200
    assert "items" in response_json
    assert "items_per_page" in response_json
    assert "page" in response_json
    assert "total_items" in response_json
    assert response_json["items_per_page"] == 20
    assert response_json["page"] == 1


def test_get_items_successfully_with_query_parameters(client, category):
    query_string = {
        "category_id": category.id,
        "page": 4,
        "items_per_page": 27,
    }

    response = client.get("/items", query_string=query_string)
    response_json = response.get_json()
    assert response.status_code == 200
    assert "items" in response_json
    assert "items_per_page" in response_json
    assert "page" in response_json
    assert "total_items" in response_json
    assert response_json["items_per_page"] == 27
    assert response_json["page"] == 4


def test_get_items_successfully_with_valid_access_token(
    client, valid_access_token_user_1
):
    response = client.get(
        "/items",
        headers={"Authorization": f"Bearer {valid_access_token_user_1}"},
    )
    response_json = response.get_json()
    assert response.status_code == 200
    assert "items" in response_json
    assert "items_per_page" in response_json
    assert "page" in response_json
    assert "total_items" in response_json


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        ({"page": "string"}, "Not a valid integer."),
        ({"page": -4}, "Must be greater than or equal to 1."),
    ],
)
def test_get_items_failed_invalid_page_parameter(test_input, expected_message, client):
    response = client.get("/items", query_string=test_input)
    response_json = response.get_json()

    assert response.status_code == 400
    assert "page" in response_json["error_data"]
    assert response_json["error_data"]["page"][0] == expected_message


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        ({"items_per_page": "string"}, "Not a valid integer."),
        ({"items_per_page": -4}, "Must be greater than or equal to 1."),
    ],
)
def test_get_items_failed_invalid_items_per_page_parameter(
    test_input, expected_message, client
):
    response = client.get("/items", query_string=test_input)
    response_json = response.get_json()

    assert response.status_code == 400
    assert "items_per_page" in response_json["error_data"]
    assert response_json["error_data"]["items_per_page"][0] == expected_message


@pytest.mark.parametrize(
    "test_input, expected_message",
    [("20a", "Not a valid integer."), (-20, "Must be greater than or equal to 0.")],
)
def test_get_items_failed_invalid_category_id_parameter(
    test_input, expected_message, client
):
    response = client.get("/items", query_string={"category_id": test_input})
    response_json = response.get_json()

    assert response.status_code == 400
    assert "category_id" in response_json["error_data"]
    assert response_json["error_data"]["category_id"][0] == expected_message


def test_get_items_failed_category_id_not_found(client, session):
    response = client.get("/items", query_string={"category_id": 10000})
    assert response.status_code == 404
    assert response.get_json()["error_message"] == "Category_id not found."


def test_get_items_failed_invalid_access_token(client, invalid_access_token):
    headers = {"Authorization": f"Bearer {invalid_access_token}"}
    response = client.get("/items", headers=headers)
    assert response.status_code == 401


def test_get_item_successfully(client, item, category):
    response = client.get(f"/items/{item.id}")
    response_json = response.get_json()

    assert response.status_code == 200
    assert "id" in response_json
    assert "name" in response_json
    assert "description" in response_json
    assert "category_id" in response_json
    assert "is_creator" in response_json
    assert response_json["name"] == "fixture_item"
    assert response_json["description"] == "Item description"
    assert response_json["category_id"] == category.id
    assert response_json["is_creator"] is False


def test_get_item_successfully_with_valid_access_token(
    client, valid_access_token_user_1, item
):
    response = client.get(
        f"/items/{item.id}",
        headers={"Authorization": f"Bearer {valid_access_token_user_1}"},
    )
    response_json = response.get_json()

    assert response.status_code == 200
    assert "id" in response_json
    assert "name" in response_json
    assert "description" in response_json
    assert "category_id" in response_json
    assert "is_creator" in response_json
    assert response_json["is_creator"] is True


def test_get_item_failed_invalid_access_token(
    client, session, invalid_access_token, item
):
    headers = {"Authorization": f"Bearer {invalid_access_token}"}
    response = client.get(f"/items/{item.id}", headers=headers)
    assert response.status_code == 401


@pytest.mark.parametrize("test_input", ["20a", -20, 10000])
def test_get_item_failed_item_id_not_found(test_input, client):
    response = client.get(f"/items/{test_input}")
    assert response.status_code == 404


def test_post_items_successfully(client, valid_access_token_user_1, category):
    response = client.post(
        "/items",
        headers={"Authorization": f"Bearer {valid_access_token_user_1}"},
        json={
            "name": "test_post_items_successfully",
            "description": "description",
            "category_id": category.id,
        },
    )

    assert response.status_code == 200
    response_json = response.get_json()
    assert "id" in response_json
    assert "name" in response_json
    assert "description" in response_json
    assert "category_id" in response_json
    assert "is_creator" in response_json
    assert response_json["name"] == "test_post_items_successfully"
    assert response_json["description"] == "description"
    assert response_json["category_id"] == category.id
    assert response_json["is_creator"] is True


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        (None, "Field may not be null."),
        ("", "Length must be between 1 and 255."),
        ("      ", "Length must be between 1 and 255."),
        ("a" * 256, "Length must be between 1 and 255."),
    ],
)
def test_post_items_failed_invalid_name_format(
    test_input,
    expected_message,
    client,
    valid_access_token_user_1,
    category,
    session,
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    json = {
        "name": test_input,
        "description": "description",
        "category_id": category.id,
    }
    response = client.post("/items", headers=headers, json=json)
    response_json = response.get_json()

    assert response.status_code == 400
    assert "name" in response_json["error_data"]
    assert response_json["error_data"]["name"][0] == expected_message


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        (None, "Field may not be null."),
        ("", "Length must be between 1 and 1024."),
        ("      ", "Length must be between 1 and 1024."),
        ("a" * 1025, "Length must be between 1 and 1024."),
    ],
)
def test_post_items_failed_invalid_description_format(
    test_input,
    expected_message,
    client,
    valid_access_token_user_1,
    category,
    session,
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    json = {
        "name": "test_post_items_failed_invalid_description_format",
        "description": test_input,
        "category_id": category.id,
    }
    response = client.post("/items", headers=headers, json=json)
    response_json = response.get_json()

    assert response.status_code == 400
    assert "description" in response_json["error_data"]
    assert response_json["error_data"]["description"][0] == expected_message


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        (None, "Field may not be null."),
        ("        ", "Not a valid integer."),
        ("20a", "Not a valid integer."),
        ("-20", "Not a valid integer."),
        ("20", "Not a valid integer."),
    ],
)
def test_post_items_failed_invalid_category_id_format(
    test_input, expected_message, client, valid_access_token_user_1, session
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    json = {
        "name": "test_post_items_failed_invalid_category_id_format",
        "description": "test_post_items_failed_invalid_category_id_format",
        "category_id": test_input,
    }
    response = client.post("/items", headers=headers, json=json)
    response_json = response.get_json()

    assert response.status_code == 400
    assert "category_id" in response_json["error_data"]
    assert response_json["error_data"]["category_id"][0] == expected_message


def test_post_items_failed_category_id_not_found(
    client, session, valid_access_token_user_1
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    json = {
        "name": "test_post_items_failed_category_id_not_found",
        "description": "test_post_items_failed_category_id_not_found",
        "category_id": 10000,
    }
    response = client.post("/items", headers=headers, json=json)
    assert response.status_code == 400
    assert response.get_json()["error_message"] == "Category_id not found."


def test_post_items_failed_item_name_existed(
    client, valid_access_token_user_1, category, session
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    json = {
        "name": "fixture_item",
        "description": "test_post_items_failed_item_name_existed",
        "category_id": category.id,
    }

    response = client.post("/items", headers=headers, json=json)
    assert response.status_code == 400
    assert "name" in response.get_json()["error_data"]
    assert (
        response.get_json()["error_data"]["name"][0]
        == "Name already belong to another item."
    )


def test_delete_items_successfully(
    client,
    session,
    valid_access_token_user_1,
    item_for_delete_successfully,
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    response = client.delete(
        f"/items/{item_for_delete_successfully.id}", headers=headers
    )
    assert response.status_code == 200


@pytest.mark.parametrize("test_input", ["20a", -20, 10000])
def test_delete_items_failed_item_id_not_found(
    test_input, client, valid_access_token_user_1
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    response = client.delete(f"/items/{test_input}", headers=headers)
    assert response.status_code == 404


def test_delete_items_failed_forbidden(
    client, valid_access_token_user_2, item_for_delete_forbidden
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_2}"}
    response = client.delete(f"/items/{item_for_delete_forbidden.id}", headers=headers)
    assert response.status_code == 403


def test_delete_items_failed_invalid_access_token(client, invalid_access_token, item):
    headers = {"Authorization": f"Bearer {invalid_access_token}"}

    response = client.delete(f"/items/{item.id}")
    assert response.status_code == 401

    response = client.delete(f"/items/{item.id}", headers=headers)
    assert response.status_code == 401


def test_put_items_successfully(
    client,
    valid_access_token_user_1,
    item_for_update_successfully,
    category,
):
    response = client.put(
        f"/items/{item_for_update_successfully.id}",
        headers={"Authorization": f"Bearer {valid_access_token_user_1}"},
        json={
            "name": "test_put_items_successfully",
            "description": "description123",
            "category_id": category.id,
        },
    )
    response_json = response.get_json()

    assert response.status_code == 200
    assert "id" in response_json
    assert "name" in response_json
    assert "description" in response_json
    assert "category_id" in response_json
    assert "is_creator" in response_json
    assert response_json["name"] == "test_put_items_successfully"
    assert response_json["description"] == "description123"
    assert response_json["is_creator"] is True


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        (None, "Field may not be null."),
        ("", "Length must be between 1 and 255."),
        ("      ", "Length must be between 1 and 255."),
        ("a" * 256, "Length must be between 1 and 255."),
    ],
)
def test_put_items_failed_invalid_name_format(
    test_input,
    expected_message,
    client,
    valid_access_token_user_1,
    category,
    item,
    session,
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    json = {
        "name": test_input,
        "description": "description",
        "category_id": category.id,
    }
    response = client.put(f"/items/{item.id}", headers=headers, json=json)
    response_json = response.get_json()

    assert response.status_code == 400
    assert "name" in response_json["error_data"]
    assert response_json["error_data"]["name"][0] == expected_message


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        (None, "Field may not be null."),
        ("", "Length must be between 1 and 1024."),
        ("      ", "Length must be between 1 and 1024."),
        ("a" * 1025, "Length must be between 1 and 1024."),
    ],
)
def test_put_items_failed_invalid_description_format(
    test_input,
    expected_message,
    client,
    valid_access_token_user_1,
    category,
    item,
    session,
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    json = {
        "name": "test_put_items_failed_invalid_description_format",
        "description": test_input,
        "category_id": category.id,
    }

    response = client.put(f"/items/{item.id}", headers=headers, json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "description" in response_json["error_data"]
    assert response_json["error_data"]["description"][0] == expected_message


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        (None, "Field may not be null."),
        ("        ", "Not a valid integer."),
        ("20a", "Not a valid integer."),
        ("-20", "Not a valid integer."),
        ("20", "Not a valid integer."),
    ],
)
def test_put_items_failed_invalid_category_id_format(
    test_input,
    expected_message,
    client,
    valid_access_token_user_1,
    item,
    session,
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    json = {
        "name": "test_put_items_failed_invalid_category_id_format",
        "description": "test_put_items_failed_invalid_category_id_format",
        "category_id": test_input,
    }
    response = client.put(f"/items/{item.id}", headers=headers, json=json)
    response_json = response.get_json()

    assert response.status_code == 400
    assert "category_id" in response_json["error_data"]
    assert response_json["error_data"]["category_id"][0] == expected_message


def test_put_items_failed_category_id_not_found(
    client, valid_access_token_user_1, item, session
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    json = {
        "name": "test_put_items_failed_category_id_not_found",
        "description": "test_put_items_failed_category_id_not_found",
        "category_id": 10000,
    }
    response = client.put(f"/items/{item.id}", headers=headers, json=json)
    assert response.status_code == 400
    assert response.get_json()["error_message"] == "Category_id not found."


@pytest.mark.parametrize("test_input", ["20a", -20, 10000])
def test_put_items_failed_item_id_not_found(
    test_input, client, valid_access_token_user_1, session
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    response = client.put(f"/items/{test_input}", headers=headers)
    assert response.status_code == 404


def test_put_items_failed_item_name_existed(
    client,
    valid_access_token_user_1,
    item,
    item_for_update_failed_item_name_existed,
    category,
    session,
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    json = {
        "name": item.name,
        "description": "test_put_items_failed_item_name_existed",
        "category_id": category.id,
    }
    response = client.put(
        f"/items/{item_for_update_failed_item_name_existed.id}",
        headers=headers,
        json=json,
    )

    assert response.status_code == 400
    assert (
        response.get_json()["error_data"]["name"][0]
        == "Item's name has already exists."
    )


def test_put_items_failed_forbidden(
    client,
    valid_access_token_user_2,
    category,
    item,
    session,
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_2}"}
    json = {
        "name": "test_put_items_failed_forbidden",
        "description": "test_put_items_failed_forbidden",
        "category_id": category.id,
    }
    response = client.put(f"/items/{item.id}", headers=headers, json=json)
    assert response.status_code == 403
