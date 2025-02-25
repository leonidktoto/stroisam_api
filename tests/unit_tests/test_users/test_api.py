import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "first_name, email, phone, last_name, status_code",
    [
        ("misha", "misha@test.com", "9170171717", "m", 200),
        ("misha", "misha@test.com", "9170171719", "m", 200),
        ("petr", "petr@test.com", "9170171718", "m", 200),
        ("ivan", "ivan@test.com", "9170171717", "m", 409),
        (123, "pet9@test.com", "9170171717", "m", 422),
        ("igor", "igor.com", "9170171717", "m", 422),
        ("vas9", "vas9@test.com", 9170171717, "m", 422),
        ("oleg", "oleg@test.com", "9170171717", 123, 422),
        ("ser", "ser@test.com", "9172171726", None, 200),
        ("", "oleg@test.com", "9170171717", 123, 422),
        ("oleg", "@test.com", "9170171717", 123, 422),
        ("oleg", "oleg@test.com", "", 123, 422),
    ],
)
@pytest.mark.asyncio
async def test_register_user(first_name, email, phone, last_name, status_code, ac: AsyncClient):

    request_data = {"first_name": first_name, "email": email, "phone": phone}

    if last_name is not None:
        request_data["last_name"] = last_name

    response = await ac.post("/users/register", json=request_data)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("9170176646", "123", 200),
        ("9170176646", "123", 401),
        ("9170176647", "124", 200),
        ("9170176648", "125", 403),
        ("9170176649", "126", 200),
        ("9270001213", "1111", 409),
        ("", "126", 422),
        ("9170176646", "", 422),
        ("", "", 422),
    ],
)
@pytest.mark.asyncio
async def test_login(username, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/users/login", data={"username": username, "password": password}, follow_redirects=True
    )

    assert response.status_code == status_code

    if status_code == 200:
        assert "access" in response.cookies, "Cookie 'access' не найдена"
        assert "refresh" in response.cookies, "Cookie 'refresh' не найдена"
    else:
        assert (
            "access" not in response.cookies
        ), "Cookie 'access' не должна быть установлена при ошибке"
        assert (
            "refresh" not in response.cookies
        ), "Cookie 'refresh' не должна быть установлена при ошибке"


@pytest.mark.parametrize(
    "phone, status_code",
    [
        ("9170170001", 409),
        #  ("9170176646", 200),
        ("9170176955", 423),
        ("1", 422),
        ("12", 422),
        ("123", 422),
        ("1234", 422),
        ("12345", 422),
        ("123456", 422),
        ("1234567", 422),
        ("123456789", 422),
        ("917O176646", 422),
    ],
)
@pytest.mark.asyncio
async def test_sms_verification(phone, status_code, ac: AsyncClient):
    response = await ac.post(
        "/users/sms_verification",
        json={
            "phone": phone,
        },
        follow_redirects=True,
    )

    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_auth_user_check_self_info(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/users/me", follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_auth_user_check_self_info_not_auth(ac: AsyncClient):
    response = await ac.get("/users/me", follow_redirects=True)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_user(authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/users/logout", follow_redirects=True)

    assert response.status_code == 200
    if response.status_code == 200:
        assert "access" not in authenticated_ac.cookies
        assert "refresh" not in authenticated_ac.cookies
