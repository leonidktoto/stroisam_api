from typing import Any, Dict
from fastapi.background import P
from jinja2 import Template
from starlette.requests import Request


from starlette_admin import BaseField, DateTimeField, EmailField, EnumField, PasswordField, PhoneField, RelationField, URLField
from starlette_admin.contrib.sqla import ModelView


from app.catalog.attributes.models import Attributes
from app.catalog.categories.models import Categories 
from app.catalog.product_attributes.models import ProductAttributes
from app.catalog.product_images.models import ProductImages
from app.catalog.products.models import Products

from starlette_admin import IntegerField, StringField, HasOne, HasMany,BooleanField

from app.orders.models import OrderStatus, Orders
from app.users.sms_codes.models import SmsCodes
from app.users.type_user.models import TypeUser

class CustomModelView(ModelView):
    column_visibility = True
    search_builder = True
    responsive_table = False
    save_state = True


class CategoriesView(CustomModelView):  
    name='категорию'
    label='Категории'
    icon = "fa-solid fa-tags"
    
    
    fields = [
        IntegerField(
            name="id",
            label="ID",
        ),
        HasOne(
            name="parent",
            label="Родительский категория",
            identity="categories",
          #  multiple=False,
        ),
        StringField(
            name="category_name",
            label="Наименование категории",
        ),
        HasMany(
            name="children",
            label="Дочерняя категория",
            identity="categories",
            multiple=True,
        ),
        StringField(
            name="image_url",
            label="Изображение (URL ссылка)",
        ),
        HasMany(
            name="products",
            label="Товары",
            identity="products",
            multiple=True,
        ),
    ]
    
    exclude_fields_from_list = [ Categories.children, Categories.products]
    exclude_fields_from_edit =[ Categories.children]
    exclude_fields_from_create = [Categories.children, Categories.products]
    searchable_fields = [Categories.category_name]
    
class ProductImagesView(CustomModelView): 
    name='изображение'
    label='Изображения товаров'
    icon = "fa-solid fa-tags"

    fields = [
        IntegerField(
            name="id",
            label="ID",
        ),
        StringField(
            name="description",
            label="Описание",
        ),
        BooleanField(
            name="logo",
            label="Логотип"
        ),
        URLField(
            name="image_url",
            label="Изображение (URL ссылка)",
        ), 
        HasOne(
            name="product",
            label="Товары",
            identity="products",
        ),
    ]

    #exclude_fields_from_list = [ProductImages.products]
    #exclude_fields_from_create = [ProductImages.products]
   

class ProductsView(CustomModelView):
    name="товар"
    label="Товары"
    icon = "fa-solid fa-tags"


    fields = [
        IntegerField(
            name="id",
            label="ID",
        ),
        StringField(
            name="article",
            label="Артикул",
        ),
        StringField(
            name="product_name",
            label="Наименование",
        ),
        StringField(
            name="description",
            label="Описание",
        ), 
        HasOne(
            name="category",
            label="Категория",
            identity="categories",
        ),
        IntegerField(
            name="price",
            label="Цена",
        ),
        IntegerField(
            name="stock",
            label="Количество",
        ),
        HasMany(
            name="image",
            label="Изображение",
            identity="product-images",
        ),
        HasMany(
            name="product_attribute",
            label="Атрибуты товара",
            identity="product-attributes",
        ),
    ]
    #exclude_fields_from_list = [ProductImages.products]
    exclude_fields_from_create = [Products.product_attribute, Products.image]
    exclude_fields_from_edit =[Products.product_attribute, Products.image]

    


class AttributesView(CustomModelView):
    name="атрибут"
    label="Атрибуты"
    icon = "fa-solid fa-tags"
    fields = [
        IntegerField(
            name="id",
            label="ID",
        ),
        StringField(
            name="attribute_name",
            label="Наименование",
        ),
        BooleanField(
            name="filtered",
            label="Фильтр",
        ),
    ]

       

class ProductAttributesView(CustomModelView):
    name="атрибут товара"
    label="Атрибуты товаров"
    icon = "fa-solid fa-tags"
    #fields = [c.name for c in ProductAttributes.__table__.c]+[ProductAttributes.product]+[ProductAttributes.attribute_name]

    fields = [
        IntegerField(
            name="id",
            label="ID",
        ),
        HasOne(
            name="attribute_name",
            label="Наименование",
            identity="attributes",
        ),
        StringField(
            name="attribute_value",
            label="Значение",
        ),
        HasOne(
            name="product",
            label="Товары",
            identity="products",
        ),
    ]

class UsersView(CustomModelView):
    name='пользователя'
    label='Все пользователи'

    fields=[
        IntegerField(
            name="id",
            label="ID",
        ),
        StringField(
            name="first_name",
            label="Имя",
        ),
        StringField(
            name="last_name",
            label="Фамилия",
        ),
        PhoneField(
            name="phone",
            label="Телефон",
        ),
        EmailField(
            name="email",
            label="Электронная почта",
        ),
        PasswordField(
            name="hashed_password",
            label="ID",
        ),     
        IntegerField(
            name="discount",
            label="Персональная скидка",
        ),
        HasOne(
            name="type_",
            label="Тип пользователя",
            identity="type-user",
        ),
        BooleanField(
            name='is_active',
            label='Активен',
        ),
        BooleanField(
            name='is_confirmed',
            label='Подтвержден',
        ),
        IntegerField(
            name="registration_attempts",
            label="Попыток регистрации",
        )
    ]


class TypeUserView(CustomModelView):
    name='тип пользоватяля'
    label='Тип пользователя'

    fields=[
        IntegerField(
            name="id",
            label="ID",
        ),
        StringField(
            name="type_name",
            label="Тип",
        ),
        HasMany(
            name="user",
            label="Пользователи",
            identity="users"
        )
    ]

    exclude_fields_from_create = [TypeUser.user]
    exclude_fields_from_edit =[TypeUser.user]

class OrdersView(CustomModelView):
    name='заказ'
    label='Заказы'

    fields=[
        IntegerField(
            name="id",
            label="ID",
        ),
        DateTimeField(
            name="order_date",
            label="Дата заказа",
        ),
        IntegerField(
            name="total_amount",
            label="Сумма заказа"
        ),
        EnumField(
            name="order_status",
            label="Статус заказа",
            enum=OrderStatus
        ),
        HasOne(
            name="user",
            label="Пользователь",
            identity="users",
        ),
        HasMany(
            name="orderitem",
            label="Товар",
            identity="order-items",
        
        )
    ]

    exclude_fields_from_create = [Orders.order_date, Orders.order_status, Orders.total_amount]
    exclude_fields_from_edit =[Orders.order_date, Orders.total_amount]

class OrderItemsView(CustomModelView):
    name = "в заказ"
    label = "Детали заказа"

    fields=[
        IntegerField(
            name="id",
            label="ID",
        ),
        HasOne(
            name="order",
            label="Номер заказа",
            identity="orders"
        ),
        HasOne(
            name="product",
            label="Товар",
            identity="products"
        ),
        IntegerField(
            name="quantity",
            label="Количество"
        ),
        IntegerField(
            name="price",
            label="Цена",
        ),
    ]


class SmsCodesView(CustomModelView):
    name="SMS код"
    label= "SMS коды"

    fields = [c.name for c in SmsCodes.__table__.c]+[SmsCodes.user]