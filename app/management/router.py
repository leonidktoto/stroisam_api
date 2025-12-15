from io import BytesIO
from typing import List

import boto3
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Request,
    UploadFile,
)
from fastapi.responses import JSONResponse, RedirectResponse
from PIL import Image
from pydantic import _migration

from app.catalog.categories.dao import CategoriesDAO
from app.catalog.product_attributes.dao import ProductAttributesDAO
from app.catalog.product_images.dao import ProductImagesDAO
from app.catalog.products.dao import ProductsDAO
from app.config import settings
from app.management.helpers import load_images_to_s3
from app.management.dao import ManagementDAO
from app.orders.order_deliveries.dao import OrderDeliveriesDAO
from app.orders.order_items.dao import OrdersItemsDAO
from app.users.schemas import SUsers
from app.users.validation import get_admin_active_auth_user
from app.orders.dao import OrdersDAO
from app.exceptions import OrderNumError
from app.management.schemas import SOrderDeliveryUpdate, SOrderFindPayload, SOrderItemsUpdatePayload, SOrderStatusUpdate

router = APIRouter(
    prefix="/managment",
    tags=["Администрирование"],
    # dependencies=[Depends(http_bearer)]
)

# Инициализация клиента S3
s3 = boto3.client(
    "s3",
    endpoint_url=settings.ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def resize_image(image: Image.Image, size: tuple) -> BytesIO:
    """
    Функция для изменения размера изображения с сохранением пропорций.
    Возвращает изображение в виде байтового потока.
    """
    resized_image = image.copy()
    resized_image.thumbnail(size)  # Сохранение пропорций
    img_byte_arr = BytesIO()
    resized_image.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)
    return img_byte_arr


@router.post("/upload-image/")
async def upload_image(
    file_dir: str,
    images: list[UploadFile] = File([...]),
    user: SUsers = Depends(get_admin_active_auth_user),
):
    result = {}

    if images:
        if images[0].filename != "":
            for image in images:
                image_url = load_images_to_s3(file=image, file_dir=file_dir)
                result[image.filename] = image_url
    print(result)
    return result


@router.post("/add_product", name="managment:add_product")
async def add_product_form(
    request: Request,
    product_name: str = Form(..., max_length=255),
    article: str = Form("", max_length=20),
    category_id: int = Form(..., gt=0, le=999999999),
    price: int = Form(..., gt=0, le=999999999),
    stock: int = Form(..., gt=0, le=999999999),
    description: str = Form("", max_length=2000),
    attributes: List[str] = Form([]),
    attribute_values: List[str] = Form([], max_length=2000),
    images: list[UploadFile] = File(None),
    user: SUsers = Depends(get_admin_active_auth_user),
):
    product = None

    try:
        dict_attr = dict(zip(attributes, attribute_values))
        print("Result:", dict_attr)

        form_data = await request.form()
        print("Form Data:", form_data)

        # Добавление продукта
        product = await ProductsDAO.add_data(
            product_name=product_name,
            article=article,
            category_id=category_id,
            price=price,
            stock=stock,
            description=description,
        )
        print(product.id)

        # Добавление атрибутов продукта
        if dict_attr:
            for attr_id, value in dict_attr.items():
                await ProductAttributesDAO.add_data(
                    product_id=product.id, attribute_name_id=int(attr_id), attribute_value=value
                )

        # Получение категории и добавление изображений
        if images[0].filename != "":  # Проверим на пустое значение из формы
            category = await CategoriesDAO.find_by_id(category_id)
            if category:
                category_name = category.category_name

                if images:
                    for image in images:

                        image_url = load_images_to_s3(
                            file=image, file_dir=category_name, product_id=product.id
                        )
                        logo = (
                            True if image.filename and image.filename.startswith("logo.") else False
                        )
                        await ProductImagesDAO.add_data(
                            product_id=product.id, image_url=image_url, logo=logo
                        )

        return RedirectResponse(url="/api/admin/add_product", status_code=303)

    except Exception as e:
        if product:
            await ProductsDAO.delete_by_filter(id=product.id)
        print(f"Ошибка: {e}")
        return JSONResponse(
            content={"error": "Ошибка добавления товара", "Детали": str(e)}, status_code=400
        )



@router.post("/find_order")
async def find_order(
    payload: SOrderFindPayload,
    user: SUsers = Depends(get_admin_active_auth_user),
):
    order_id = payload.order_id

    if not await OrdersDAO.find_one_or_none(id=order_id):
        raise OrderNumError
    return await ManagementDAO.find_order(order_id=order_id)

@router.put("/order_items/{order_id}/update")
async def update_order(
    order_id: int,
    payload: SOrderItemsUpdatePayload, 
    user: SUsers = Depends(get_admin_active_auth_user),
):
    if not await OrdersDAO.find_one_or_none(id=order_id):
        raise OrderNumError
    new_items = [
        item.model_dump() | {"order_id": order_id}
        for item in payload.items
    ]

    await OrdersItemsDAO.delete_by_filter(order_id=order_id)
    await OrdersItemsDAO.add_many(data_list = new_items)

    
    return {"message": "Заказ пользователя обновлен", "order_id": order_id}

@router.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    payload: SOrderStatusUpdate,
    user: SUsers = Depends(get_admin_active_auth_user),
):
    order = await OrdersDAO.find_one_or_none(id=order_id)
    if not order:
        raise OrderNumError

    # колонка order_status: Mapped[OrderStatus] – можно передавать Enum
    await OrdersDAO.update_data({"order_status": payload.order_status}, id=order_id)

    return {"status": "ok"}

@router.put("/orders/{order_id}/delivery")
async def update_order_delivery(
    order_id: int,
    payload: SOrderDeliveryUpdate,
    user: SUsers = Depends(get_admin_active_auth_user),
):
    delivery = await OrderDeliveriesDAO.find_one_or_none(order_id=order_id)
    if not delivery:
        # если у тебя своя ошибка — можешь бросить её
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Delivery not found")

    await OrderDeliveriesDAO.update_data(
        {"desired_delivery_at": payload.desired_delivery_at},
        order_id=order_id,
    )

    return {"status": "ok"}