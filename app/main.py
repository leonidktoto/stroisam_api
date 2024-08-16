from app.create_fastapi_app import create_app
from app.create_starlette_admin import create_admin
from app.catalog.categories.router import router as router_categories
from app.catalog.products.router import router as router_products
from app.users.router import router as router_users

# Создаем приложение FastAPI
app = create_app(create_custom_static_urls=True)
prefix="/api"

#Подключаем роутеры
app.include_router(router_users, prefix=prefix)
app.include_router(router_categories,prefix=prefix)
app.include_router(router_products,prefix=prefix)

#Монтируем Starlette-admin в FastAPI
admin=create_admin()
admin.mount_to(app)


