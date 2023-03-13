from httpx import AsyncClient


async def test_bad_create_user_not_passord(ac: AsyncClient):
    payload = {
      "hash_password": "",
      "email": "test@test.test",
    }
    response = await ac.post("/users/", json=payload)
    assert response.status_code == 422


async def test_bad_create_user_low_passord(ac: AsyncClient):
    payload = {
      "hash_password": "tet",
      "email": "test@test.test",
    }
    response = await ac.post("/users/", json=payload)
    assert response.status_code == 422


async def test_bad_create_user_dont_match(ac: AsyncClient):
    payload = {
      "hash_password": "test",
      "email": "test@test.test",
    }
    response = await ac.post("/users/", json=payload)
    assert response.status_code == 422


async def test_bad_create_user_no_valid_email(ac: AsyncClient):
    payload = {
      "hash_password": "test",
      "email": "test",
    }
    response = await ac.post("/users/", json=payload)
    assert response.status_code == 422


async def test_create_user_one(ac: AsyncClient):
    payload = {
      "hash_password": "Testpassword123",
      "email": "test1@test.com",
      "username": "test1",
    }
    response = await ac.post("/users/", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 1


async def test_bad_create_user__email_exist(ac: AsyncClient):
    payload = {
      "hash_password": "Testpassword123",
      "email": "test1@test.com",
      "username": "test1",
    }
    response = await ac.post("/users/", json=payload)
    assert response.status_code == 400


async def test_create_user_two(ac: AsyncClient):
    payload = {
      "hash_password": "Testpassword123",
      "email": "test2@test.com",
      "username": "test2",
    }
    response = await ac.post("/users/", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 2


async def test_create_user_three(ac: AsyncClient):
    payload = {
      "hash_password": "Testpassword123",
      "email": "test3@test.com",
      "username": "test3",
    }
    response = await ac.post("/users/", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 3


async def test_create_user_four(ac: AsyncClient):
    payload = {
        "hash_password": "Testpassword123",
        "email": "test4@test.com",
        "username": "test4",
    }
    response = await ac.post("/users/", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 4


async def test_create_user_five(ac: AsyncClient):
    payload = {
        "hash_password": "Testpassword123",
        "email": "test5@test.com",
        "username": "test5",
    }
    response = await ac.post("/users/", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 5


async def test_bad_login_try(ac: AsyncClient):
    payload = {
        "email": "test2@test.com",
        "hash_password": "tess",
    }
    response = await ac.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect username or password'


async def test_try_login_one(ac: AsyncClient, login_user):
    response = await login_user("test1@test.com", "Testpassword123")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


async def test_try_login_two(ac: AsyncClient, login_user):
    response = await login_user("test2@test.com", "Testpassword123")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


async def test_try_login_three(ac: AsyncClient, login_user):
    response = await login_user("test3@test.com", "Testpassword123")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


async def test_try_login_four(ac: AsyncClient, login_user):
    response = await login_user("test4@test.com", "Testpassword123")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


async def test_try_login_five(ac: AsyncClient, login_user):
    response = await login_user("test5@test.com", "Testpassword123")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


async def test_auth_me_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}"
    }
    response = await ac.post("/auth/me", headers=headers)
    print(response.json())
    assert response.status_code == 200
    assert response.json().get('username') == "test1"
    assert response.json().get('email') == "test1@test.com"
    assert response.json().get('id') == 1


async def test_auth_me_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.post("/auth/me", headers=headers)
    print(response.json())
    assert response.status_code == 200
    assert response.json().get('username') == "test2"
    assert response.json().get('email') == "test2@test.com"
    assert response.json().get('id') == 2


async def test_bad_auth_me(ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer sdffaf.afdsg.rtrwtrete",
    }
    response = await ac.post("/auth/me", headers=headers)
    assert response.status_code == 401


async def test_get_users_list(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.get("/users/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("users")) == 5


async def test_get_users_list_unauth(ac: AsyncClient):
    response = await ac.get("/users/")
    assert response.status_code == 403


async def test_get_user_by_id(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}"
    }
    response = await ac.get("/users/2", headers=headers)
    assert response.status_code == 200
    assert response.json().get("id") == 2
    assert response.json().get("email") == 'test2@test.com'
    assert response.json().get("username") == 'test2'


async def test_get_user_by_id_unauth(ac: AsyncClient):
    response = await ac.get("/users/2")
    assert response.status_code == 403


async def test_bad_get_user_by_id__not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}"
    }
    response = await ac.get("/users/6", headers=headers)
    assert response.status_code == 404


async def test_bad_update_user_one__not_your_acc(ac: AsyncClient, users_tokens):
    payload = {
      "username": "test1NEW",
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}"
    }
    response = await ac.put("/users/2", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


async def test_update_user_one(ac: AsyncClient, users_tokens):
    payload = {
      "username": "test1NEW",
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}"
    }
    response = await ac.put("/users/1", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get("id") == 1


async def test_get_user_by_id_updated(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}"
    }
    response = await ac.get("/users/1", headers=headers)
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("email") == 'test1@test.com'
    assert response.json().get("username") == 'test1NEW'


async def test_bad_delete_user_five__not_your_acc(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}"
    }
    response = await ac.delete("/users/5", headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


async def test_delete_user_five(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test5@test.com']}"
    }
    response = await ac.delete("/users/5", headers=headers)
    assert response.status_code == 200


async def test_get_users_list_after_delete(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}"
    }
    response = await ac.get("/users/", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("users")) == 4
