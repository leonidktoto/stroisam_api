from pydantic_core.core_schema import model_field
import pytest
import json
from sqlalchemy import insert, text
import asyncio

from app.config import settings
from app.database import Base, async_engine, sync_engine, async_session_maker
from app.users.models import Users
from app.users.type_user.models import TypeUser
from app.users.sms_codes.models import SmsCodes
from app.catalog.attributes.models import Attributes
from app.catalog.categories.models import Categories
from app.catalog.products.models import Products
from app.catalog.product_attributes.models import ProductAttributes
from app.catalog.product_images.models import ProductImages
from app.orders.models import Orders
from app.orders.order_items.models import OrderItems
from app.carts.models import Carts
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from app.main import app as fastapi_app
from app.create_fastapi_app import lifespan


@pytest.fixture(scope= "session", autouse=True)
async def setup_db():
    print(f"{settings.DB_NAME=}")
    assert settings.MODE == "TEST"
    async with async_engine.begin() as conn:


        # Удаление функции триггера
        await conn.execute(text("DROP FUNCTION IF EXISTS update_total_amount CASCADE;"))

        # Удаление функции триггера
        await conn.execute(text("DROP FUNCTION IF EXISTS update_cart_price CASCADE;"))

        # Удаление функции триггера
        await conn.execute(text("DROP FUNCTION IF EXISTS update_sum_price CASCADE;"))

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


        # Создание функции триггера (считаем сумму заказа всех товаров)
        await conn.execute(text("""
        CREATE OR REPLACE FUNCTION update_total_amount()
        RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'DELETE' THEN
                UPDATE orders
                SET total_amount = (
                    SELECT COALESCE(SUM(quantity * price), 0)
                    FROM order_items
                    WHERE order_id = OLD.order_id
                )
                WHERE id = OLD.order_id;
                RETURN OLD;
            ELSE
                UPDATE orders
                SET total_amount = (
                    SELECT COALESCE(SUM(quantity * price), 0)
                    FROM order_items
                    WHERE order_id = NEW.order_id
                )
                WHERE id = NEW.order_id;
                RETURN NEW;
            END IF;
        END;
        $$ LANGUAGE plpgsql;
        """))
        

        # Создание триггера для вставки, обновления и удаления
        await conn.execute(text("""
        CREATE TRIGGER trg_update_total_amount
        AFTER INSERT OR UPDATE OR DELETE ON order_items
        FOR EACH ROW
        EXECUTE FUNCTION update_total_amount();
        """))

        # Создание функции триггера (Обновляем цену товара в корзине)
        await conn.execute(text("""
        CREATE OR REPLACE FUNCTION update_cart_price()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE carts
            SET price = NEW.price
            WHERE product_id = NEW.id;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """))

        # Создание триггера для вставки, обновления и удаления
        await conn.execute(text("""
        CREATE TRIGGER update_cart_price_trigger
        AFTER UPDATE OF price ON products
        FOR EACH ROW
        EXECUTE FUNCTION update_cart_price();
        """))


        # Создание функции триггера (считаем сумму цены конкретного товара)
        await conn.execute(text("""
        CREATE OR REPLACE FUNCTION update_sum_price()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.sum_price := NEW.price * NEW.quantity;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """))

        # Создание триггера для вставки, обновления и удаления
        await conn.execute(text("""
        CREATE TRIGGER update_sum_price_trigger_orders_items
        BEFORE INSERT OR UPDATE ON order_items
        FOR EACH ROW
        EXECUTE FUNCTION update_sum_price();
        """))

        await conn.execute(text("""
        CREATE TRIGGER update_sum_price_trigger_carts
        BEFORE INSERT OR UPDATE ON carts
        FOR EACH ROW
        EXECUTE FUNCTION update_sum_price();
        """))
        # Создание функции триггера на удаление записей если order_id IS NULL
        await conn.execute(text("""
        CREATE OR REPLACE FUNCTION delete_if_order_id_is_null()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.order_id IS NULL THEN
                DELETE FROM order_items WHERE id = NEW.id;
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        """))
        # Создание триггера для вставки, обновления и удаления
        await conn.execute(text("""
        CREATE TRIGGER trg_delete_if_order_id_is_null
        BEFORE INSERT OR UPDATE ON order_items
        FOR EACH ROW
        EXECUTE FUNCTION delete_if_order_id_is_null();
        """))
#
        

    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", "r", encoding = "utf8") as file:
            print(model)
            return json.load(file)

    categories=open_mock_json("categories")
    products=open_mock_json("products")
    attributes=open_mock_json("attributes")
    product_attributes=open_mock_json("product_attributes")
    type_user=open_mock_json("type_users")
    users=open_mock_json("users")
    sms_codes=open_mock_json("sms_codes")

    async with async_session_maker() as session:
        add_category = insert(Categories).values(categories)
        add_products = insert(Products).values(products)
        add_attributes = insert(Attributes).values(attributes)
        add_products_attributes = insert(ProductAttributes).values(product_attributes)
        add_type_user = insert(TypeUser).values(type_user)
        add_user = insert(Users).values(users)
        add_sms_codes = insert(SmsCodes).values(sms_codes)

        await session.execute(add_category)
        await session.execute(add_products)
        await session.execute(add_attributes)
        await session.execute(add_products_attributes)
        await session.execute(add_type_user)
        await session.execute(add_user)
        await session.execute(add_sms_codes)
        await session.commit()


@pytest.fixture(scope="function")
async def test_app():
    async with lifespan(fastapi_app):
        return fastapi_app

@pytest.fixture(scope="function")
async def ac(test_app):
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as ac:
        yield ac


#    Аутентифицированный пользователь
@pytest.fixture(scope="session")
async def test_app_auth():
    async with lifespan(fastapi_app):
        return fastapi_app

@pytest.fixture(scope="session")
async def authenticated_ac(test_app_auth):
    async with AsyncClient(transport=ASGITransport(app=test_app_auth), base_url="http://test_auth_user") as ac:
        response = await ac.post("/users/login", data={
        "username": "1111111111",
        "password": "126"
    }, follow_redirects=True)

        assert ac.cookies["access"], "Cookie 'access' не найдена"
        assert ac.cookies["refresh"], "Cookie 'refresh' не найдена"

        yield ac

@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session

