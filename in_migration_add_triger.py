from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'XXXX'
down_revision = 'YYYY'
branch_labels = None
depends_on = None

def upgrade():
    # Создание функции триггера (считаем сумму заказа всех товаров)
    op.execute("""
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
    """)

    # Создание триггера для вставки, обновления и удаления
    op.execute("""
    CREATE TRIGGER trg_update_total_amount
    AFTER INSERT OR UPDATE OR DELETE ON order_items
    FOR EACH ROW
    EXECUTE FUNCTION update_total_amount();
    """)

    # Создание функции триггера (Обновляем цену товара в корзине)
    op.execute("""
    CREATE OR REPLACE FUNCTION update_cart_price()
    RETURNS TRIGGER AS $$
    BEGIN
        UPDATE carts
        SET price = NEW.price
        WHERE product_id = NEW.id;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Создание триггера для вставки, обновления и удаления
    op.execute("""
    CREATE TRIGGER update_cart_price_trigger
    AFTER UPDATE OF price ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_cart_price();
    """)


    # Создание функции триггера (считаем сумму цены конкретного товара)
    op.execute("""
    CREATE OR REPLACE FUNCTION update_sum_price()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.sum_price := NEW.price * NEW.quantity;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Создание триггера для вставки, обновления и удаления
    op.execute("""
    CREATE TRIGGER update_sum_price_trigger_orders_items
    BEFORE INSERT OR UPDATE ON order_items
    FOR EACH ROW
    EXECUTE FUNCTION update_sum_price();
    """)

    op.execute("""
    CREATE TRIGGER update_sum_price_trigger_carts
    BEFORE INSERT OR UPDATE ON carts
    FOR EACH ROW
    EXECUTE FUNCTION update_sum_price();
    """)
    # Создание функции триггера на удаление записей если order_id IS NULL
    op.execute("""
    CREATE OR REPLACE FUNCTION delete_if_order_id_is_null()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.order_id IS NULL THEN
            DELETE FROM order_items WHERE id = NEW.id;
        END IF;
        RETURN NEW; -- Возврат NEW для AFTER триггера
    END;
    $$ LANGUAGE plpgsql;
    """)
    # Создание триггера для вставки, обновления и удаления
    op.execute("""
    CREATE TRIGGER trg_delete_if_order_id_is_null
    BEFORE INSERT OR UPDATE ON order_items
    FOR EACH ROW
    EXECUTE FUNCTION delete_if_order_id_is_null();
    """)

def downgrade():
    # Удаление триггера
    op.execute("DROP TRIGGER IF EXISTS trg_update_total_amount ON order_items;")
    # Удаление функции триггера
    op.execute("DROP FUNCTION IF EXISTS update_total_amount;")

    # Удаление триггера
    op.execute("DROP TRIGGER IF EXISTS update_cart_price_trigger ON products;")
    # Удаление функции триггера
    op.execute("DROP FUNCTION IF EXISTS update_cart_price;")

    # Удаление триггера
    op.execute("DROP TRIGGER IF EXISTS update_sum_price_trigger_orders_items ON order_items;")
    op.execute("DROP TRIGGER IF EXISTS update_sum_price_trigger_carts ON order_items;")
    # Удаление функции триггера
    op.execute("DROP FUNCTION IF EXISTS update_sum_price;")

