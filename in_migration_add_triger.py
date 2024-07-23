from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'XXXX'
down_revision = 'YYYY'
branch_labels = None
depends_on = None


def upgrade():
    # Создание функции триггера
    op.execute("""
    CREATE OR REPLACE FUNCTION update_total_amount()
    RETURNS TRIGGER AS $$
    BEGIN
        UPDATE orders
        SET total_amount = (
            SELECT COALESCE(SUM(price), 0)
            FROM order_items
            WHERE order_id = NEW.order_id
        )
        WHERE id = NEW.order_id;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Создание триггера для вставки и обновления
    op.execute("""
    CREATE TRIGGER trg_update_total_amount
    AFTER INSERT OR UPDATE OR DELETE ON order_items
    FOR EACH ROW
    EXECUTE FUNCTION update_total_amount();
    """)

def downgrade():
    # Удаление триггера
    op.execute("DROP TRIGGER IF EXISTS trg_update_total_amount ON order_items;")
    # Удаление функции триггера
    op.execute("DROP FUNCTION IF EXISTS update_total_amount;")
