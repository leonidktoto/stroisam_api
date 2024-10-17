from fastapi import FastAPI, HTTPException, Request

from fastapi.responses import JSONResponse, RedirectResponse
from app.create_fastapi_app import create_app
from app.create_starlette_admin import create_admin
from app.catalog.categories.router import router as router_categories
from app.catalog.products.router import router as router_products
from app.users.router import router as router_users
from app.carts.router import router as router_carts
from app.orders.router import router as router_orders
from app.management.router import router as router_managments
from starlette.middleware.base import BaseHTTPMiddleware

# Создаем приложение FastAPI
app = create_app(create_custom_static_urls=True)
#app = FastAPI()
#prefix="/api"


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Проверяем, начинается ли путь с "/admin"
        if request.url.path.startswith("/admin") and not request.url.path.startswith("/admin/login"):
            # Получаем токен из cookies
            token = request.cookies.get("access_token_cookie")
            
            # Если токена нет, перенаправляем на страницу логина
            if not token:
                return RedirectResponse(url='/admin/login')
        
        # Если токен найден или это не /admin, продолжаем выполнение запроса
        response = await call_next(request)
        return response
        
      #  try:
      #      payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
      #      request.state.user = payload
      #  except jwt.ExpiredSignatureError:
      #      raise HTTPException(status_code=401, detail="Token has expired")
      #  except jwt.InvalidTokenError:
      #      raise HTTPException(status_code=401, detail="Invalid token")
        
        return await call_next(request)

#app.add_middleware(JWTAuthMiddleware)

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


