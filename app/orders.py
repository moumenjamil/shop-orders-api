"""Every write of the orders service to the shop database (public.orders)."""
from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


# Which status an order may move to from each status.
NEXT = {
    OrderStatus.CREATED: {OrderStatus.PAID, OrderStatus.CANCELLED},
    OrderStatus.PAID: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
    OrderStatus.SHIPPED: {OrderStatus.REFUNDED},
    OrderStatus.CANCELLED: set(),
    OrderStatus.REFUNDED: set(),
}


def create_order(conn, order_id, customer_id, amount):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO orders (id, customer_id, status, amount, created_at, updated_at)"
            " VALUES (%s, %s, %s, %s, now(), now())",
            (order_id, customer_id, OrderStatus.CREATED.value, amount))


def pay(conn, order_id, payment_id):
    _move(conn, order_id, OrderStatus.PAID, payment_id=payment_id)


def ship(conn, order_id):
    _move(conn, order_id, OrderStatus.SHIPPED)


def cancel(conn, order_id):
    _move(conn, order_id, OrderStatus.CANCELLED)


def refund(conn, order_id):
    """A shipped order the customer sent back: the money goes back to them."""
    _move(conn, order_id, OrderStatus.REFUNDED)


def _move(conn, order_id, to, payment_id=None):
    with conn.cursor() as cur:
        cur.execute("SELECT status FROM orders WHERE id = %s FOR UPDATE", (order_id,))
        row = cur.fetchone()
        if row is None:
            raise LookupError(f"order {order_id} not found")
        if to not in NEXT[OrderStatus(row[0])]:
            raise ValueError(f"order {order_id}: {row[0]} -> {to.value} is not allowed")
        if payment_id is None:
            cur.execute("UPDATE orders SET status = %s, updated_at = now() WHERE id = %s",
                        (to.value, order_id))
        else:
            cur.execute("UPDATE orders SET status = %s, payment_id = %s, updated_at = now()"
                        " WHERE id = %s", (to.value, payment_id, order_id))
