import pytest
from app.carts.dao import CartsDAO

@pytest.mark.parametrize("user_id, expected_response",
    [
        (6, "Брусок строганый 40x40x3000 мм хвоя сорт"),
        (1, None),
        (2, None)
    ]
)

@pytest.mark.asyncio
async def test_get_user_cart(user_id, expected_response):
    result = await CartsDAO.get_user_cart(user_id)
    if expected_response:
        assert result is not None
        assert result[0]["product_name"] == expected_response
    else: 
        assert result is None

@pytest.mark.asyncio
async def test_add_prdct_and_find_prdct_in_cart():
    await CartsDAO.add_data(
            product_id = 1, 
            quantity = 10,
            price = 100,
            user_id = 1
        )
    product_in_cart = await CartsDAO.find_one_or_none(product_id=1, user_id=1)
    assert product_in_cart is not None
    assert product_in_cart.product_id == 1
    assert product_in_cart.quantity == 10


@pytest.mark.parametrize("product_id, user_id",
    [
        (2,3)
    ]
)

@pytest.mark.asyncio
async def test_add_update_and_find_prdct_in_cart(product_id, user_id):
    product_in_cart = await CartsDAO.find_one_or_none(product_id=product_id, user_id=user_id)
    assert product_in_cart is not None
    assert product_in_cart.quantity == 3

    await CartsDAO.update_data(
               {
                   "quantity":50,
                   "price":100,
               },
               product_id=product_id, 
               user_id=user_id,
               )

    product_in_cart = await CartsDAO.find_one_or_none(product_id=product_id, user_id=user_id)
    assert product_in_cart is not None
    assert product_in_cart.product_id == product_id
    assert product_in_cart.quantity == 50


@pytest.mark.parametrize("product_id, user_id",
    [
        (2,5)
    ]
)

@pytest.mark.asyncio
async def test_remove_product_from_cart_by_id(product_id, user_id):
    result = await CartsDAO.get_user_cart(user_id)
    assert result is not None
    assert len(result) == 2
    
    await CartsDAO.delete_by_filter(id=2, user_id=user_id)

    result = await CartsDAO.get_user_cart(user_id)
    assert result is not None
    assert len(result) == 1

@pytest.mark.parametrize("user_id",
    [
        (5)
    ]
)

@pytest.mark.asyncio
async def test_clear_all_products_from_cart(user_id):
    result = await CartsDAO.get_user_cart(user_id)
    assert result is not None
    
    await CartsDAO.delete_by_filter(user_id=user_id)
    result = await CartsDAO.get_user_cart(user_id)
    assert result is  None
