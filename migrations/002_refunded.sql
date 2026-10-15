-- Refunds: a shipped order can now be REFUNDED.
ALTER TABLE orders DROP CONSTRAINT IF EXISTS orders_status_check;
ALTER TABLE orders ADD CONSTRAINT orders_status_check
    CHECK (status IN ('CREATED','PAID','SHIPPED','CANCELLED','REFUNDED'));
