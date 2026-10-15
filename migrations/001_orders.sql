-- The orders table, owned by this service.
CREATE TABLE IF NOT EXISTS orders (
    id          BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(id),
    status      TEXT NOT NULL CHECK (status IN ('CREATED','PAID','SHIPPED','CANCELLED')),
    amount      NUMERIC(12,2) NOT NULL,
    payment_id  TEXT REFERENCES payments(id),
    created_at  TIMESTAMPTZ NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL
);
