from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import I18nConfig, DropDown
from starlette.middleware import Middleware
from starlette_admin.contrib.sqla import Admin
from app.adminpanel.provider import MyAuthProvider
from app.adminpanel.viewstarlette import (
    AttributesView,
    CartsView,
    CategoriesView,
    OrderItemsView,
    OrdersView,
    ProductAttributesView,
    ProductImagesView,
    ProductsView,
    SmsCodesView,
    TypeUserView,
    UsersView)
from app.carts.models import Carts
from app.database import sync_engine
from app.catalog.categories.models import Categories
from app.catalog.products.models import Products
from app.catalog.product_images.models import ProductImages
from app.catalog.product_attributes.models import ProductAttributes
from app.catalog.attributes.models import Attributes
from app.users.models import Users
from app.users.type_user.models import TypeUser
from app.users.sms_codes.models import SmsCodes
from app.orders.models import Orders
from app.orders.order_items.models import OrderItems


def create_admin() -> Admin:
    admin = Admin(
    sync_engine, 
    title="Панель администратора", 
    i18n_config = I18nConfig(default_locale="ru"),
    auth_provider=MyAuthProvider(allow_routes=["app/adminpanel/statics/logo.svg"]),
    middlewares=[Middleware(SessionMiddleware, secret_key="123")],
    templates_dir="app/adminpanel/templates",
    )


    admin.add_view(
        DropDown(
            "Каталог",
            icon="fa fa-cube",
            views=[
                CategoriesView(Categories),
                ProductsView(Products),
                ProductAttributesView(ProductAttributes),
                ProductImagesView(ProductImages),
                AttributesView(Attributes),
            ],
        )
    )
    admin.add_view(
        DropDown(
            "Пользователи и типы",
            icon="fa fa-user-cog",
            views=[
                UsersView(Users),
                TypeUserView(TypeUser),
            ],
        )
    )
    admin.add_view(
        DropDown(
            "Управление заказами",
            icon="fa fa-shopping-cart",
            views=[
                CartsView(Carts),
                OrdersView(Orders),
                OrderItemsView(OrderItems),
            ],
        )
    )
    admin.add_view(SmsCodesView(SmsCodes, icon="fa-solid fa-sms"))


    return admin