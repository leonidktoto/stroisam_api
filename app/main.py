from app.carts.router import router as router_carts
from app.catalog.categories.router import router as router_categories
from app.catalog.products.router import router as router_products
from app.create_fastapi_app import create_app
from app.create_starlette_admin import create_admin
from app.config import settings
from app.management.router import router as router_managments
from app.orders.router import router as router_orders
from app.users.router import router as router_users
from app.favorites.router import router as router_favorites
from hawk_python_sdk.modules.fastapi import HawkFastapi
from fastapi.middleware.cors import CORSMiddleware

# Создаем приложение FastAPI
app = create_app(create_custom_static_urls=True)

#Разблокировать для работы с Hawk в Production!!!
hawk=HawkFastapi(
 {
   'app_instance':app,
   "token": settings.HAWK_TOKEN
 })  # type: ignore


# class JWTAuthMiddleware(BaseHTTPMiddleware):
#    async def dispatch(self, request: Request, call_next):
#        # Проверяем, начинается ли путь с "/admin"
#        if request.url.path.startswith("/api/admin") and not request.url.path.startswith("/api/admin/login"):
#            # Получаем токен из cookies
#            token = request.cookies.get("refresh")
#            # Если токена нет, перенаправляем на страницу логина
#            if not token:
#                return RedirectResponse(url='/admin/login')
#
#        # Если токен найден или это не /admin, продолжаем выполнение запроса
#        response = await call_next(request)
#        return response

origins = ["http://localhost:5173"]
#CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)
# Подключаем роутеры
app.include_router(router_categories)  # ,prefix=prefix)
app.include_router(router_products)  # ,prefix=prefix)

app.include_router(router_users)  # , prefix=prefix)
app.include_router(router_carts)  # , prefix=prefix)
app.include_router(router_favorites)  # , prefix=prefix)
app.include_router(router_orders)  # , prefix=prefix)
app.include_router(router_managments)  # , prefix=prefix)

# Монтируем Starlette-admin в FastAPI
admin = create_admin()
admin.mount_to(app)
