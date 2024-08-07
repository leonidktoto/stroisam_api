from fastapi import FastAPI
from fastapi.responses import JSONResponse


from app.catalog.attributes.models import Attributes
from app.catalog.product_attributes.models import ProductAttributes



from starlette_admin.contrib.sqla import Admin
from starlette_admin import I18nConfig, DropDown

from starlette.applications import Starlette

from app.database import sync_engine
from app.catalog.categories.models import Categories
from app.catalog.products.models import Products
from app.catalog.product_images.models import ProductImages
from app.adminpanel.viewstarlette import AttributesView, CategoriesView, OrderItemsView, OrdersView, ProductAttributesView, ProductImagesView, ProductsView, SmsCodesView, TypeUserView, UsersView
from app.exceptions import BookingException
from app.orders.models import Orders
from app.orders.order_items.models import OrderItems
from app.users.models import Users
from app.users.sms_codes.models import SmsCodes
from app.users.type_user.models import TypeUser

from app.catalog.categories.router import router as router_categories
from app.catalog.products.router import router as router_products
from app.users.router import router as router_users




# Создаем приложение FastAPI
app = FastAPI()


app.include_router(router_users)
app.include_router(router_categories)
app.include_router(router_products)



app_starlette = Starlette()  # FastAPI()


admin = Admin(sync_engine, title="Панель администратора", i18n_config = I18nConfig(default_locale="ru"))


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
            OrdersView(Orders),
            OrderItemsView(OrderItems),
        ],
    )
)
admin.add_view(SmsCodesView(SmsCodes, icon="fa-solid fa-sms"))

admin.mount_to(app)


