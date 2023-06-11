import pytest


def test_create_user_invalid_methods(client, session):
    # assert not supported methods
    response = client.get("/users")
    assert response.status_code == 405

    response = client.put("/users")
    assert response.status_code == 405

    response = client.delete("/users")
    assert response.status_code == 405


def test_create_user_successfully(client, session):
    response = client.post(
        "/users",
        json={
            "email": "test_create_user_successfully@gmail.com",
            "password": "Password123",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_create_user_failed_email_existed(client, session):
    response = client.post(
        "/users",
        json={
            "email": "testemail@gmail.com",
            "password": "Password123",
        },
    )
    assert response.status_code == 400
    assert (
        response.get_json()["error_message"]
        == "Email already belong to another account."
    )


def test_create_user_failed_invalid_json_body(client, session):
    response = client.post("/users", json=None)
    assert response.status_code == 400
    assert response.get_json()["error_message"] == "Request's body is not a valid json."


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        (None, "Field may not be null."),  # Field can not be none
        ("Password", "Password does not meet constraints."),  # Does not contain number
        (
            "password123",
            "Password does not meet constraints.",
        ),  # Does not capitalize characters
        ("Pd123", "Length of password must in range 6-30."),  # Length must be > 6
        ("a" * 31, "Length of password must in range 6-30."),  # Length must be < 30
        (
            "       ",
            "Length of password must in range 6-30.",
        ),  # White-space is stripped
        (1234, "Password must be a string."),  # Password is not a string
    ],
)
def test_create_user_failed_invalid_password_format(
    test_input, expected_message, client, session
):
    json = {"email": "test_user@gmail.com", "password": test_input}
    response = client.post("/users", json=json)

    assert response.status_code == 400
    assert "password" in response.get_json()["error_data"]
    assert response.get_json()["error_data"]["password"][0] == expected_message


@pytest.mark.parametrize(
    "test_input, expected_message",
    [
        (None, "Field may not be null."),
        ("@gmail.com", "Not a valid email address."),
        ("bachle@.com", "Not a valid email address."),
        ("bachle@gmail", "Not a valid email address."),
        ("  sdf ", "Not a valid email address."),
    ],
)
def test_create_user_failed_invalid_email_format(
    test_input, expected_message, client, session
):
    json = {"email": test_input, "password": "Password123"}
    response = client.post("/users", json=json)

    assert response.status_code == 400
    assert "email" in response.get_json()["error_data"]
    assert response.get_json()["error_data"]["email"][0] == expected_message
