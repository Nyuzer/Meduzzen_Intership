from httpx import AsyncClient


async def test_get_users(ac: AsyncClient):
    response = await ac.get("/users/")
    assert response.status_code == 200
    assert response.json().get("users") == []


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


async def test_create_user_error(ac: AsyncClient):
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


async def test_get_users_list(ac: AsyncClient):
    response = await ac.get("/users/")
    assert response.status_code == 200
    assert len(response.json().get("users")) == 3


async def test_get_user_by_id(ac: AsyncClient):
    response = await ac.get("/users/1")
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("email") == 'test1@test.com'
    assert response.json().get("username") == 'test1'


async def test_bad_get_user_by_id(ac: AsyncClient):
    response = await ac.get("/users/4")
    assert response.status_code == 404


async def test_update_user_one(ac: AsyncClient):
    payload = {
      "username": "test1NEW",
    }
    response = await ac.put("/users/1", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 1


async def test_get_user_by_id_updates(ac: AsyncClient):
    response = await ac.get("/users/1")
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("email") == 'test1@test.com'
    assert response.json().get("username") == 'test1NEW'


async def test_update_user_not_exist(ac: AsyncClient):
    payload = {
      "username": "test1NEW",
    }
    response = await ac.put("/users/4", json=payload)
    assert response.status_code == 404


async def test_delete_user_one(ac: AsyncClient):
    response = await ac.delete("/users/1")
    assert response.status_code == 200


async def test_get_users_list_after_delete(ac: AsyncClient):
    response = await ac.get("/users/")
    assert response.status_code == 200
    assert len(response.json().get("users")) == 2
