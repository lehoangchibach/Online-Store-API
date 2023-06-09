import pytest


def test_login_invalid_methods(client, session):
    # assert not support methods
    response = client.get("/tokens")
    assert response.status_code == 405

    response = client.put("/tokens")
    assert response.status_code == 405

    response = client.delete("/tokens")
    assert response.status_code == 405


def test_login_successfully(client, session):
    # assert successful request
    json = {"email": "testemail@gmail.com", "password": "Password123"}

    response = client.post("/tokens", json=json)
    assert response.status_code == 200
    assert "access_token" in response.get_json()


@pytest.mark.parametrize(
    "test_input",
    [
        {
            "email": "wrong_testemail@gmail.com",  # wrong email, correct password
            "password": "Password123",
        },
        {
            "email": "testemail@gmail.com",  # correct email, wrong password
            "password": "Password12345",
        },
    ],
)
def test_login_failed_invalid_credential(test_input, client, session):
    response = client.post("/tokens", json=test_input)
    assert response.status_code == 400
    assert response.get_json()["error_message"] == "Email or password is not correct."


def test_login_failed_invalid_json_body(client, session):
    response = client.post("/tokens", json=None)
    assert response.status_code == 400
    assert response.get_json()["error_message"] == "Request's body is not a json."


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
            "          ",
            "Length of password must in range 6-30.",
        ),  # White-space is stripped
    ],
)
def test_login_failed_invalid_password_format(
    test_input, expected_message, client, session
):
    json = {"email": "test_user@gmail.com", "password": test_input}

    response = client.post("/tokens", json=json)
    assert response.status_code == 400
    response_json = response.get_json()
    assert "password" in response_json["error_data"]
    assert response_json["error_data"]["password"][0] == expected_message


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
def test_login_failed_invalid_email_format(
    test_input, expected_message, client, session
):
    # assert request with invalid email
    json = {"email": test_input, "password": "Password"}

    response = client.post("/tokens", json=json)
    assert response.status_code == 400
    assert "email" in response.get_json()["error_data"]
    assert response.get_json()["error_data"]["email"][0] == expected_message
