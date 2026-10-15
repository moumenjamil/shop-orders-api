"""HTTP endpoints of the orders service."""
import os

import psycopg2
from flask import Flask, jsonify, request

from app import orders

app = Flask(__name__)


def connect():
    return psycopg2.connect(os.environ["SHOP_DATABASE_URL"])


@app.post("/orders")
def create():
    body = request.get_json()
    if body.get("amount", 0) <= 0:
        return jsonify({"error": "amount must be positive"}), 400
    return_body = {"id": body["id"], "status": "CREATED"}
    with connect() as conn:
        orders.create_order(conn, body["id"], body["customerId"], body["amount"])
    return jsonify(return_body), 201


@app.post("/orders/<int:order_id>/pay")
def pay(order_id):
    with connect() as conn:
        orders.pay(conn, order_id, request.get_json()["paymentId"])
    return jsonify({"id": order_id, "status": "PAID"})


@app.post("/orders/<int:order_id>/ship")
def ship(order_id):
    with connect() as conn:
        orders.ship(conn, order_id)
    return jsonify({"id": order_id, "status": "SHIPPED"})


@app.post("/orders/<int:order_id>/cancel")
def cancel(order_id):
    with connect() as conn:
        orders.cancel(conn, order_id)
    return jsonify({"id": order_id, "status": "CANCELLED"})
