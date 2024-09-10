from app.create_fastapi_app import create_app
from app.create_starlette_admin import create_admin
from app.catalog.categories.router import router as router_categories
from app.catalog.products.router import router as router_products
from app.users.router import router as router_users
from app.carts.router import router as router_carts
from app.orders.router import router as router_orders

# Создаем приложение FastAPI
app = create_app(create_custom_static_urls=True)
prefix="/api"

#Подключаем роутеры

app.include_router(router_categories,prefix=prefix)
app.include_router(router_products,prefix=prefix)

app.include_router(router_users, prefix=prefix)
app.include_router(router_carts, prefix=prefix)
app.include_router(router_orders, prefix=prefix)

#Монтируем Starlette-admin в FastAPI
admin=create_admin()
admin.mount_to(app)


