from fastapi import FastAPI, HTTPException, Request

from fastapi.responses import JSONResponse, RedirectResponse
from hawk_python_sdk.modules.fastapi.types import FastapiSettings
from app.create_fastapi_app import create_app
from app.create_starlette_admin import create_admin
from app.catalog.categories.router import router as router_categories
from app.catalog.products.router import router as router_products
from app.users.router import router as router_users
from app.carts.router import router as router_carts
from app.orders.router import router as router_orders
from app.management.router import router as router_managments
from starlette.middleware.base import BaseHTTPMiddleware
from hawk_python_sdk.modules.fastapi import HawkFastapi
from app.config import settings

# Создаем приложение FastAPI
app = create_app(create_custom_static_urls=True)

                                      # Разблокировать для работы с Hawk в Production!!!
#hawk=HawkFastapi(
#  {
#    'app_instance':app, 
#    "token": settings.HAWK_TOKEN
#  })  # type: ignore


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Проверяем, начинается ли путь с "/admin"
        if request.url.path.startswith("/api/admin") and not request.url.path.startswith("/api/admin/login"):
            # Получаем токен из cookies
            token = request.cookies.get("access_token_cookie")
            # Если токена нет, перенаправляем на страницу логина
            if not token:
                return RedirectResponse(url='/admin/login')
        
        # Если токен найден или это не /admin, продолжаем выполнение запроса
        response = await call_next(request)
        return response
        

#Подключаем роутеры

app.include_router(router_categories)#,prefix=prefix)
app.include_router(router_products)#,prefix=prefix)

app.include_router(router_users)#, prefix=prefix)
app.include_router(router_carts)#, prefix=prefix)
app.include_router(router_orders)#, prefix=prefix)
app.include_router(router_managments)#, prefix=prefix)

#Монтируем Starlette-admin в FastAPI
admin=create_admin()
admin.mount_to(app)


