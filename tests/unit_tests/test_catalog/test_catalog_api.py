from httpx import AsyncClient
import pytest


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
      "article": None,
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
            "article": None,
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
    assert response.status_code == status_code
    
    if expected_response is not None:
        assert response.json() == expected_response




@pytest.mark.parametrize(
    "category_id, filters, status_code, expected_response",
        [
            (24, [
            {
                "attribute_name": "Материал",
                "attribute_value": [
                "Сосна", "Береза", "Хвоя"
                ]
            },
            {
                "attribute_name": "Сорт",
                "attribute_value": [
                "Люкс", "Оптима"
                ]
            },
            {
                "attribute_name": "Размер",
                "attribute_value": [
                "40x50x2000 мм", "20x40x2000 мм"
                ]
            }
            ], 200, [
            {
                "id": 14,
                "article": None,
                "product_name": "Рейка строганая 40x50x2000 мм хвоя сорт Оптима",
                "price": 120,
                "image_url": None
            }]
            ),
            (
                24, [{"test":"test"}], 422, None   
            ),
            (
                "24", [{"test":"test"}], 422, None   
            ),
            (
                24, None , 422, None   
            ),
            (24, [
            {
                "attribute_name": "Размер",
                "attribute_value": [
                "40x50x2000 мм", "20x40x2000 мм"
                ]
            }
            ], 200, [
            {
                "id": 14,
                "article": None,
                "product_name": "Рейка строганая 40x50x2000 мм хвоя сорт Оптима",
                "price": 120,
                "image_url": None
            }]
            ),

        ]
    )


@pytest.mark.asyncio
async def test_get_product_by_filter(category_id, filters, status_code, expected_response, ac: AsyncClient):
    payload = {"filters": filters, "category_id": category_id}
    print(filters)

    response = await ac.post(f"/products/filter?category_id={category_id}",  json=filters, follow_redirects=True)
    assert response.status_code == status_code
    
    if expected_response is not None:
        assert response.json() == expected_response


   