from httpx import AsyncClient
import pytest
from sqlalchemy import Null, null


@pytest.mark.asyncio
async def test_get_main_categories(ac: AsyncClient):
    response = await ac.get("/categories/main", follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "parent_id, status_code, expected_response" ,
    [
        (0,  200, []),
        (9, 200, [
            {
                "id": 24,
                "parent_id": 9,
                "category_name": "Рейки",
                "image_url": None,
                "has_children": False
            },
            {
                "id": 25,
                "parent_id": 9,
                "category_name": "Бруски",
                "image_url": None,
                "has_children": False
            },
            {
                "id": 26,
                "parent_id": 9,
                "category_name": "Доски",
                "image_url": None,
                "has_children": False
            }
                    ]),
        (999, 200, []),
        ("9zxcc", 422, None),
        ("??", 404, None),
        ("%%%", 422, None),
    ]
)

@pytest.mark.asyncio
async def test_get_subcategories(parent_id, status_code, expected_response, ac: AsyncClient):
    response = await ac.get(f"/categories/sub/{parent_id}", follow_redirects=True)
    assert response.status_code == status_code
    if expected_response is not None:
        assert response.json() == expected_response



@pytest.mark.parametrize(
    "category_id, status_code, expected_response",
    [
        (0, 200, []),
        (26, 200, [{
      "id": 15,
      "article": 345467543,
      "product_name": "Доска",
      "price": 13,
      'image_url': None
    }]),
        (999, 200, []),
        ("9zxcc", 422, None),
        ("??", 404, None),
        ("%%%", 422, None),
    ]
)


@pytest.mark.asyncio
async def test_get_products_by_category_id(category_id, status_code,expected_response, ac: AsyncClient):
    response = await ac.get(f"/products/category/{category_id}", follow_redirects=True)
    assert response.status_code == status_code
    if expected_response is not None:
        assert response.json() == expected_response



@pytest.mark.parametrize(
    "id, status_code, expected_response",
    [
        (0,200,None),
        (999, 200, None),
        ("9zxcc", 422, None),
        ("??", 404, None),
        ("%%%", 422, None),

        (15,200,
            {"id":15,
            "article":345467543,
            "product_name":"Доска",
            "description":"прямоугольная",
            "price":13,
            "product_attributes":[
                {"attribute_name":"Материал",
                "attribute.value":"Сосна"}],
                "image_urls":[]}
        )

    ]

)

@pytest.mark.asyncio
async def test_get_products_by_id(id, status_code,expected_response, ac: AsyncClient):
    response = await ac.get(f"/products/id/{id}", follow_redirects=True)
    print("!!!!")
    print(response.content)
    assert response.status_code == status_code
    
    if expected_response is not None:
        assert response.json() == expected_response