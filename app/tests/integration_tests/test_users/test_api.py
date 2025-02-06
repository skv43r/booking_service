from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("email, password, status_code", [
    ("test@user.com", "password123", 200),
    ("test@user.com", "pasword111", 409),
    ("testuser", "password123", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code

@pytest.mark.parametrize("email, password, status_code", [
    ("fedor@moloko.ru", "test", 200),
    ("sharik@moloko.ru", "test", 200),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code