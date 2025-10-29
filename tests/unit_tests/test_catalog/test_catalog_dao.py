import pytest

from app.catalog.categories.dao import CategoriesDAO
from app.catalog.products.dao import ProductsDAO


@pytest.mark.parametrize(
    "data",
    [
        (
            {
                "category_name": "Игрушки",
                "parent_id": None,
            }
        ),
        (
            {
                "category_name": "test",
                "parent_id": 1,
            }
        ),
    ],
)
@pytest.mark.asyncio
async def test_add_and_get_category(data):
    new_category = await CategoriesDAO.add_data(**data)

    new_category = await CategoriesDAO.find_one_or_none(id=new_category["id"])

    assert new_category is not None


@pytest.mark.parametrize(
    "category_id, expected_response",
    [
        (
            9,
            [
                {
                    "id": 25,
                    "parent_id": 9,
                    "category_name": "Бруски",
                    "image_url": None,
                    "has_children": False,
                },
                {
                    "id": 26,
                    "parent_id": 9,
                    "category_name": "Доски",
                    "image_url": None,
                    "has_children": False,
                },
                                {
                    "id": 24,
                    "parent_id": 9,
                    "category_name": "Рейки",
                    "image_url": None,
                    "has_children": False,
                },
            ],
        ),
        (0, []),
        (-1, []),
        (99, []),
    ],
)
@pytest.mark.asyncio
async def test_find_subcategory(category_id, expected_response):
    subcategory = await CategoriesDAO.find_subcategory(category_id)
    assert subcategory == expected_response


@pytest.mark.asyncio
async def test_find_products_by_category_id():
    result = await ProductsDAO.find_products(category_id=25)
    assert len(result) == 10
    assert result[0]["id"] == 10
    assert result[0]["image_url"] is None


@pytest.mark.asyncio
async def test_find_products_by_id():
    result = await ProductsDAO.find_products_by_id(1)
    assert result is not None
    assert result["id"] == 1
    assert result["product_name"] == "Брусок строганый 40x40x3000 мм хвоя сорт"
    assert result["product_attributes"][0]["attribute.value"] == "Сосна"
