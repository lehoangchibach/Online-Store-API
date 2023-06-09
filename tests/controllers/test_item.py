# def test_get_items_successfully(client, session):
#     # assert success request
#     query_string = {
#         "category_id": None,
#         "page_number": 1,
#         "page_size": 23,
#     }
#
#     token = client.post("/users", json={
#         "email": "test_get_items_successfully@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.get("/items")
#     response_json = response.get_json()
#     assert response.status_code == 200
#     assert "items" in response_json
#     assert "items_per_page" in response_json
#     assert "page" in response_json
#     assert "total_items" in response_json
#
#     response = client.get("/items", query_string=query_string)
#     response_json = response.get_json()
#     assert response.status_code == 200
#     assert "items" in response_json
#     assert "items_per_page" in response_json
#     assert "page" in response_json
#     assert "total_items" in response_json
#
#     response = client.get("/items", headers={
#         "Authorization": f"Bearer {token}"
#     })
#     response_json = response.get_json()
#     assert response.status_code == 200
#     assert "items" in response_json
#     assert "items_per_page" in response_json
#     assert "page" in response_json
#     assert "total_items" in response_json
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_get_items_successfully"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     query_string["category_id"] = category_id
#     response = client.get("/items", query_string=query_string)
#     response_json = response.get_json()
#     assert response.status_code == 200
#     assert "items" in response_json
#     assert "items_per_page" in response_json
#     assert "page" in response_json
#     assert "total_items" in response_json
#
#
# def test_get_items_invalid_page(client, session):
#     response = client.get("/items", query_string={"page": "string"})
#     response_json = response.get_json()
#     assert response.status_code == 400
#     assert "page" in response_json["error_data"]
#
#     response = client.get("/items", query_string={"page": -4})
#     response_json = response.get_json()
#     assert response.status_code == 400
#     assert "page" in response_json["error_data"]
#
#
# def test_get_items_invalid_items_per_page(client, session):
#     response = client.get("/items", query_string={"items_per_page": "string"})
#     response_json = response.get_json()
#     assert response.status_code == 400
#     assert "items_per_page" in response_json["error_data"]
#
#     response = client.get("/items", query_string={"items_per_page": -4})
#     response_json = response.get_json()
#     assert response.status_code == 400
#     assert "items_per_page" in response_json["error_data"]
#
#
# def test_get_items_invalid_category_id(client, session):
#     response = client.get("/items", query_string={"category_id": "12a"})
#     response_json = response.get_json()
#     assert response.status_code == 400
#     assert "category_id" in response_json["error_data"]
#
#     response = client.get("/items", query_string={"category_id": -4})
#     response_json = response.get_json()
#     assert response.status_code == 400
#     assert "category_id" in response_json["error_data"]
#
#
# def test_get_items_not_found_category_id(client, session):
#     response = client.get("/items", query_string={"category_id": 10000})
#     response_json = response.get_json()
#     assert response.status_code == 404
#
#
# def test_get_items_invalid_access_token(client, session):
#     expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." \
#                     "eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NjE5" \
#                     "NzMxOCwianRpIjoiN2QzMWUyM2UtMmU3MC00" \
#                     "ODlmLTkwNWEtNDE0ZDI5MjM4NTM4IiwidHlw" \
#                     "ZSI6ImFjY2VzcyIsInN1YiI6MjUsIm5iZiI6" \
#                     "MTY4NjE5NzMxOCwiZXhwIjoxNjg2MTk4MjE4" \
#                     "fQ.Dj0EKAS0zjz3EbWKEIdReKdrduMPy3RPE" \
#                     "UDVg_bEA-k"
#     headers = {
#         "Authorization": f"Bearer {expired_token}"
#     }
#
#     response = client.get("/items", headers=headers)
#     assert response.status_code == 401
#
#
# def test_get_item_successfully(client, session):
#     # assert success request
#     token = client.post("/users", json={
#         "email": "test_get_item_successfully@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_get_item_successfully"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     response = client.post("/items", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_get_item_successfully",
#         "description": "description",
#         "category_id": category_id
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     item_id = response.get_json()["id"]
#
#     response = client.get(f"/items/{item_id}")
#     response_json = response.get_json()
#     assert response.status_code == 200
#     assert "id" in response_json
#     assert "name" in response_json
#     assert "description" in response_json
#     assert "category_id" in response_json
#     assert "is_creator" in response_json
#
#
# def test_get_item_invalid_access_token(client, session):
#     expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." \
#                     "eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NjE5" \
#                     "NzMxOCwianRpIjoiN2QzMWUyM2UtMmU3MC00" \
#                     "ODlmLTkwNWEtNDE0ZDI5MjM4NTM4IiwidHlw" \
#                     "ZSI6ImFjY2VzcyIsInN1YiI6MjUsIm5iZiI6" \
#                     "MTY4NjE5NzMxOCwiZXhwIjoxNjg2MTk4MjE4" \
#                     "fQ.Dj0EKAS0zjz3EbWKEIdReKdrduMPy3RPE" \
#                     "UDVg_bEA-k"
#     headers = {
#         "Authorization": f"Bearer {expired_token}"
#     }
#
#     response = client.get("/items/20", headers=headers)
#     assert response.status_code == 401
#
#
# def test_get_item_invalid_item_id(client, session):
#     response = client.get(f"/items/20a")
#     assert response.status_code == 404
#
#     response = client.get(f"/items/{-29}")
#     assert response.status_code == 404
#
#
# def test_get_item_not_found_item_id(client, session):
#     response = client.get(f"/items/{10000}")
#     assert response.status_code == 404
#
#
# def test_post_items_successfully(client, session):
#     # assert successful request
#     token = client.post("/users", json={
#         "email": "test_post_items_successfully@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_post_items_successfully"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     response = client.post("/items", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_post_items_successfully",
#         "description": "description",
#         "category_id": category_id
#     })
#     assert response.status_code == 200
#     response_json = response.get_json()
#     assert "id" in response_json
#     assert "name" in response_json
#     assert "description" in response_json
#     assert "category_id" in response_json
#     assert "is_creator" in response_json
#
#
# def test_post_items_invalid_name(client, session):
#     token = client.post("/users", json={
#         "email": "test_post_items_invalid_name@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_post_items_invalid_name"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "",
#         "description": "description",
#         "category_id": category_id
#     }
#
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "name" in response_json["error_data"]
#
#     json["name"] = None
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "name" in response_json["error_data"]
#
#     json["name"] = "      "
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "name" in response_json["error_data"]
#
#     json["name"] = "a" * 256
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "name" in response_json["error_data"]
#
#
# def test_post_items_invalid_description(client, session):
#     token = client.post("/users", json={
#         "email": "test_post_items_invalid_description@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_post_items_invalid_description"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "test - test_post_items_invalid_description",
#         "description": "",
#         "category_id": category_id
#     }
#
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "description" in response_json["error_data"]
#
#     json["description"] = None
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "description" in response_json["error_data"]
#
#     json["description"] = "      "
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "description" in response_json["error_data"]
#
#     json["description"] = "a" * 1025
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "description" in response_json["error_data"]
#
#
# def test_post_items_invalid_category_id(client, session):
#     token = client.post("/users", json={
#         "email": "test_post_items_invalid_category_id@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_post_items_invalid_category_id"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "test - test_post_items_invalid_category_id",
#         "description": "test - test_post_items_invalid_category_id",
#         "category_id": None
#     }
#
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "category_id" in response_json["error_data"]
#
#     json["category_id"] = "20a"
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "category_id" in response_json["error_data"]
#
#     json["category_id"] = "20"
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "category_id" in response_json["error_data"]
#
#     json["category_id"] = -20
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "category_id" in response_json["error_data"]
#
#
# def test_post_items_not_found_category_id(client, session):  # category_id not found
#     token = client.post("/users", json={
#         "email": "test_post_items_not_found_category_id@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "test - test_post_items_invalid_category_id",
#         "description": "test - test_post_items_invalid_category_id",
#         "category_id": 10000
#     }
#
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400  # convert to 400
#
#
# def test_post_items_duplicate_item_name(client, session):
#     token = client.post("/users", json={
#         "email": "test_post_items_duplicate_item_name@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_post_items_duplicate_item_name"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "test - test_post_items_duplicate_item_name",
#         "description": "test - test_post_items_duplicate_item_name",
#         "category_id": category_id
#     }
#
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 200
#
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 400
#     assert "name" in response.get_json()["error_data"]
#
#
# def test_delete_items_successfully(client, session):
#     token = client.post("/users", json={
#         "email": "test_delete_items_successfully@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_delete_items_successfully"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "test - test_delete_items_successfully",
#         "description": "test - test_delete_items_successfully",
#         "category_id": category_id
#     }
#
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     item_id = response.get_json()["id"]
#
#     response = client.delete(f"/items/{item_id}", headers=headers)
#     assert response.status_code == 200
#
#
# def test_delete_items_invalid_item_id(client, session):
#     token = client.post("/users", json={
#         "email": "test_delete_items_invalid_item_id@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#
#     response = client.delete(f"/items/20a", headers=headers)
#     assert response.status_code == 404
#
#     response = client.delete(f"/items/{-20}", headers=headers)
#     assert response.status_code == 404
#
#
# def test_delete_items_not_found_item_id(client, session):
#     token = client.post("/users", json={
#         "email": "test_delete_items_not_found_item_id@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#
#     response = client.delete(f"/items/{2000}", headers=headers)
#     assert response.status_code == 404
#
#
# def test_delete_items_forbidden(client, session):
#     token = client.post("/users", json={
#         "email": "test_delete_items_forbidden@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     forbidden_token = client.post("/users", json={
#         "email": "test_delete_items_forbidden123@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_delete_items_forbidden"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "test - test_delete_items_forbidden",
#         "description": "test - test_delete_items_forbidden",
#         "category_id": category_id
#     }
#
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     item_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {forbidden_token}"
#     }
#     response = client.delete(f"/items/{item_id}", headers=headers)
#     assert response.status_code == 403
#
#
# def test_delete_items_invalid_access_token(client, session):
#     expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." \
#                     "eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NjE5" \
#                     "NzMxOCwianRpIjoiN2QzMWUyM2UtMmU3MC00" \
#                     "ODlmLTkwNWEtNDE0ZDI5MjM4NTM4IiwidHlw" \
#                     "ZSI6ImFjY2VzcyIsInN1YiI6MjUsIm5iZiI6" \
#                     "MTY4NjE5NzMxOCwiZXhwIjoxNjg2MTk4MjE4" \
#                     "fQ.Dj0EKAS0zjz3EbWKEIdReKdrduMPy3RPE" \
#                     "UDVg_bEA-k"
#     headers = {
#         "Authorization": f"Bearer {expired_token}"
#     }
#
#     response = client.delete(f"/items/20")
#     assert response.status_code == 401
#
#     response = client.delete(f"/items/20", headers=headers)
#     assert response.status_code == 401
#
#
# ######################
# def test_put_items_successfully(client, session):
#     # assert successful request
#     token = client.post("/users", json={
#         "email": "test_put_items_successfully@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_put_items_successfully"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     response = client.post("/items", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_put_items_successfully",
#         "description": "description",
#         "category_id": category_id
#     })
#     assert response.status_code == 200
#     response_json = response.get_json()
#     assert "id" in response_json
#     assert "name" in response_json
#     assert "description" in response_json
#     assert "category_id" in response_json
#     assert "is_creator" in response_json
#
#     item_id = response_json["id"]
#     response = client.put(f"/items/{item_id}", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_put_items_successfully123",
#         "description": "description123",
#         "category_id": category_id
#     })
#     assert response.status_code == 200
#     response_json = response.get_json()
#     assert "id" in response_json
#     assert "name" in response_json
#     assert "description" in response_json
#     assert "category_id" in response_json
#     assert "is_creator" in response_json
#
#
# def test_put_items_invalid_name(client, session):
#     token = client.post("/users", json={
#         "email": "test_put_items_invalid_name@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_put_items_invalid_name"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "",
#         "description": "description",
#         "category_id": category_id
#     }
#
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "name" in response_json["error_data"]
#
#     json["name"] = None
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "name" in response_json["error_data"]
#
#     json["name"] = "      "
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "name" in response_json["error_data"]
#
#     json["name"] = "a" * 256
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "name" in response_json["error_data"]
#
#
# def test_put_items_invalid_description(client, session):
#     token = client.post("/users", json={
#         "email": "test_put_items_invalid_description@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_put_items_invalid_description"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "test_put_items_invalid_description",
#         "description": "",
#         "category_id": category_id
#     }
#
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "description" in response_json["error_data"]
#
#     json["description"] = None
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "description" in response_json["error_data"]
#
#     json["description"] = "      "
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "description" in response_json["error_data"]
#
#     json["description"] = "a" * 1025
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "description" in response_json["error_data"]
#
#
# def test_put_items_invalid_category_id(client, session):
#     token = client.post("/users", json={
#         "email": "test_put_items_invalid_category_id@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_put_items_invalid_category_id"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "test - test_put_items_invalid_category_id",
#         "description": "test - test_put_items_invalid_category_id",
#         "category_id": None
#     }
#
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "category_id" in response_json["error_data"]
#
#     json["category_id"] = "20a"
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "category_id" in response_json["error_data"]
#
#     json["category_id"] = "20"
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "category_id" in response_json["error_data"]
#
#     json["category_id"] = -20
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert "category_id" in response_json["error_data"]
#
#
# def test_put_items_not_found_category_id(client, session):
#     token = client.post("/users", json={
#         "email": "test_put_items_not_found_category_id@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_put_items_not_found_category_id"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "test - test_put_items_not_found_category_id",
#         "description": "test - test_put_items_not_found_category_id",
#         "category_id": 10000
#     }
#
#     response = client.put("/items/20", headers=headers, json=json)
#     assert response.status_code == 404
#
#
# def test_put_items_not_found_item_name(client, session):
#     token = client.post("/users", json={
#         "email": "test_put_items_duplicate_item_name@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_put_items_duplicate_item_name"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "test - test_put_items_duplicate_item_name",
#         "description": "test - test_put_items_duplicate_item_name",
#         "category_id": category_id
#     }
#
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 200
#
#     response = client.put(f"/items/{100000}", headers=headers, json=json)
#     assert response.status_code == 404
#
#
# def test_put_items_forbidden(client, session):
#     token = client.post("/users", json={
#         "email": "test_put_items_forbidden@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     forbidden_token = client.post("/users", json={
#         "email": "test_put_items_forbidden123@gmail.com",
#         "password": "Password123"
#     }).get_json()["access_token"]
#
#     response = client.post("/categories", headers={
#         "Authorization": f"Bearer {token}"
#     }, json={
#         "name": "test_put_items_forbidden"
#     })
#     assert response.status_code == 200
#     assert "id" in response.get_json()
#     category_id = response.get_json()["id"]
#
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     json = {
#         "name": "test - test_put_items_forbidden",
#         "description": "test - test_put_items_forbidden",
#         "category_id": category_id
#     }
#
#     response = client.post("/items", headers=headers, json=json)
#     assert response.status_code == 200
#
#     item_id = response.get_json()["id"]
#     headers = {
#         "Authorization": f"Bearer {forbidden_token}"
#     }
#     response = client.put(f"/items/{item_id}", headers=headers, json=json)
#     assert response.status_code == 403
