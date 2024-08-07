from fastapi import FastAPI
#from app.nomenclature.categories.router import router as router_categories
#from app.nomenclature.products.router import router as router_products
##from app.nomenclature.products.product_attribute.router import router as router_attribute
#from app.nomenclature.products.product_image.router import router as router_image
#from sqladmin import Admin
#from app.database import async_engine 
#from app.adminpanel.view import CategoriesAdmin, ProductsAdmin


from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from starlette.middleware.wsgi import WSGIMiddleware
#from app.adminpanel.viewflask import CategoriesAdmin, ProductsAdmin
#from app.nomenclature.categories.models import Categories
#from app.nomenclature.products.models import Products
from app.database import sync_session
# Создаем приложение Flask для Flask-Admin
flask_app = Flask(__name__)
flask_app.secret_key = "supersecretkey"

# Настраиваем Flask-Admin
admin = Admin(app=flask_app, name='Admin Panel')
#admin.add_view(CategoriesAdmin(Categories, sync_session(), name="Категории"))
#admin.add_view(ProductsAdmin(Products, sync_session(),name="Товары"))

# Создаем приложение FastAPI
app = FastAPI()

# Интегрируем Flask приложение с FastAPI
app.mount("/", WSGIMiddleware(flask_app))

#app.include_router(router_categories)
#app.include_router(router_products)
#app.include_router(router_attribute)
#app.include_router(router_image)

#admin = Admin(app, async_engine)
#admin.add_view(CategoriesAdmin)
#admin.add_view(ProductsAdmin)
