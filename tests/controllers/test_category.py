import pytest


def test_get_categories_successfully(client):
    response = client.get("/categories")
    response_json = response.get_json()

    assert response.status_code == 200
    assert "categories" in response_json
    assert "total_items" in response_json
    assert response_json["items_per_page"] == 20
    assert response_json["page"] == 1


def test_get_categories_successfully_with_query_parameters(client):
    # assert success request
    response = client.get(
        "/categories",
        query_string={
            "page": 5,
            "items_per_page": 23,
        },
    )
    response_json = response.get_json()

    assert response.status_code == 200
    assert response_json["items_per_page"] == 23
    assert response_json["page"] == 5


def test_get_categories_successfully_with_access_token(
    client, valid_access_token_user_1
):
    response = client.get(
        "/categories",
        headers={"Authorization": f"Bearer {valid_access_token_user_1}"},
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        ({"page": "string"}, "Not a valid integer."),
        ({"page": -4}, "Must be greater than or equal to 1."),
    ],
)
def test_get_categories_failed_invalid_page_parameter(
    test_input, expected_message, client
):
    response = client.get("/categories", query_string=test_input)
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
def test_get_categories_failed_invalid_items_per_page_parameter(
    test_input, expected_message, client, session
):
    response = client.get("/categories", query_string=test_input)
    response_json = response.get_json()
    assert response.status_code == 400
    assert "items_per_page" in response_json["error_data"]
    assert response_json["error_data"]["items_per_page"][0] == expected_message


def test_post_categories_successfully(client, session, valid_access_token_user_1):
    response = client.post(
        "/categories",
        headers={"Authorization": f"Bearer {valid_access_token_user_1}"},
        json={"name": "test_post_categories_successfully"},
    )
    response_json = response.get_json()

    assert response.status_code == 200
    assert "id" in response_json
    assert "name" in response_json
    assert "is_creator" in response_json
    assert response_json["name"] == "test_post_categories_successfully"
    assert response_json["is_creator"] is True


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        ({"name": None}, "Field may not be null."),
        ({"name": ""}, "Length must be between 1 and 255."),
        ({"name": "      "}, "Length must be between 1 and 255."),
        ({"name": "a" * 256}, "Length must be between 1 and 255."),
        ({"name": 256}, "Not a valid string."),
    ],
)
def test_post_categories_failed_invalid_name_format(
    test_input, expected_message, client, valid_access_token_user_1
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}

    response = client.post("/categories", headers=headers, json=test_input)
    response_json = response.get_json()

    assert response.status_code == 400
    assert "name" in response_json["error_data"]
    assert response_json["error_data"]["name"][0] == expected_message


def test_post_categories_failed_name_existed(
    client, category, valid_access_token_user_1
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    json = {"name": category.name}

    response = client.post("/categories", headers=headers, json=json)
    response_json = response.get_json()

    assert response.status_code == 400
    assert "name" in response_json["error_data"]
    assert (
        response_json["error_data"]["name"][0]
        == "Name already belong to another category."
    )


def test_post_categories_failed_expired_access_token(client, invalid_access_token):
    headers = {"Authorization": f"Bearer {invalid_access_token}"}
    json = {"name": "test_post_categories_failed_expired_access_token"}

    response = client.post("/categories", json=json)
    assert response.status_code == 401

    response = client.post("/categories", headers=headers, json=json)
    assert response.status_code == 401


def test_post_categories_failed_invalid_access_token(client):
    headers = {"Authorization": "Bearer"}
    json = {"name": "test_post_categories_failed_invalid_access_token"}
    response = client.post("/categories", headers=headers, json=json)
    assert response.status_code == 401


def test_delete_categories_successfully(
    client, valid_access_token_user_1, category_for_delete_successfully
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}

    response = client.delete(
        f"/categories/{category_for_delete_successfully.id}", headers=headers
    )
    assert response.status_code == 200


def test_delete_categories_failed_invalid_access_token(client, invalid_access_token):
    headers = {"Authorization": f"Bearer {invalid_access_token}"}

    response = client.delete("/categories/20")
    assert response.status_code == 401

    response = client.delete("/categories/20", headers=headers)
    assert response.status_code == 401


@pytest.mark.parametrize("test_input", ["20a", -20, 10000])
def test_delete_categories_failed_category_id_not_found(
    test_input, client, valid_access_token_user_1
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    response = client.delete(f"/categories/{test_input}", headers=headers)
    assert response.status_code == 404


def test_delete_categories_failed_forbidden(
    client,
    category_for_delete_failed_forbidden,
    valid_access_token_user_2,
):
    headers = {"Authorization": f"Bearer {valid_access_token_user_2}"}
    response = client.delete(
        f"/categories/{category_for_delete_failed_forbidden.id}", headers=headers
    )
    assert response.status_code == 403


def test_delete_categories_failed_internal_server_error(
    client, valid_access_token_user_1, category_for_delete_failed_forbidden, mocker
):
    mocked_delete = mocker.patch("sqlalchemy.orm.session.Session.delete")
    mocked_delete.side_effect = Exception("Test")

    headers = {"Authorization": f"Bearer {valid_access_token_user_1}"}
    response = client.delete(
        f"/categories/{category_for_delete_failed_forbidden.id}", headers=headers
    )
    assert response.status_code == 500
    assert response.get_json()["error_message"] == "Internal Server Error."
