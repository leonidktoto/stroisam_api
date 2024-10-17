from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("first_name, email, phone, last_name, status_code", [
    ("misha", "misha@test.com", "9170171717", "m", 200),
    ("petr", "petr@test.com", "9170171718", "m", 200),
    ("ivan", "ivan@test.com", "9170171717", "m", 409),
    (123, "pet9@test.com", "9170171717", "m", 422),
    ("igor", "igor.com", "9170171717", "m", 422),
    ("vas9", "vas9@test.com", 9170171717, "m", 422),
    ("oleg", "oleg@test.com", "9170171717", 123, 422),
    ("ser", "ser@test.com", "9172171726", None, 200)
])
@pytest.mark.asyncio
async def test_register_user(first_name, email, phone, last_name, status_code,  ac: AsyncClient):

    request_data={
        "first_name" : first_name,
        "email" : email,
        "phone" : phone
    }

    if last_name is not None:
        request_data["last_name"] = last_name    

    response = await ac.post("/users/register", json=request_data)

    assert response.status_code == status_code