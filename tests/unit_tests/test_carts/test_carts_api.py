from httpx import AsyncClient
import pytest

test_data = [
        (
            {
                "product_id": 0,
                "quantity": 0    
            },
            404
        ),
        (
            {
                "product_id": 1,
                "quantity": 1    
            },
            200
        ),
        (
            {
                "product_id": "test",
                "quantity": "test"    
            },
            422
        ),
        (
            {
                "product_id": 1,
                "quantity": "test"    
            },
            422
        ),
        (
            {
                "product_id": "test",
                "quantity": 1    
            },
            422
        )
    ]

@pytest.mark.asyncio
async def test_carts_no_auth_user(ac: AsyncClient):
    response = await ac.get("/users/cart/", follow_redirects=True)
    assert response.status_code == 401
    response = await ac.post("/users/cart/items", follow_redirects=True)
    assert response.status_code == 401
    response = await ac.delete("/users/cart/items", follow_redirects=True)
    assert response.status_code == 401
    response = await ac.patch("/users/cart/items", follow_redirects=True)
    assert response.status_code == 401
    response = await ac.delete("/users/cart/items/1", follow_redirects=True)
    assert response.status_code == 401



@pytest.mark.parametrize(
    "product, status_code", test_data)
@pytest.mark.asyncio
async def test_partial_update_item(product, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.patch("/users/cart/items", json=product, follow_redirects=True)
    assert response.status_code == status_code

@pytest.mark.asyncio
async def test_get_cart_contents(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/users/cart", follow_redirects=True)
    assert response.json()[0]["product_id"] == 1
    assert response.status_code == 200

@pytest.mark.parametrize("id, status_code",
    [
        (1,204),
        (0,204),
        ("1",204),
        ("sdas",422)
    ]  
)
@pytest.mark.asyncio
async def test_remove_item_from_cart(id, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.delete(f"/users/cart/items/{id}", follow_redirects=True)
    assert response.status_code == status_code

@pytest.mark.asyncio
async def test_clear_cart(authenticated_ac: AsyncClient):
    response = await authenticated_ac.delete("/users/cart/items", follow_redirects=True)
    assert response.status_code == 204

@pytest.mark.parametrize(
    "product, status_code", test_data)
@pytest.mark.asyncio
async def test_add_item_to_cart(product, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/users/cart/items", json=product, follow_redirects=True)
    assert response.status_code == status_code